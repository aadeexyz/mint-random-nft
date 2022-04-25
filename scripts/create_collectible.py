from brownie import AdvanceCollectible
from scripts.helper_scripts import get_account, fund_with_link
from web3 import Web3


def create_collectible():
    account = get_account()
    advance_collectible = AdvanceCollectible[-1]
    fund_with_link(advance_collectible.address,
                   amount=Web3.toWei(0.1, "ether"))
    creation_tx = advance_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("New token has been created!")
    return creation_tx


def main():
    create_collectible()