from brownie import (
    MockV3Aggregator,
    LinkToken,
    MockVRFCoordinator,
    Contract,
    accounts,
    network,
    config,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets"
DECIMALS = 8
INITIAL_VALUE = 200000000000
CONTRACT_TO_MOCK = {
    "v3_aggregator": MockV3Aggregator,
    "link_token": LinkToken,
    "vrf_coordinator": MockVRFCoordinator,
}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    elif id:
        return accounts.get(id)
    elif (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
          or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"Active Network: {network.show_active()}")
    account = get_account()
    print("Deploying Mocks...")
    CONTRACT_TO_MOCK["v3_aggregator"].deploy(
        decimals,
        initial_value,
        {"from": account},
    )
    print("Deployed MockV3Aggregator")
    link_token = CONTRACT_TO_MOCK["link_token"].deploy({"from": account})
    print("Deployed LinkToken")
    CONTRACT_TO_MOCK["vrf_coordinator"].deploy(
        link_token.address,
        {"from": account},
    )
    print("Deployed MockVRFCoordinator")
    print("Mocks Deployed!")


def get_contract(contract_name):
    contract_type = CONTRACT_TO_MOCK[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][
            network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name,
            contract_address,
            contract_type.abi,
        )
    return contract


def fund_with_link(
        contract_address,
        account=None,
        link_token=None,
        amount=Web3.toWei(0.1, "ether"),
):
    acount = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": acount})
    tx.wait(1)
    print(f"Funded {contract_address} with {amount} LINK")
