// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SnippetRegistry {
    struct Snippet {
        bytes32 hash;
        string ipfsCID;
        uint256 trustScore;
        uint256 timestamp;
        address submitter;
    }

    mapping(bytes32 => Snippet) private snippets;
    event SnippetSubmitted(bytes32 indexed hash, string ipfsCID, uint256 trustScore, address indexed submitter);

    function submitSnippet(bytes32 _hash, string memory _ipfsCID, uint256 _trustScore) public {
        require(snippets[_hash].timestamp == 0, "Snippet already exists");
        snippets[_hash] = Snippet(_hash, _ipfsCID, _trustScore, block.timestamp, msg.sender);
        emit SnippetSubmitted(_hash, _ipfsCID, _trustScore, msg.sender);
    }

    function getSnippet(bytes32 _hash) public view returns (bytes32, string memory, uint256, uint256, address) {
        Snippet memory s = snippets[_hash];
        return (s.hash, s.ipfsCID, s.trustScore, s.timestamp, s.submitter);
    }

    function exists(bytes32 _hash) public view returns (bool) {
        return snippets[_hash].timestamp != 0;
    }
}
