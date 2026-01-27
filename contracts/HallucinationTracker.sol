// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HallucinationTracker {
    event LogEntry(uint256 indexed queryHash, uint8 score, uint256 timestamp, string modelVersion);
    
    function logSingle(uint256 queryHash, uint8 score, string calldata modelVersion) external {
        emit LogEntry(queryHash, score, block.timestamp, modelVersion);
    }
    
    function logBatch(uint256[] calldata queryHashes, uint8[] calldata scores, string[] calldata modelVersions) external {
        require(queryHashes.length == scores.length && scores.length == modelVersions.length, "Array length mismatch");
        for (uint i = 0; i < queryHashes.length; i++) {
            emit LogEntry(queryHashes[i], scores[i], block.timestamp, modelVersions[i]);
        }
    }
}