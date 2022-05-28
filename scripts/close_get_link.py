from brownie import accounts, config, Lottery, network, chain, interface
import  time

def main():
    account = accounts.add(config['wallets']['from_key'])
    net = network.show_active()
    print(net)
    Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account })
    lottery = Lottery[len(Lottery) - 1]
    time.sleep(1)
# set
    lottery.setLottery(1, 10000000000000000, 1000,{'from': account })
    time.sleep(1)
    print(lottery.s_lotteryDuration()) 
    print(lottery.s_entranceFee())
    print(lottery.s_fundingFee())
    link = interface.ERC20("0x01be23585060835e02b77ef475b0cc51aa1e0709")
    time.sleep(1)
    link.transfer(lottery, 1000000000000000000, {'from':account})
# start
    time.sleep(1)
    lottery.start({'from' : account})
    time.sleep(1)
# enter
    account2 = accounts.add(config['wallets']['from_key2'])
    lottery.enter({'from' : account2, 'amount' : 10000000000000000})
    time.sleep(1)
    account3 = accounts.add(config['wallets']['from_key3'])
    lottery.enter({'from' : account3, 'amount' : 10000000000000000})
# close
    time.sleep(5)
    lottery.close({'from':account})
    time.sleep(5)
    while lottery.s_winner() == accounts.at('0x0000000000000000000000000000000000000000', force=True):
        print('not yet  man')
        time.sleep(2)
        lottery.s_winner()
        print(lottery.s_winner())
        time.sleep(2)
        
# fundWinner
    lottery.fundWinner({'from':account2})
    print(lottery.s_winner())
# claim
    #we test claim on funding address, in this example is 
    lottery.claim({'from' : account})