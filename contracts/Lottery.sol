// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

library TransferHelper {
    function safeApprove(address token, address to, uint value) internal {
        // bytes4(keccak256(bytes('approve(address,uint256)')));
        (bool success, bytes memory data) = token.call(abi.encodeWithSelector(0x095ea7b3, to, value));
        require(success && (data.length == 0 || abi.decode(data, (bool))), "TransferHelper: APPROVE_FAILED");
    }

    function safeTransfer(address token, address to, uint value) internal {
        // bytes4(keccak256(bytes('transfer(address,uint256)')));
        (bool success, bytes memory data) = token.call(abi.encodeWithSelector(0xa9059cbb, to, value));
        require(success && (data.length == 0 || abi.decode(data, (bool))), "TransferHelper: TRANSFER_FAILED");
    }

    function safeTransferFrom(address token, address from, address to, uint value) internal {
        // bytes4(keccak256(bytes('transferFrom(address,address,uint256)')));
        (bool success, bytes memory data) = token.call(abi.encodeWithSelector(0x23b872dd, from, to, value));
        require(success && (data.length == 0 || abi.decode(data, (bool))), "TransferHelper: TRANSFER_FROM_FAILED");
    }

    function safeTransferETH(address to, uint value) internal {
        (bool success,) = to.call{value:value}(new bytes(0));
        require(success, "TransferHelper: ETH_TRANSFER_FAILED");
    }
}

contract Lottery is VRFConsumerBase, Ownable, ReentrancyGuard{

  /////////////////////STATES///////////////////////
   
  uint256 public s_entranceFee; 
  uint256 public s_lotteryDuration; 
  uint256 public s_lastLottery;
  address payable[] public s_players;  //https://ethereum.stackexchange.com/questions/24061/is-there-a-maximum-array-size-in-solidity
  address public s_winner; 
  uint256 public s_fundingFee; // ex. 670 //https://www.youtube.com/watch?v=nsf46dzgCog
  uint256 public s_totalLotteryBalance;
  uint256 public s_randomness;
  bytes32 internal immutable keyHash; //https://ethereum.stackexchange.com/questions/82259/what-is-the-difference-between-the-constant-and-immutable-keywords-in-solidity
  uint256 internal immutable chainLinkFee; 
  mapping(address => uint256) public balance;
  enum State {OPEN,CLOSED,CALCULATING}
  State public s_state;
  

  /////////////////// EVENTS //////////////////////

  event lastWinner(address indexed _Winner, uint256 _amountWon);

  // MUMBAI
  // LINK TOKEN : 0x326C977E6efc84E512bB9C30f76E30c160eD06FB
  // vrf_coordinator : 0x8C7382F9D8f56b33781fE506E897a4F1e2d17255
  // fee : 0.0001 Link
  // key_hash : 0x6e75b569a01ef56d18cab6a8e71e6600d6ce853834d4a5748b720d06f878b3a4 
  // entranceAmount : 100000000000000000

  // RINKEBY
  // LINK TOKEN : 0x01BE23585060835E02B77ef475b0Cc51aA1e0709
  // vrf_coordinator : 0xb3dCcb4Cf7a26f6cf6B120Cf5A73875B7BBc655B
  // key_hash : 0x2ed0feb3e7fd2022120aa84fab1945545a9f2ffc9076fd6156fa96eaff4c1311
  // fee : 0.1 LINK
  // entranceAmount : 100000000000000000

  //////////////////CONSTRUCTOR//////////////////////
  
  constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash)
     
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
   
    {
        keyHash = _keyhash;
        chainLinkFee = 0.0001 * 10**18; //be careful with network's fee.
        s_state = State.CLOSED;
        
    }

  function enter() payable public {
    require(s_state == State.OPEN,"Lottery must be OPEN, please wait.");
    require(msg.value == s_entranceFee,"Please, send xx MATIC.");
    require(s_players.length <= 100,"Maximun participant's capacity");
    require(msg.sender != owner(),"Owner can not participate in the  Lottery.");
    s_players.push(payable(msg.sender));
    s_totalLotteryBalance += s_entranceFee;
  }

  function start() public onlyOwner {
    require(s_state == State.CLOSED,"Lottery must be CLOSED, please wait.");
    require(LINK.balanceOf(address(this)) >= chainLinkFee, "Not enough LINK - fill contract with faucet.");
    require(s_lotteryDuration > s_lastLottery,"Lottery has to last longer.");
    require(s_entranceFee > 0 && s_fundingFee > 0,"Either entrance fee and funding fee have to be above cero.");
    s_state = State.OPEN;
  }

  function close( ) public {
    require(s_state == State.OPEN,"Lottery must be OPEN, please wait.");
    require(LINK.balanceOf(address(this)) >= chainLinkFee, "Not enough LINK - fill contract with faucet.");
    require(block.timestamp >= s_lotteryDuration,"Lottery has not finished.");//https://ethereum.stackexchange.com/questions/15747/what-is-the-difference-between-now-and-block-timestamp
    require(s_players.length > 1, "Not enough players.");
    s_state = State.CALCULATING;
    s_lastLottery = s_lotteryDuration;
    requestRandomness(keyHash,chainLinkFee);//we need to check this call does not reverts.
  }

//https://docs.chain.link/docs/vrf-security-considerations/v1/#fulfillrandomness-must-not-revert
//fulfillRandomness must not revert.
//If your fulfillRandomness function uses more than 200k gas, the transaction will fail.

 function fulfillRandomness(bytes32 /*requestId*/, uint256 randomNumber) internal override { 
    s_randomness = randomNumber;
    uint256 randomWinner = (s_randomness % s_players.length) + 1 ;
    s_winner = s_players[randomWinner];
  }

  // function pickWinner() was changed to fundWinner(), reasons below.
  //running function pickWinner() the transaction reverts and gives the following data:
  //0x4e487b710000000000000000000000000000000000000000000000000000000000000032
  //https://www.4byte.directory/
  //0x4e487b71
  //Panic(uint256)
  //https://docs.soliditylang.org/en/v0.8.6/control-structures.html?highlight=Panic#panic-via-assert-and-error-via-require
  //0x41: If you allocate too much memory or create an array that is too large.
  //we think is due to copying a big number into memory.

  function fundWinner() public {
    require(s_state == State.CALCULATING,"Lottery must be CALCULATING, please wait.");
    require(s_winner != address(0),"address(0x000...) could not be the winner");
    uint256 total = s_totalLotteryBalance;
    uint256 amtFunding = (total * s_fundingFee) / 10000;
    uint256 amtWinner = (total - amtFunding);
    balance[owner()] += amtFunding;
    balance[s_winner] += amtWinner;
    s_totalLotteryBalance = 0; // this could be refactor to balance[LOTTERY] = 0 // Lottery as an internal balance.
    delete s_players;//https://www.evm.codes/#60 // 429,043.00 gas for 100 elements // aprox. 2,800,000 gas for 600 elments
    delete s_winner;
    s_state = State.CLOSED; 
  }

 // pull pattern

 function claim() public nonReentrant {
    require(balance[msg.sender] > 0,"You need funds to claim.");
    uint256 amt = balance[msg.sender];
    balance[msg.sender] = 0;
    TransferHelper.safeTransferETH(msg.sender,amt);
    }

 function setLottery(uint256 _addTime, uint256 _entranceAmount, uint256 _basisPoints) public onlyOwner {
    require( s_state == State.CLOSED,"State must be CLOSED" );
    s_lotteryDuration = block.timestamp + _addTime;//e.g. 5 min = 300 blocks //https://docs.soliditylang.org/en/develop/units-and-global-variables.html#time-units
    s_entranceFee = _entranceAmount; // e.g. 1 ETH = 1000000000000000000 Wei = 10**18 Wei.
    s_fundingFee = _basisPoints;// e.g. 670 = 6.7 pct.  
    }

 function withdrawLink() public onlyOwner {
    require( s_state == State.CLOSED,"State must be CLOSED" );
    LINK.transfer(msg.sender, LINK.balanceOf(address(this)));
    }

    //If requestRandomness reverts, we wont be able to close the lottery and send the funds.
    //Here we could pull the funds and giving them back to the next winner or do the picking off chain.
    //Only possible if none calls fundWinner() 1 hour after close() was called.
  
  function emergencyWithdraw() public onlyOwner nonReentrant {
    require(s_state == State.CALCULATING,"Lottery must be CALCULATING, please wait.");
    require(block.timestamp > (s_lotteryDuration + 6 hours ),"Less than an hour has passed.");
    balance[owner()] = s_totalLotteryBalance;
    s_state = State.CLOSED;

  }
}

