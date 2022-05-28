from brownie import accounts, config, Lottery, network, Contract, interface

#send link
#interface.LinkTokenInterface(link_token)

def main():
    net = network.show_active()
    account = accounts.add(config['wallets']['from_key'])
    contract_container = Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account })
    print(contract_container)
    link = interface.ERC20("0x01be23585060835e02b77ef475b0cc51aa1e0709")
    link.transfer(contract_container, 100000000000000000, {'from':account})
    
