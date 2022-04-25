from brownie import network
from scripts.helper_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.deploy import deploy
from scripts.create_collectible import create_collectible
import pytest


def test_can_create_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")

    # Act
    advance_collectible = deploy()
    creation_tx = create_collectible()
    random_number = 420
    request_id = creation_tx.events["requestedCollectible"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id,
        random_number,
        advance_collectible.address,
        {"from": get_account()},
    )

    # Assert
    assert advance_collectible.tokenCounter() == 1
    assert advance_collectible.tokenIdToShape(0) == random_number % 3