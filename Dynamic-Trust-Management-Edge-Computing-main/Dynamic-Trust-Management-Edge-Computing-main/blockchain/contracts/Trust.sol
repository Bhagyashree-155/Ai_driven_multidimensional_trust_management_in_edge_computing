pragma solidity ^0.8.0;

contract Trust {
    mapping(string => uint) public scores;

    function update(string memory node, uint score) public {
        scores[node] = score;
    }

    function get(string memory node) public view returns(uint){
        return scores[node];
    }
}