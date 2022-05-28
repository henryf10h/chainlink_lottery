from brownie import network, accounts, config, Lottery

def main():
    net = network.show_active()
    print(net)
    account1 = accounts.add(config['wallets']['from_key'])
    print(config['wallets']['from_key'])
    return Lottery.deploy(config['networks'][net]['vrf_coordinator'],config['networks'][net]['link_token'],config['networks'][net]['keyhash'],{'from': account1 })

#https://github.com/eth-brownie/brownie/issues/1031

# 0x080c0F31a3Ede1C011B43C648924F61da3216621