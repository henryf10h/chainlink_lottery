from brownie import accounts, config, Lottery, network, chain

def main():
    net = network.show_active()
    account = accounts.add(config['wallets']['from_key'])
    lot = Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account })
    lot_obj = lot.s_players()
    print(lot_obj)