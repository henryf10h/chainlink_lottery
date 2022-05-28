from brownie import accounts, config, Lottery, network, chain, interface, Contract
import  time

abi = [       
    {   
        'inputs': [
            {
                'internalType': "address",
                'name': "_VRFCoordinator",
                'type': "address"
            },
            {
                'internalType': "address",
                'name': "_LinkToken",
                'type': "address"
            },
            {
                'internalType': "bytes32",
                'name': "_keyhash",
                'type': "bytes32"
            }
        ],
        'name': "constructor",
        'stateMutability': "nonpayable",
        'type': "constructor"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "previousOwner",
                'type': "address"
            },
            {
                'indexed': True,
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "OwnershipTransferred",
        'type': "event"
    },
    {
        'anonymous': False,
        'inputs': [
            {
                'indexed': True,
                'internalType': "address",
                'name': "_Winner",
                'type': "address"
            },
            {
                'indexed': False,
                'internalType': "uint256",
                'name': "_amountWon",
                'type': "uint256"
            }
        ],
        'name': "lastWinner",
        'type': "event"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'name': "balance",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "claim",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "close",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "emergencyWithdraw",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "enter",
        'outputs': [],
        'stateMutability': "payable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "fundWinner",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "owner",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "bytes32",
                'name': "requestId",
                'type': "bytes32"
            },
            {
                'internalType': "uint256",
                'name': "randomness",
                'type': "uint256"
            }
        ],
        'name': "rawFulfillRandomness",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "renounceOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_entranceFee",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_fundingFee",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_lastLottery",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_lotteryDuration",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'name': "s_players",
        'outputs': [
            {
                'internalType': "address payable",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_randomness",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_state",
        'outputs': [
            {
                'internalType': "enum Lottery.State",
                'name': "",
                'type': "uint8"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_totalLotteryBalance",
        'outputs': [
            {
                'internalType': "uint256",
                'name': "",
                'type': "uint256"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "s_winner",
        'outputs': [
            {
                'internalType': "address",
                'name': "",
                'type': "address"
            }
        ],
        'stateMutability': "view",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "uint256",
                'name': "_addTime",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_entranceAmount",
                'type': "uint256"
            },
            {
                'internalType': "uint256",
                'name': "_basisPoints",
                'type': "uint256"
            }
        ],
        'name': "setLottery",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "start",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [
            {
                'internalType': "address",
                'name': "newOwner",
                'type': "address"
            }
        ],
        'name': "transferOwnership",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    },
    {
        'inputs': [],
        'name': "withdrawLink",
        'outputs': [],
        'stateMutability': "nonpayable",
        'type': "function"
    }
]

def main():
    account = accounts.add(config['wallets']['from_key'])
    net = network.show_active()
    print(net)
    # https://eth-brownie.readthedocs.io/en/stable/core-contracts.html
    lottery = Contract.from_abi("Lottery", "0x080c0F31a3Ede1C011B43C648924F61da3216621", abi)
    time.sleep(1)
# set
    lottery.setLottery(500000, 1000000000000000000, 1000,{'from': account })