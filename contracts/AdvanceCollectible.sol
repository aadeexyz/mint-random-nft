// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvanceCollectible is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    enum Shape {
        CIRCLE,
        SQUARE,
        RECTANGLE
    }
    mapping(uint256 => Shape) public tokenIdToShape;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event shapeAssigned(uint256 indexed tokenId, Shape shape);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Shape", "SHP")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomNumber)
        internal
        override
    {
        Shape shape = Shape(_randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToShape[newTokenId] = shape;
        emit shapeAssigned(newTokenId, shape);
        address sender = requestIdToSender[_requestId];
        _safeMint(sender, newTokenId);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 _tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), _tokenId),
            "ERC721 caller is neither owner nor approved"
        );
        _setTokenURI(_tokenId, _tokenURI);
    }
}
