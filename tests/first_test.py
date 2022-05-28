import pytest
from datetime import datetime
import time

# 0x562c2eB9fEADaA4Ba14a1118C4d76a438eA193A0
# https://github.com/eth-brownie/brownie/issues/1003

from brownie import  config, network, interface, Lottery, accounts, chain
 #Brownie provides fixtures that simplify interacting with and testing your project. Most core Brownie functionality can be accessed via a fixture rather than an import statement.

@pytest.fixture
def account(accounts):
    return accounts.add(config['wallets']['from_key'])

def test_lottery(Lottery, account):
    net = network.show_active()
    Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account })
    lottery = Lottery[len(Lottery) - 1]

    assert account == accounts.at('0xc4eAb635B40bF49907375c3C7bd2495e3fDe79df', force=True)
# set
    lottery.setLottery(1, 100000000000000000, 1000,{'from': account })

    time.sleep(1)

    assert lottery.s_lotteryDuration() > chain.time() 
    assert lottery.s_entranceFee() == 100000000000000000
    assert lottery.s_fundingFee() == 1000

    link = interface.ERC20("0x01be23585060835e02b77ef475b0cc51aa1e0709")
    link.transfer(lottery, 100000000000000000, {'from':account})
# start
    lottery.start({'from' : account})

    assert lottery.s_state() == 0
# enter
    account2 = accounts.add(config['wallets']['from_key2'])
    lottery.enter({'from' : account2, 'amount' : 100000000000000000})

    assert lottery.s_totalLotteryBalance() == 100000000000000000

    account3 = accounts.add(config['wallets']['from_key3'])
    lottery.enter({'from' : account3, 'amount' : 100000000000000000})

    assert lottery.s_totalLotteryBalance() == 200000000000000000 
    
# close
    lottery.close({'from':account})

    # assert lottery.s_players(0) > 1
    assert lottery.s_state() == 2
    assert lottery.s_lotteryDuration() <= chain.time()
    #assert lottery.s_winner() != 0
    #s_winner would return 0x address. You have to wait for node to reply.

# fundWinner
    #waiting for oracle response could last up to 5 min.
    time.sleep(700)
    #when you dont wait you get 0 because random number has not come back.
    lottery.fundWinner({'from':account2})

    assert lottery.s_state() == 1
    assert lottery.s_winner() == 0
    assert lottery.s_randomness() > 0

# claim
    #we test claim on funding address, in this example is 
    lottery.claim({'from' : account})

    assert lottery.balance(account) > 0