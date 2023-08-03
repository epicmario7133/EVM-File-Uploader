pragma solidity ^0.5.0;

contract SolidityTest {
string data = "";
address owner = msg.sender;

    function getValue() public view returns(string memory) {
        return  data;
    }
    function delateAll() public {
        require(tx.origin == owner, "Not the owner");

        data = "";
    }
    function SetOwner(address newowner) public {
        if(tx.origin == owner){
            owner = newowner;
        }
        else{
            revert("Not the owner");
        }
    }
    function GetOwner() public view returns (address) {
        return owner;
    }
}