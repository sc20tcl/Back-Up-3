import { expect } from "chai";
import { ethers } from "hardhat";
import { HardhatEthersSigner } from "@nomicfoundation/hardhat-ethers/signers";
import { CarPooling } from "../typechain-types";

describe("CarPooling",  () => {
    let carPooling: CarPooling;
    let user1: HardhatEthersSigner;
    let user2: HardhatEthersSigner;
    let user3: HardhatEthersSigner;
    let user4: HardhatEthersSigner;
    let user5: HardhatEthersSigner;
    let balanceBefore: bigint;
    let balanceAfter: bigint;

    beforeEach(async () => {
        const CarPooling = await ethers.getContractFactory("CarPooling");
        [user1, user2, user3, user4, user5] = await ethers.getSigners();

        carPooling = await CarPooling.deploy();
    });

    it("should allow users to register as a passenger", async () => {
        // Check: Unregistered user should not be a passenger in the member struct
        await carPooling.getPassenger(user1.address).then((passenger) => {
            expect(passenger.isRegistered).to.be.false;
            expect(passenger.hasRide).to.be.false;
        })
        // Register user as a passenger
        await carPooling.connect(user1).passengerRegister();
        // Check: Registered user should be a passenger
        await carPooling.getPassenger(user1.address).then((passenger) => {
            expect(passenger.isRegistered).to.be.true;
            expect(passenger.hasRide).to.be.false;
        })
        // Check: Registered passenger should not be able to register as a passenger again
        await expect(carPooling.connect(user1).passengerRegister()).to.be.reverted;
    });

    it("should allow users to register as a driver", async () => {
        // Check: Unregistered user should not be a driver in the member struct
        await carPooling.getDriver(user1.address).then((driver) => {
            expect(driver.isRegistered).to.be.false;
            expect(driver.hasRide).to.be.false;
        })
        // Register user as a driver
        await carPooling.connect(user1).driverRegister();
        // Check: Registered user should be a driver in the member struct
        await carPooling.getDriver(user1.address).then((driver) => {
            expect(driver.isRegistered).to.be.true;
            expect(driver.hasRide).to.be.false;
        })
        // Check: Registered driver should not be able to register as a driver again
        await expect(carPooling.connect(user1).driverRegister()).to.be.reverted;
    });

    it("should allow drivers to create rides", async () => {
        // Check: Unregistered user should not be able to create a ride
        await expect(carPooling.connect(user1).createRide(10, 5, 10, 0, 1)).to.be.reverted;
        // Register user as a driver
        await carPooling.connect(user1).driverRegister();
        await carPooling.getDriver(user1).then((driver) => {
           expect(driver.hasRide).to.be.false;
        });
        // Check: Ride can't be created with no seats
        await expect(carPooling.connect(user1).createRide(10, 0, 10, 0, 1)).to.be.reverted;
        // Check: Ride can't be created with free seats
        await expect(carPooling.connect(user1).createRide(10, 5, 0, 0, 1)).to.be.reverted;
        // Check: Ride can't be created with invalid travel times
        await expect(carPooling.connect(user1).createRide(24, 5, 5, 0, 1)).to.be.reverted;
        // Check: Ride can't be created with origin and destination equal
        await expect(carPooling.connect(user1).createRide(23, 5, 5, 1, 1)).to.be.reverted;
        // Check: Registered driver should be able to create a ride with valid parameters and emit RideCreated event
        await expect(carPooling.connect(user1).createRide(10, 5, 10, 0, 1)).to.emit(carPooling, 'RideCreated').withArgs(0, user1.address, 10, 5, 10, 0, 1);
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.driver).to.equal(user1.address);
            expect(ride.travelTime).to.equal(10);
            expect(ride.availableSeats).to.equal(5);
            expect(ride.seatPrice).to.equal(10);
            expect(ride.origin).to.equal(0);
            expect(ride.destination).to.equal(1);
            expect(ride.status).to.equal(0);
            expect(ride.passengerAddr.length).to.equal(0);
        });
        await carPooling.getDriver(user1).then((driver) => {
           expect(driver.hasRide).to.be.true;
        });
        await expect(carPooling.connect(user1).createRide(10, 5, 10, 0, 1)).to.be.reverted;
    });

    it("should allow users to query rides", async () => {
        // Requires correct implementation of createRide
        // Create three rides
        await carPooling.connect(user1).driverRegister();
        await carPooling.connect(user1).createRide(10, 5, ethers.parseEther("10"), 0, 1);
        await carPooling.connect(user2).driverRegister();
        await carPooling.connect(user2).createRide(11, 3, ethers.parseEther("10"), 0, 1);
        await carPooling.connect(user3).driverRegister();
        await carPooling.connect(user3).createRide(12, 2, ethers.parseEther("10"), 1, 2);
        // Check: User should be able to query rides with valid parameters
        await carPooling.findRides(0, 1).then((rideIds) => {
            expect(rideIds.length).to.equal(2);
            expect(rideIds[0]).to.equal(0);
            expect(rideIds[1]).to.equal(1);
        })
        await carPooling.findRides(0, 2).then((rideIds) => {
            expect(rideIds.length).to.equal(0);
        })
        await carPooling.findRides(1, 2).then((rideIds) => {
            expect(rideIds.length).to.equal(1);
            expect(rideIds[0]).to.equal(2);
        })
    });

    it("should allow passengers to join rides", async () => {
        // Requires correct implementation of createRide
        // Create a ride
        await carPooling.connect(user1).driverRegister();
        await carPooling.connect(user1).createRide(10, 2, ethers.parseEther("10"), 0, 1);
        // Register user as a passenger
        await expect(carPooling.connect(user2).joinRide(1)).to.be.reverted;
        await carPooling.connect(user2).passengerRegister();
        // Check: Registered passenger should not be able to join a ride with invalid parameters
        await expect(carPooling.connect(user2).joinRide(1)).to.be.reverted;
        await expect(carPooling.connect(user2).joinRide(0, {value: ethers.parseEther("9")})).to.be.reverted;
        // Check: Registered passenger should be able to join a ride with valid parameters and emit RideJoined event
        balanceBefore = await ethers.provider.getBalance(carPooling.getAddress());
        await expect(carPooling.connect(user2).joinRide(0, {value: ethers.parseEther("10")})).to.emit(carPooling, 'RideJoined').withArgs(0, user2.address);
        balanceAfter = await ethers.provider.getBalance(carPooling.getAddress());
        // Check: Joined ride should transfer funds to contract
        expect(balanceAfter).to.equal(balanceBefore + ethers.parseEther("10"));
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.passengerAddr.length).to.equal(1);
            expect(ride.passengerAddr[0]).to.equal(user2.address);
        });
        // Check: Full ride should change status to booking closed
        await carPooling.connect(user3).passengerRegister();
        expect(await carPooling.connect(user3).joinRide(0, {value: ethers.parseEther("10")})).to.emit(carPooling, 'RideJoined').withArgs(0, user3.address);
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.status).to.equal(1);
            expect(ride.passengerAddr.length).to.equal(2);
            expect(ride.passengerAddr[0]).to.equal(user2.address);
            expect(ride.passengerAddr[1]).to.equal(user3.address);
        });
        await carPooling.getPassenger(user2).then((passenger) => {
           expect(passenger.hasRide).to.be.true;
        });
        await carPooling.getPassenger(user3).then((passenger) => {
           expect(passenger.hasRide).to.be.true;
        });
        await expect(carPooling.connect(user2).joinRide(0)).to.be.reverted;
        await carPooling.connect(user4).passengerRegister();
        await expect(carPooling.connect(user4).joinRide(0)).to.be.reverted;
    });

    it("should allow drivers to start rides", async () => {
        // Requires correct implementation of createRide
        // Create a ride
        await carPooling.connect(user1).driverRegister();
        await carPooling.connect(user4).driverRegister();
        await carPooling.connect(user1).createRide(10, 2, ethers.parseEther("10"), 0, 1);

        await carPooling.connect(user2).passengerRegister();
        await carPooling.connect(user3).passengerRegister();

        await carPooling.connect(user2).joinRide(0, {value: ethers.parseEther("10")});
        await carPooling.connect(user3).joinRide(0, {value: ethers.parseEther("10")});

        await expect(carPooling.connect(user1).startRide(1)).to.be.reverted;
        await expect(carPooling.connect(user4).startRide(0)).to.be.reverted;
        await expect(carPooling.connect(user2).startRide(0)).to.be.reverted

        expect(await carPooling.connect(user1).startRide(0)).to.emit(carPooling, 'RideStarted').withArgs(0);
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.status).to.equal(2);
        });

        await expect(carPooling.connect(user1).startRide(0)).to.be.reverted;
    });

    it("should allow drivers to complete rides", async () => {
        // Requires correct implementation of createRide
        // Create a ride
        await carPooling.connect(user1).driverRegister();
        await carPooling.connect(user4).driverRegister();
        await carPooling.connect(user1).createRide(10, 2, ethers.parseEther("10"), 0, 1);

        await carPooling.connect(user2).passengerRegister();
        await carPooling.connect(user3).passengerRegister();
        await carPooling.connect(user5).passengerRegister();

        await carPooling.connect(user2).joinRide(0, {value: ethers.parseEther("10")});
        await carPooling.connect(user3).joinRide(0, {value: ethers.parseEther("10")});

        await expect(carPooling.connect(user1).completeRide(0)).to.be.reverted;

        expect(await carPooling.connect(user1).startRide(0)).to.emit(carPooling, 'RideStarted').withArgs(0);
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.status).to.equal(2);
        });

        await expect(carPooling.connect(user1).completeRide(1)).to.be.reverted;
        await expect(carPooling.connect(user4).completeRide(0)).to.be.reverted;
        await expect(carPooling.connect(user5).completeRide(0)).to.be.reverted;

        let contractBalanceBefore = await ethers.provider.getBalance(carPooling.getAddress());

        expect(await carPooling.connect(user1).completeRide(0)).to.emit(carPooling, 'RideCompleted').withArgs(0);
        await carPooling.getRideById(0).then((ride) => {
            expect(ride.status).to.equal(3);
        });

        let contractBalanceAfter = await ethers.provider.getBalance(carPooling.getAddress());
        expect(contractBalanceAfter).to.equal(contractBalanceBefore - ethers.parseEther("20"));

        await carPooling.getPassenger(user2.address).then((passenger) => {
            expect(passenger.isRegistered).to.be.true;
            expect(passenger.hasRide).to.be.false;
        });

        await carPooling.getDriver(user1.address).then((driver) => {
            expect(driver.isRegistered).to.be.true;
            expect(driver.hasRide).to.be.false;
        })
    });
});
