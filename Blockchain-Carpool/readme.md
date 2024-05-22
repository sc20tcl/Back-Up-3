## Description of the proposed coordination mechanism implemented in the assignPassengersToRides() function (no more than 200 words):
n/a

## Do you use any additional contract variables? If so, what is the purpose of each variable? (no more than 200 words):
rideCount - is a variable to track the total number of rides in the "rides" map
awaitingRideCount - number of rides in awaiting ride map

 optimalPairList;
    uint256 public optimalPairCount;
    mapping(uint256 => bool) public assignedRiders;

## Do you use any additional data structures (structs)? If so, what is the purpose of each structure? (no more than 200 words):
awaitingRides - a struct to contain all of the 
alreadyReq - a boolean map to represent each request having being made so that a user can't submit a request twice

## Do you use any additional contract functions? If so, what is the purpose of each function? (no more than 200 words):
n/a

## Did you implement any additional test cases to test your smart contract? If so, what are these tests?
yes extra test cases to ensure an awaiting rider can't submit twice. A driver can only alter their own ride struct. A ride cannot have no value. A ride cannot travel to its origin destination.