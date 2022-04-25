from brownie import AdvanceCollectible, network
from scripts.helper_scripts import OPENSEA_URL, get_account
import json


def set_token_uri(token_id, nft_contract, token_uri):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, token_uri, {"from": account})
    tx.wait(1)


def main():
    print(f"Active network: {network.show_active()}")
    advance_collectible = AdvanceCollectible[-1]
    number_of_collectibles = advance_collectible.tokenCounter()
    print(f"Number of collectibles: {number_of_collectibles}")

    for token_id in range(number_of_collectibles):
        if not advance_collectible.tokenURI(token_id).startswith("ipfs://"):
            print(f"Setting token URI for: {token_id}")
            with open(f"./metadata/{network.show_active()}/metadata-hashes.json") as f:
                metadata_hashes = json.load(f)
                set_token_uri(
                    token_id,
                    advance_collectible,
                    metadata_hashes[str(token_id)],
                )
                print(
                    f"View NFT at: {OPENSEA_URL}/{advance_collectible.address}/{token_id}"
                )
