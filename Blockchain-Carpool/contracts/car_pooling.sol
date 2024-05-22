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
	enum RequestStatus {Requested, Fulfilled}

	struct Request {
		uint256 id;
		address addr;
		uint8 preferredTravelTime;
		Location origin;
		Location destination;
		RequestStatus status;
		uint256 pricePaid;
	}

	struct TravelPath {
		Location origin;
		Location destination;
	}

	struct Pair {
		uint256 rideId;
		uint256 requestId;
	}

	struct DPEntry {
		uint256 deviation;
		Pair[] pairs;
	}

	mapping(address => bool) internal passengerRequests;
	mapping(uint256 => Request) internal requests;

	uint256 internal nextRequestId = 0;

	function abs(int x) internal pure returns (uint) {
		return uint(x >= 0 ? x : -x);
	}

	function getRequest(address addr) public view returns (bool) {
		return passengerRequests[addr];
	}

	function findRequests(Location _origin, Location _destination) internal view returns (uint256[] memory) {
		uint256[] memory validRequests = new uint256[](nextRequestId);

		uint256 index = 0;

		for (uint256 i = 0; i < nextRequestId; i++) {
			Request storage r = requests[i];
			if (r.origin == _origin && r.destination == _destination && r.status != RequestStatus.Fulfilled) {
				validRequests[index] = r.id;
				index++;
			}
		}

		assembly {
			mstore(validRequests, index)
		}

		return validRequests;
	}

	function quickSortRequests(uint256[] memory arr, int left, int right) internal {
		int i = left;
		int j = right;

		if (i == j) return;

		uint pivot = requests[arr[uint(left + (right - left) / 2)]].preferredTravelTime;

		while (i <= j) {
			while (requests[arr[uint(i)]].preferredTravelTime < pivot) i++;
			while (pivot < requests[arr[uint(j)]].preferredTravelTime) j--;
			if (i <= j) {
				(arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
				i++;
				j--;
			}
		}

		if (left < j)
			quickSortRequests(arr, left, j);
		if (i < right)
			quickSortRequests(arr, i, right);
	}

	function awaitAssignRide(Location _source, Location _destination, uint8 preferredTravelTime) public payable onlyPassenger {
		require(msg.value > 0, "Insufficient payment amount!");
		require(preferredTravelTime >= 0 && preferredTravelTime <= 23, "Travel time must be between 0 and 23");
		require(_source != _destination, "Origin and Destination must not be the same");
		require(!passengerRequests[msg.sender], "You can only have one ride request at once!");

		requests[nextRequestId] = Request({
			id: nextRequestId,
			addr: msg.sender,
			preferredTravelTime: preferredTravelTime,
			origin: _source,
			destination: _destination,
			status: RequestStatus.Requested,
			pricePaid: msg.value
		});

		nextRequestId += 1;
		passengerRequests[msg.sender] = true;
	}

	function assignPassengersToRides() public {
		TravelPath[6] memory directions = [
			TravelPath(Location.A, Location.B),
			TravelPath(Location.A, Location.C),
			TravelPath(Location.B, Location.A),
			TravelPath(Location.B, Location.C),
			TravelPath(Location.C, Location.A),
			TravelPath(Location.C, Location.B)
		];

		for (uint256 i = 0; i < directions.length; i++) {
			uint256[] memory ridesForPath = findRides(directions[i].origin, directions[i].destination);

			if (ridesForPath.length == 0) {
				continue;
			}

			uint256[] memory requestsForPath = findRequests(directions[i].origin, directions[i].destination);

			if (requestsForPath.length == 0) {
				continue;
			}

			quickSortRides(ridesForPath, int(0), int(ridesForPath.length - 1));
			quickSortRequests(requestsForPath, int(0), int(requestsForPath.length - 1));

			Pair[] memory mappings = performAssignment(ridesForPath, requestsForPath);

			for (uint256 j = 0; j < mappings.length; j++) {
				address[] memory passengerArray = new address[](rides[mappings[j].rideId].passengerAddr.length + 1);

				for (uint256 k = 0; k < rides[mappings[j].rideId].passengerAddr.length; k++) {
					passengerArray[k] = rides[mappings[j].rideId].passengerAddr[k];
				}

				passengerArray[passengerArray.length - 1] = requests[mappings[j].requestId].addr;

				rides[mappings[j].rideId].passengerAddr = passengerArray;
				rides[mappings[j].rideId].availableSeats--;

				passengers[requests[mappings[j].requestId].addr].hasRide = true;
				passengerRequests[requests[mappings[j].requestId].addr] = false;

				if (rides[mappings[j].rideId].availableSeats == 0) {
					rides[mappings[j].rideId].status = RideStatus.FullyBooked;
				}

				requests[mappings[j].requestId].status = RequestStatus.Fulfilled;

				if (requests[mappings[j].requestId].pricePaid > rides[mappings[j].rideId].seatPrice) {
					uint256 amountToPay = requests[mappings[j].requestId].pricePaid - rides[mappings[j].rideId].seatPrice;
					payable(requests[mappings[j].requestId].addr).transfer(amountToPay);
				}

				emit RideJoined(mappings[j].rideId, requests[mappings[j].requestId].addr);
			}
		}

		for (uint256 i = 0; i < nextRequestId; i++) {
			if (requests[i].status != RequestStatus.Fulfilled) {
				payable(requests[i].addr).transfer(requests[i].pricePaid);
				requests[i].status = RequestStatus.Fulfilled;
			}
		}
	}

	function performAssignment(uint256[] memory ridesToAssign, uint256[] memory requestsToAssign) public view returns (Pair[] memory) {
		uint256 totalRideSpaces = 0;

		for (uint256 i = 0; i < ridesToAssign.length; i++) {
			totalRideSpaces += rides[ridesToAssign[i]].availableSeats;
		}

		uint256[] memory allRidesToAssign = new uint256[](totalRideSpaces);

		uint256 pos = 0;
		for (uint256 i = 0; i < ridesToAssign.length; i++) {
			for (uint256 j = 0; j < rides[ridesToAssign[i]].availableSeats; j++) {
				allRidesToAssign[pos] = ridesToAssign[i];
				pos += 1;
			}
		}

		if (requestsToAssign.length <= allRidesToAssign.length) {
			uint256 n = requestsToAssign.length;
			uint256 m = allRidesToAssign.length;

			DPEntry[][] memory dp = new DPEntry[][](m + 1);

			for (uint256 i = 0; i < m + 1; i++) {
				DPEntry[] memory r = new DPEntry[](n + 1);
				for (uint256 j = 0; j < n + 1; j++) {
					r[j] = DPEntry({
						deviation: 999999,
						pairs: new Pair[](0)
					});
				}
				dp[i] = r;
			}

			dp[0][0].deviation = 0;

			for (uint256 i = 0; i < m; i++) {
				for (uint256 j = 0; j < n + 1; j++) {
					dp[i + 1][j].deviation = dp[i][j].deviation;
					dp[i + 1][j].pairs = new Pair[](dp[i][j].pairs.length);

					for (uint256 k = 0; k < dp[i][j].pairs.length; k++) {
						dp[i + 1][j].pairs[k].rideId = dp[i][j].pairs[k].rideId;
						dp[i + 1][j].pairs[k].requestId = dp[i][j].pairs[k].requestId;
					}
				}

				for (uint256 j = 0; j < n; j++) {
					uint256 newDiff = dp[i][j].deviation + abs(int8(requests[requestsToAssign[j]].preferredTravelTime) - int8(rides[allRidesToAssign[i]].travelTime));

					if (newDiff < dp[i + 1][j + 1].deviation) {
						dp[i + 1][j + 1] = DPEntry({
							deviation: newDiff,
							pairs: new Pair[](dp[i][j].pairs.length + 1)
						});

						for (uint256 k = 0; k < dp[i][j].pairs.length; k++) {
							dp[i + 1][j + 1].pairs[k] = dp[i][j].pairs[k];
						}

						dp[i + 1][j + 1].pairs[dp[i][j].pairs.length] = Pair({
							rideId: allRidesToAssign[i],
							requestId: requestsToAssign[j]
						});
					}
				}
			}

			return dp[m][n].pairs;
		} else {
			uint256 n = allRidesToAssign.length;
			uint256 m = requestsToAssign.length;

			DPEntry[][] memory dp = new DPEntry[][](m + 1);

			for (uint256 i = 0; i < m + 1; i++) {
				DPEntry[] memory r = new DPEntry[](n + 1);
				for (uint256 j = 0; j < n + 1; j++) {
					r[j] = DPEntry({
						deviation: 999999,
						pairs: new Pair[](0)
					});
				}
				dp[i] = r;
			}

			dp[0][0].deviation = 0;

			for (uint256 i = 0; i < m; i++) {
				for (uint256 j = 0; j < n + 1; j++) {
					dp[i + 1][j].deviation = dp[i][j].deviation;
					dp[i + 1][j].pairs = new Pair[](dp[i][j].pairs.length);

					for (uint256 k = 0; k < dp[i][j].pairs.length; k++) {
						dp[i + 1][j].pairs[k].rideId = dp[i][j].pairs[k].rideId;
						dp[i + 1][j].pairs[k].requestId = dp[i][j].pairs[k].requestId;
					}
				}

				for (uint256 j = 0; j < n; j++) {
					uint256 newDiff = dp[i][j].deviation + abs(int8(requests[requestsToAssign[i]].preferredTravelTime) - int8(rides[allRidesToAssign[j]].travelTime));

					if (newDiff < dp[i + 1][j + 1].deviation) {
						dp[i + 1][j + 1] = DPEntry({
							deviation: newDiff,
							pairs: new Pair[](dp[i][j].pairs.length + 1)
						});

						for (uint256 k = 0; k < dp[i][j].pairs.length; k++) {
							dp[i + 1][j + 1].pairs[k] = dp[i][j].pairs[k];
						}

						dp[i + 1][j + 1].pairs[dp[i][j].pairs.length] = Pair({
							rideId: allRidesToAssign[j],
							requestId: requestsToAssign[i]
						});
					}
				}
			}

			return dp[m][n].pairs;
		}
	}
}
