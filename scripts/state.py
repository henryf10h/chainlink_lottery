from brownie import accounts, config, Lottery, network, chain

def main():
    net = network.show_active()
    account = accounts.add(config['wallets']['from_key'])
    contract = Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account }) 
    print(contract.s_state())