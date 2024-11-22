pragma solidity ^0.8.0;

import { CryoPod } from "./CryoPod.sol";

contract Setup {
    CryoPod public immutable TARGET;
    bytes32 public flagHash = 0x0;

    event DeployedTarget(address at);

    constructor() payable {
        TARGET = new CryoPod();
        emit DeployedTarget(address(TARGET));
    }

    function isSolved(string calldata flag) public view returns (bool) {
        return keccak256(abi.encodePacked(flag)) == flagHash;
    }
}
