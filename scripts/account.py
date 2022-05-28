from brownie import accounts, config

def main():
    a = accounts.add(config['wallets']['from_key'])
    print(type(a))
    return a
    