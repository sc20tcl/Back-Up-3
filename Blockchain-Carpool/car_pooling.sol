// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CarPooling {

    enum RideStatus {BookingOpen, FullyBooked, Started, Completed}
    enum Location {A, B, C}

    struct Ride {
        uint256 rideId;
        address driver;
        uint8 travelTime;
        uint8 availableSeats;
        uint8 totalSeats;
        uint256 seatPrice;
        Location origin;
        Location destination;
        RideStatus status; // status of the ride
        address [] passengerAddr; // addresses of all passengers who booked the ride
    }

    struct Driver {
        bool isRegistered;
        bool hasRide;
    }

    struct Passenger {
        bool isRegistered;
        bool hasRide;
    }

    mapping(uint256 => Ride) internal rides;
    mapping(address => Driver) internal drivers;
    mapping(address => Passenger) internal passengers; 

    // Your auxiliary data structures here, if required
    uint256 public rideCount;

    event RideCreated(uint256 rideId, address driver, uint8 travelTime, uint8 availableSeats, uint256 seatPrice, Location origin, Location destination);
    event RideJoined(uint256 rideId, address passenger);
    event RideStarted(uint256 rideId);
    event RideCompleted(uint256 rideId);

    modifier onlyDriver() {
        require(drivers[msg.sender].isRegistered, "Not a registered driver");
        _;
    }

    modifier onlyPassenger(){
        require(passengers[msg.sender].isRegistered, "Not a registered passenger");
        _;
    }
    modifier notDriver(){
       require(!drivers[msg.sender].isRegistered, "A registered driver");
        _;
    }
    modifier notPassenger(){
        require(!passengers[msg.sender].isRegistered, "A registered driver");
        _;
    }
    modifier driverSingleRide(){
        require(!drivers[msg.sender].hasRide, "Driver doesn't have a ride");
        _;
    }
    modifier passengerSingleRide(){
        require(passengers[msg.sender].isRegistered, "Passenger doesn't have a ride");
        _;
    }

   function passengerRegister() public notPassenger {
        passengers[msg.sender] = Passenger({isRegistered: true, hasRide: false});
    }

     function driverRegister() public notDriver{
        drivers[msg.sender] = Driver({isRegistered: true, hasRide: false});
    }

    function createRide(uint8 _travelTime, uint8 _availableSeats, uint256 _seatPrice, Location _origin, Location _destination) public onlyDriver driverSingleRide{
        require(_availableSeats > 0, "You must atleast one seat availible");
        require(_seatPrice > 0, "You must charge for your seat");
        require(_destination != _origin, "You must travel to a different location");
        require(_travelTime < 24 && _travelTime >= 0, "You must travel to a different location");


        uint256 newRideId = rideCount++; 
        rides[newRideId] = Ride({rideId: newRideId, driver: msg.sender, travelTime: _travelTime, availableSeats: _availableSeats, totalSeats: _availableSeats, seatPrice: _seatPrice, origin: _origin, destination: _destination, status: RideStatus.BookingOpen,
            passengerAddr: new address[](0)
        });
        drivers[msg.sender].hasRide = true;
        emit RideCreated(newRideId, msg.sender, _travelTime, _availableSeats, _seatPrice, _origin, _destination);
        
    }

    function findRides(Location _source, Location _destination) public view returns (uint256[] memory) {
        uint256[] memory rideList = new uint256[](rideCount);
        uint256 ridesFound = 0;

        for (uint256 i = 0; i < rideCount; i++) {
            if (compareLocations(rides[i].origin, _source) && compareLocations(rides[i].destination, _destination)) {
                rideList[ridesFound] = rides[i].rideId;
                ridesFound++;
            }
        }

        uint256[] memory matchedRides = new uint256[](ridesFound);
        for (uint256 j = 0; j < ridesFound; j++) {
            matchedRides[j] = rideList[j];
        }

        return matchedRides;
    }

    function compareLocations(Location loc1, Location loc2) private pure returns (bool) {
        return (keccak256(abi.encodePacked(loc1)) == keccak256(abi.encodePacked(loc2)));
    }

    function joinRide(uint256 _rideId) public payable onlyPassenger passengerSingleRide{
        Ride storage ride = rides[_rideId];
        require(ride.availableSeats > 0, "No seats available");
        ride.passengerAddr.push(msg.sender); 
        ride.availableSeats -= 1;

        require(msg.value == ride.seatPrice, "Incorrect amount of Ether sent");

        if (ride.availableSeats == 0){
            ride.status = RideStatus.FullyBooked;
        }
        emit RideJoined(_rideId, msg.sender);
        passengers[msg.sender].hasRide = true;
    }

    function startRide(uint256 _rideId) public onlyDriver{
        Ride storage ride = rides[_rideId];
        require(ride.driver == msg.sender, "only the driver can start their own ride");

        require(ride.status == RideStatus.BookingOpen || ride.status == RideStatus.FullyBooked, "only start a ride that is open");
        
        ride.status = RideStatus.Started;
        emit RideStarted(_rideId);
    }

    function completeRide(uint256 _rideId) public onlyDriver{
        require(msg.sender == rides[_rideId].driver, "only the driver can end their own ride");
        require(rides[_rideId].status == RideStatus.Started, "only end a ride that has started");
        Ride storage ride = rides[_rideId];
        ride.status = RideStatus.Completed;

        uint256 totalPayment = ride.seatPrice * (ride.totalSeats - ride.availableSeats);

        (bool sent, ) = payable(msg.sender). call{value: totalPayment} ("");
        require(sent, "Failed to send Ether to the driver");

        emit RideCompleted(_rideId);
        drivers[ride.driver].hasRide = false;
        for (uint256 passenger = 0; passenger < (ride.totalSeats - ride.availableSeats); passenger++){
            passengers[ride.passengerAddr[passenger]].hasRide = false;
        }
    }

    // -------------------- Already implemented functions, do not modify ------------------

    function getDriver(address addr) public view returns (Driver memory){
        return(drivers[addr]);
    }

    function getPassenger(address addr) public view returns (Passenger memory){
        return(passengers[addr]);
    }

    function getRideById(uint256 _rideId) public view returns (Ride memory){
        return(rides[_rideId]);
    }
}

// ----------------------------------- Coordination -----------------------------------

contract CarPoolingCoordination is CarPooling {
    
    struct AwaitingRide {
        uint256 aRideId;
        uint8 pTravelTime;
        uint256 depositValue;
        Location origin;
        Location destination;
        address passengerAddr; 
    }

    struct tempRide {
        uint256 rideId;
        address[] passengers;
    }

    struct Pairing {
        uint256 rideId;
        uint256 aRideId;

        uint deviation;
    }

    uint256 public awaitingRideCount;

    mapping(uint256 => AwaitingRide) internal awaitingRides;
    mapping(address => bool) internal alreadyReq;
    mapping(uint256 => Pairing) public optimalPairList;
    uint256 public optimalPairCount;
    mapping(uint256 => bool) public assignedRiders;
    

    function awaitAssignRide(Location _source, Location _destination, uint8 preferredTravelTime) public payable onlyPassenger {
        require(_destination != _source, "You must travel to a different location");
        require(preferredTravelTime < 24 && preferredTravelTime >= 0, "You must travel to a different location");
        require(!alreadyReq[msg.sender], "you cannot request three rides");
        require(msg.value > 0, "You need to make a deposit");
        uint256 newRideId = awaitingRideCount++; 
        awaitingRides[newRideId] = AwaitingRide({aRideId: newRideId, pTravelTime: preferredTravelTime, depositValue: msg.value, origin: _source, destination: _destination, passengerAddr: msg.sender});
        awaitingRideCount++;

        alreadyReq[msg.sender] = true;
    }

    function assignPassengersToRides() public {
        // createOptimalPairs();
        // actionOptimalPairs();
    }

    function createOptimalPairs() public {
        // Iterate over all combinations of locations, excluding same-origin-destination pairs
        for (uint i = 0; i < uint(Location.C); i++) {
            for (uint j = 0; j < uint(Location.C); j++) {
                if (i != j) {
                    Location origin = Location(i);
                    Location destination = Location(j);

                    // Retrieve and sort lists of rides and passengers
                    uint256[] memory sortedRides = getAndSortRides(origin, destination);

                    uint256[] memory sortedPassengers = getAndSortPassengers(origin, destination);

                    // Find optimal pairings
                    // uint256[] memory optimalPairs = findOptimalPairings(sortedRides, sortedPassengers);

                    // Add all optimal pairs to the main list
                    // for (uint k = 0; k < optimalPairs.length; k++) {
                    //     optimalPairList[optimalPairCount] = optimalPairs[k];
                    //     optimalPairCount ++;
                    //     assignedRiders[optimalPairs[k].aRideId] = true;
                    //     optimalPairCount ++;
                    // }
                }
            }
        }
    }

    function actionOptimalPairs() public{
        for (uint256 pair = 0; pair < optimalPairCount; pair++){
            Ride storage ride = rides[optimalPairList[pair].rideId];
            AwaitingRide storage aPassenger = awaitingRides[optimalPairList[pair].aRideId];

            passengers[aPassenger.passengerAddr] = Passenger({isRegistered: true, hasRide: true});

            ride.availableSeats -= 1;

            if (ride.availableSeats == 0){
                ride.status = RideStatus.FullyBooked;
            }
            emit RideJoined(ride.rideId, aPassenger.passengerAddr);
            uint256 refundValue = ride.seatPrice - aPassenger.depositValue;
            (bool sent, ) = payable(ride.driver). call{value: refundValue} ("");
            require(sent, "Failed to refund Ether to the Passenger");
        }

        for (uint rider = 0; rider < awaitingRideCount; rider++) {
            if (!assignedRiders[awaitingRides[rider].aRideId]){
                (bool sent, ) = payable(awaitingRides[rider].passengerAddr). call{value: awaitingRides[rider].depositValue} ("");
                require(sent, "Failed to refund Ether to the Passenger");
            }
        }
    }


    // Function to find optimal pairings
   function findOptimalPairings(uint[] memory sortedRideIds, uint[] memory sortedAwaitingRideIds) 
        public view returns (uint[] memory, uint)
    {
        uint numRides = sortedRideIds.length;
        uint numAwaiting = sortedAwaitingRideIds.length;
        uint[] memory bestPairing = new uint[](2 * numRides);
        uint minimalDeviation = type(uint).max;

        // Brute force all possible permutations of pairings
        for (uint i = 0; i < (1 << numAwaiting); i++) {
            uint[] memory currentPairing = new uint[](2 * numRides);
            uint currentDeviation = 0;
            uint pairIndex = 0;

            // Attempt to create a valid pairing by treating i as a bitmask
            for (uint j = 0; j < numAwaiting && pairIndex < numRides; j++) {
                if (i & (1 << j) != 0) {
                    currentPairing[2 * pairIndex] = sortedRideIds[pairIndex]; // Ride index
                    currentPairing[2 * pairIndex + 1] = sortedAwaitingRideIds[j]; // Awaiting Ride index

                    // Calculate deviation for this pairing
                    currentDeviation += absDifference(
                        rides[sortedRideIds[pairIndex]].travelTime,
                        awaitingRides[sortedAwaitingRideIds[j]].pTravelTime
                    );
                    pairIndex++;
                }
            }

            // Only consider this permutation if all rides are paired
            if (pairIndex == numRides && currentDeviation < minimalDeviation) {
                minimalDeviation = currentDeviation;
                bestPairing = currentPairing;
            }
        }

        return (bestPairing, minimalDeviation);
    }

    function absDifference(uint8 time1, uint8 time2) private pure returns (uint) {
        if (time1 > time2) {
            return time1 - time2;
        } else {
            return time2 - time1;
        }
    }


    function getAndSortRides(Location origin, Location destination) private view returns (uint256[] memory) {
        uint256[] memory tempRideIds = new uint256[](rideCount);
        uint count = 0;

        for (uint256 i = 0; i < rideCount; i++) {
            if (rides[i].origin == origin && rides[i].destination == destination) {
                for (uint256 seats = 0; seats < rides[i].availableSeats; seats++)
                    tempRideIds[count] = i;
                    count++;
            }
        }

        uint256[] memory filteredRideIds = new uint256[](count);
        for (uint256 j = 0; j < count; j++) {
            filteredRideIds[j] = tempRideIds[j];
        }

        return sortArray(filteredRideIds, 1); 
    }

    function getAndSortPassengers(Location origin, Location destination) private view returns (uint256[] memory) {
        uint256[] memory tempRideIds = new uint256[](awaitingRideCount);
        uint count = 0;

        for (uint256 i = 0; i < rideCount; i++) {
            if (awaitingRides[i].origin == origin && awaitingRides[i].destination == destination) {
                tempRideIds[count] = i;
                count++;
            }
        }

        uint256[] memory filteredPassengerIds = new uint256[](count);
        for (uint256 j = 0; j < count; j++) {
            filteredPassengerIds[j] = tempRideIds[j];
        }
        return sortArray(filteredPassengerIds, 1); 
    }

    function partitionPassenger(uint[] memory arr, int low, int high) internal view returns (int) {
        uint pivotIndex = arr[uint(high)];
        AwaitingRide storage pivot = awaitingRides[pivotIndex];
        int i = low - 1;

        for (int j = low; j <= high - 1; j++) {
            AwaitingRide storage currentRide = awaitingRides[arr[uint(j)]];
            if (currentRide.pTravelTime < pivot.pTravelTime) {
                i++;
                // Swap arr[i] and arr[j]
                (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
            }
        }
        // Swap arr[i + 1] and arr[high] (or pivot)
        (arr[uint(i + 1)], arr[uint(high)]) = (arr[uint(high)], arr[uint(i + 1)]);
        return i + 1;
    }

    function partitionRide(uint[] memory arr, int low, int high) internal view returns (int) {
        uint pivotIndex = arr[uint(high)];
        Ride storage pivot = rides[pivotIndex];
        int i = low - 1;

        for (int j = low; j <= high - 1; j++) {
            Ride storage currentRide = rides[arr[uint(j)]];
            if (currentRide.travelTime < pivot.travelTime) {
                i++;
                // Swap arr[i] and arr[j]
                (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
            }
        }
        // Swap arr[i + 1] and arr[high] (or pivot)
        (arr[uint(i + 1)], arr[uint(high)]) = (arr[uint(high)], arr[uint(i + 1)]);
        return i + 1;
    }

    function quickSort(uint[] memory arr, int low, int high, int typeCode) internal view {
        if (low < high) {
            if (typeCode == 1){
                int pi = partitionRide(arr, low, high);
                quickSort(arr, low, pi - 1, 1);
                quickSort(arr, pi + 1, high, 1);
            }
            else {
                int pi = partitionPassenger(arr, low, high);
                quickSort(arr, low, pi - 1, 0);
                quickSort(arr, pi + 1, high, 0);
            }
        }
    }

    function sortArray(uint[] memory arr, int typeCode) public view returns (uint[] memory) {
        if (arr.length > 0){
            quickSort(arr, 0, int(arr.length - 1), typeCode);
        }
        return arr;
    }

}