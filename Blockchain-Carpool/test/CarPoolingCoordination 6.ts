import { expect } from "chai";
import { ethers } from "hardhat";
import { HardhatEthersSigner } from "@nomicfoundation/hardhat-ethers/signers";
import { CarPoolingCoordination } from "../typechain-types";

describe("CarPoolingCoordination", () => {
	let carPoolingCoordination: CarPoolingCoordination;
	let user1: HardhatEthersSigner;
	let user2: HardhatEthersSigner;
	let user3: HardhatEthersSigner;
	let user4: HardhatEthersSigner;
	let user5: HardhatEthersSigner;
	let user6: HardhatEthersSigner;
	let user7: HardhatEthersSigner;
	let user8: HardhatEthersSigner;

	beforeEach(async () => {
		const CarPoolingCoordination = await ethers.getContractFactory("CarPoolingCoordination");
		[user1, user2, user3, user4, user5, user6, user7, user8] = await ethers.getSigners();

		carPoolingCoordination = await CarPoolingCoordination.deploy();
	});

	it("should allow passengers to await a ride assignment", async () => {
		await expect(carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")})).to.be.reverted;

		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();

		await expect(carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 1)).to.be.reverted;
		await expect(carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 24, {value: ethers.parseEther("10")})).to.be.reverted;
		await expect(carPoolingCoordination.connect(user1).awaitAssignRide(1, 1, 1, {value: ethers.parseEther("10")})).to.be.reverted;

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("10")});

		await expect(carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")})).to.be.reverted;

	});

	it("should perform assignment to correct rides", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(4, 3, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(9, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user1).findOptimalPairings([0, 0, 0, 1], [0, 1, 3, 2]).then((result) => {
			console.log(result);
		});
	});

	it("should perform assignment to correct rides 2", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 10, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(8, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(14, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user1).findOptimalPairings([0, 1], [1, 0]).then((result) => {
			console.log(result);
		});
	});

	it("should perform assignment to correct rides 3", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(16, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(14, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user1).findOptimalPairings([1, 0], [0]).then((result) => {
			console.log(result);
		});
	});

	it("should perform assignment to correct rides 4", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 15, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 10, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(16, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(14, 1, ethers.parseEther("10"), 0, 1);


		// await carPoolingCoordination.connect(user1).sortArray([0, 1, 2], 1).then((result) => {
		// 	console.log("order of passengers", result);
		// });

		// await carPoolingCoordination.connect(user1).sortArray([0, 1], 0).then((result) => {
		// 	console.log("order of rides", result);
		// });

		
		await carPoolingCoordination.connect(user1).findOptimalPairings([1, 0], [1, 2, 0]).then((result) => {
			console.log("order of optimum pairs ", result);
		});

	});

	it("should correctly sort an array of ride indices by travel time", async function () {
        await carPoolingCoordination.connect(user5).driverRegister();
        await carPoolingCoordination.connect(user6).driverRegister();
        await carPoolingCoordination.connect(user7).driverRegister();

        // Create rides with varied travel times
        await carPoolingCoordination.connect(user5).createRide(12, 3, ethers.parseEther("10"), 0, 1);
        await carPoolingCoordination.connect(user6).createRide(5, 3, ethers.parseEther("10"), 0, 1);
        await carPoolingCoordination.connect(user7).createRide(8, 3, ethers.parseEther("10"), 0, 1);

        // Expected order by travel times: [5, 8, 12]
        let rideIds = [0, 1, 2];  // Assume these indices correspond to the order rides were created

        // Act: Sort the rides
        let sortedRideIds = await carPoolingCoordination.sortArray(rideIds, 1); // typeCode 1 for rides

        // Assert: Check if the rides are sorted by travel time
        expect(sortedRideIds[0]).to.equal(1); // travel time 5
        expect(sortedRideIds[1]).to.equal(2); // travel time 8
        expect(sortedRideIds[2]).to.equal(0); // travel time 12
    });

    it("should handle an empty array without error", async function () {
        let emptyArray = [];

        // Act & Assert: Should not throw an error
        await expect(carPoolingCoordination.sortArray(emptyArray, 1))
            .to.not.be.reverted;
    });

    it("should maintain the order of an already sorted array", async function () {
        await carPoolingCoordination.connect(user5).driverRegister();
        await carPoolingCoordination.connect(user6).driverRegister();

        // Create already sorted rides by travel time
        await carPoolingCoordination.connect(user5).createRide(10, 3, ethers.parseEther("10"), 0, 1);
        await carPoolingCoordination.connect(user6).createRide(15, 3, ethers.parseEther("10"), 0, 1);

        let rideIds = [0, 1];  // Indices correspond to the order rides were created

        // Act: Sort the rides
        let sortedRideIds = await carPoolingCoordination.sortArray(rideIds, 1); // typeCode 1 for rides

        // Assert: The order should remain the same
        expect(sortedRideIds[0]).to.equal(0);
        expect(sortedRideIds[1]).to.equal(1);
    });

    it("should correctly sort reverse ordered arrays", async function () {
        await carPoolingCoordination.connect(user5).driverRegister();
        await carPoolingCoordination.connect(user6).driverRegister();

        // Create rides in reverse order by travel time
        await carPoolingCoordination.connect(user6).createRide(20, 3, ethers.parseEther("10"), 0, 1);
        await carPoolingCoordination.connect(user5).createRide(5, 3, ethers.parseEther("10"), 0, 1);

        let rideIds = [0, 1];  // Indices are reversed

        // Act: Sort the rides
        let sortedRideIds = await carPoolingCoordination.sortArray(rideIds, 1); // typeCode 1 for rides

        // Assert: The array should be sorted in ascending order
        expect(sortedRideIds[0]).to.equal(1); // travel time 5
        expect(sortedRideIds[1]).to.equal(0); // travel time 20
    });

	it("should correctly create optimal pairs and update state variables", async () => {
		// Register users and set up the rides
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
	
		// Setup rides and awaiting passengers
		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("15")});
		await carPoolingCoordination.connect(user5).createRide(4, 3, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(9, 1, ethers.parseEther("10"), 0, 1);
	
		// Execute the function that creates optimal pairs
		await carPoolingCoordination.createOptimalPairs();
	
		// Fetch the state of optimalPairList and optimalPairCount
		const pairCount = await carPoolingCoordination.optimalPairCount();
	
		// Assuming you can fetch optimalPairList entries if your contract allows it
		for (let i = 0; i < pairCount; i++) {
			const pair = await carPoolingCoordination.optimalPairList(i);
			console.log(`Pair ${i}: Ride ID = ${pair.rideId}, Awaiting Ride ID = ${pair.aRideId}`);
		}
	
		// Expectations: Check if the optimal pairs are as expected
		expect(pairCount).to.be.greaterThan(0);  // Expecting that some pairs have been created
	
		// Additional assertions can check for specific expected pairings
		// These will depend on the logic within `findOptimalPairings` and the setup of the test data
	});

	it("should assign passengers to rides (full test)", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
		await carPoolingCoordination.connect(user7).passengerRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("15")});
		await carPoolingCoordination.connect(user7).awaitAssignRide(0, 1, 23, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(4, 3, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(9, 1, ethers.parseEther("10"), 0, 1);

		let balanceBefore7 = await ethers.provider.getBalance(user7.getAddress());

		console.log("USER 4 BEFORE", ethers.formatEther(await ethers.provider.getBalance(user4.getAddress())));

		const response = await carPoolingCoordination.connect(user2).assignPassengersToRides();
		const receipt = await response.wait();

		console.log("GAS USED: ", receipt?.gasUsed);

		let balanceAfter7 = await ethers.provider.getBalance(user7.getAddress());
		let balanceBefore1 = await ethers.provider.getBalance(user1.getAddress());

		await carPoolingCoordination.connect(user2).getRideById(0).then((ride) => {
			console.log(`Number of passengers: ${ride.passengerAddr.length}`);
			ride.passengerAddr.forEach((addr, index) => {
				console.log(`Passenger ${index}: ${addr}`);
			});
		
			// Then perform assertions
			expect(ride.passengerAddr.length).to.be.at.least(3);
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[2]).to.equal(user1.address);
			expect(ride.passengerAddr[1]).to.equal(user2.address);
			expect(ride.passengerAddr[0]).to.equal(user4.address);
		});

		let balanceAfter1 = await ethers.provider.getBalance(user1.getAddress());

		console.log("USER 4 AFTER ", ethers.formatEther(await ethers.provider.getBalance(user4.getAddress())));

		expect(balanceBefore7).to.equal(balanceAfter7 - ethers.parseEther("10"));
		expect(balanceAfter1).to.equal(balanceBefore1);
	});

	it("should action step xxxxxxxxxxxxxxx ", async () => {
		// Register users and assign rides
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
		await carPoolingCoordination.connect(user7).passengerRegister();
	
		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("15")});
		await carPoolingCoordination.connect(user7).awaitAssignRide(0, 1, 23, {value: ethers.parseEther("10")});
	
		await carPoolingCoordination.connect(user5).createRide(4, 3, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(9, 1, ethers.parseEther("10"), 0, 1);
	
		// Create optimal pairs manually for testing or assume it's already correctly populated
		// Normally you would call createOptimalPairs here if the pairs are not set by default
		// For example, if that function is already tested and known to work as expected:
		await carPoolingCoordination.createOptimalPairs();
		const pairCount = await carPoolingCoordination.optimalPairCount();
    	for (let i = 0; i < pairCount; i++) {
			const pair = await carPoolingCoordination.optimalPairList(i);
			console.log(`Pair ${i}: Ride ID = ${pair.rideId}, Awaiting Ride ID = ${pair.aRideId}`);
		}
	
		// Now execute the function that actions the optimal pairs
		await carPoolingCoordination.actionOptimalPairs();
	
		// Check results
		// Check if passengers have been assigned correctly, seats decremented, and statuses updated
		const ride1 = await carPoolingCoordination.getRideById(0);
		expect(ride1.availableSeats).to.equal(2);  // Assuming starting with 3 seats
		expect(ride1.status).to.equal(0);  // Assuming status enum where 0 is open and 1 is fully booked
	
		const ride2 = await carPoolingCoordination.getRideById(1);
		expect(ride2.availableSeats).to.equal(0);
		expect(ride2.status).to.equal(1);  // Ride fully booked
	
		// Check refunds
		// Note: checking Ether transactions involves examining event logs or balance changes
		// Example: Check if balance of the driver has increased by the seat price times number of passengers
		// Optionally check for events emitted, like RideJoined or refunds
		// This part of testing may require setup to capture and examine transaction receipts
	
		// Example to check the balance change if needed (simplified)
		// const initialBalance = ethers.BigNumber.from(await ethers.provider.getBalance(user6.getAddress()));
		// const expectedRefund = ethers.utils.parseEther("0.5");  // Example value, adjust as necessary
		// const finalBalance = ethers.BigNumber.from(await ethers.provider.getBalance(user6.getAddress()));
		// expect(finalBalance).to.equal(initialBalance.add(expectedRefund));
	
		// Ensure no rides have pending passengers incorrectly
		for (let i = 0; i < 7; i++) { // Assuming 7 is the number of passengers
			const passengerStatus = await carPoolingCoordination.getPassenger(await carPoolingCoordination.optimalPairList(i).aRideId);
			expect(passengerStatus.hasRide).to.be.true;
		}
	});
	

	it("should assign passengers to rides (full test 2)", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).passengerRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
		await carPoolingCoordination.connect(user7).driverRegister();
		await carPoolingCoordination.connect(user8).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(1, 0, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(2, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(2, 1, 8, {value: ethers.parseEther("15")});
		await carPoolingCoordination.connect(user5).awaitAssignRide(0, 1, 23, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user6).createRide(4, 3, ethers.parseEther("10"), 2, 1);
		await carPoolingCoordination.connect(user7).createRide(9, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user8).createRide(10, 1, ethers.parseEther("10"), 1, 0);

		await carPoolingCoordination.assignPassengersToRides();

		await carPoolingCoordination.getRideById(0).then((ride) => {
			expect(ride.status).to.equal(0);
			expect(ride.availableSeats).to.equal(1);
			expect(ride.passengerAddr[1]).to.equal(user4.address);
			expect(ride.passengerAddr[0]).to.equal(user3.address);
		});

		await carPoolingCoordination.getRideById(1).then((ride) => {
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[0]).to.equal(user1.address);
		});

		await carPoolingCoordination.getRideById(2).then((ride) => {
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[0]).to.equal(user2.address);
		});
	});

	it("should assign passengers to rides 2", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
		await carPoolingCoordination.connect(user7).driverRegister();
		await carPoolingCoordination.connect(user8).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 4, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 9, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 4, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 4, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(14, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(8, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user7).createRide(6, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user8).createRide(7, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user2).assignPassengersToRides();
		await carPoolingCoordination.connect(user2).getRideById(0).then((ride) => {
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[0]).to.equal(user2.address);
		});
	});

	it("should assign passengers to rides 3", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();
		await carPoolingCoordination.connect(user7).driverRegister();
		await carPoolingCoordination.connect(user8).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(4, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user6).createRide(4, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user7).createRide(9, 1, ethers.parseEther("10"), 0, 1);
		await carPoolingCoordination.connect(user8).createRide(4, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user2).assignPassengersToRides();
		await carPoolingCoordination.connect(user2).getRideById(2).then((ride) => {
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[0]).to.equal(user3.address);
		});
	});

	it("should assign passengers to rides 4", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user5).createRide(4, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user2).assignPassengersToRides();
		await carPoolingCoordination.connect(user2).getRideById(0).then((ride) => {
			expect(ride.status).to.equal(1);
			expect(ride.availableSeats).to.equal(0);
			expect(ride.passengerAddr[0]).to.equal(user1.address);
		});
	});

	it("should perform assignment to correct rides", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();

		await carPoolingCoordination.connect(user5).createRide(4, 1, ethers.parseEther("10"), 0, 1);

		await carPoolingCoordination.connect(user2).assignPassengersToRides();
		await carPoolingCoordination.connect(user2).getRideById(0).then((ride) => {
			expect(ride.status).to.equal(0);
			expect(ride.availableSeats).to.equal(1);
		});
	});

	it("should assign passengers to rides (wrong direction)", async () => {
		await carPoolingCoordination.connect(user1).passengerRegister();
		await carPoolingCoordination.connect(user2).passengerRegister();
		await carPoolingCoordination.connect(user3).passengerRegister();
		await carPoolingCoordination.connect(user4).passengerRegister();
		await carPoolingCoordination.connect(user5).driverRegister();
		await carPoolingCoordination.connect(user6).driverRegister();

		await carPoolingCoordination.connect(user1).awaitAssignRide(0, 1, 6, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user2).awaitAssignRide(0, 1, 7, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user3).awaitAssignRide(0, 1, 14, {value: ethers.parseEther("10")});
		await carPoolingCoordination.connect(user4).awaitAssignRide(0, 1, 8, {value: ethers.parseEther("10")});

		await carPoolingCoordination.connect(user5).createRide(4, 3, ethers.parseEther("10"), 1, 0);
		await carPoolingCoordination.connect(user6).createRide(9, 1, ethers.parseEther("10"), 2, 1);

		await carPoolingCoordination.connect(user2).assignPassengersToRides();
		await carPoolingCoordination.connect(user2).getRideById(0).then((ride) => {
			expect(ride.status).to.equal(0);
			expect(ride.availableSeats).to.equal(3);
		});
		await carPoolingCoordination.connect(user2).getRideById(1).then((ride) => {
			expect(ride.status).to.equal(0);
			expect(ride.availableSeats).to.equal(1);
		});
	});
});
