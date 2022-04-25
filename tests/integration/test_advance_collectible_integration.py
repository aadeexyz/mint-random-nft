from brownie import network
from scripts.helper_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_LOCAL_ENVIRONMENTS
from scripts.deploy import deploy
import pytest
import time


def test_can_create_collectible_integration():
    # Arrange
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
            or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        pytest.skip("Only for integration testing!")

    # Act
    advance_collectible = deploy()
    time.sleep(180)

    # Assert
    assert advance_collectible.tokenCounter() == 1