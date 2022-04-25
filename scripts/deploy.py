from brownie import AdvanceCollectible, config, network
from scripts.helper_scripts import get_account, get_contract


def deploy():
    account = get_account()
    print(f"Your Account: {account.address}")
    advance_collectible = AdvanceCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify",
            False,
        ),
    )
    print(f"Deployed at: {advance_collectible.address}")
    return advance_collectible


def main():
    deploy()