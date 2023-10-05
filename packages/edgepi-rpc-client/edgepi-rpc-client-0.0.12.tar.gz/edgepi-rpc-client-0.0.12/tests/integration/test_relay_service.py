"""
Relay service integration tests
"""
import pytest
from edgepi_rpc_client.services.relay.client_relay_service import ClientRelayService

@pytest.fixture(name='relay_service')
def fixture_test_relay_service():
    """Inits new relay service client for testing"""
    return ClientRelayService('tcp://localhost:5555')

def test_open_relay(relay_service):
    """Test client call of open_relay and compare with client call of get_state_relay"""
    # Open relay
    response = relay_service.open_relay()

    state = relay_service.get_state_relay()

    assert not state
    assert response == "Successfully opened relay"

def test_close_relay(relay_service):
    """Test client call of close_relay and compare with client call of get_state_relay"""
    # Open relay
    response = relay_service.close_relay()

    state = relay_service.get_state_relay()

    assert state
    assert response == "Successfully closed relay"
