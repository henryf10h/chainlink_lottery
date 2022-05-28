from brownie import accounts, config, Lottery, network, chain

def main():
    net = network.show_active()
    account = accounts.add(config['wallets']['from_key'])
    contract = Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account }) 
    blok = chain.time()
    print(blok)
    set_lot = contract.setLottery(300, 100000000000000000, 1000,{'from': account })
    print(set_lot)
    dur = contract.s_lotteryDuration()
    print(dur)