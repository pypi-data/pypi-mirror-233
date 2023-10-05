"""DinService integration tests"""
import pytest
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput
from edgepi.digital_input.digital_input_constants import DinPins as sdkDinPins
from edgepi_rpc_client.services.din.client_din_service import ClientDinService
from edgepi_rpc_client.services.din.din_pb_enums import DinPins

@pytest.fixture(name='din_service')
def fixture_test_din_service():
    """Inits new din service client for testing"""
    return ClientDinService('tcp://localhost:5555')

@pytest.mark.parametrize("pin, sdk_pin", [
    (DinPins.DIN1, sdkDinPins.DIN1),
    (DinPins.DIN2, sdkDinPins.DIN2),
    (DinPins.DIN3, sdkDinPins.DIN3),
    (DinPins.DIN4, sdkDinPins.DIN4),
    (DinPins.DIN5, sdkDinPins.DIN5),
    (DinPins.DIN6, sdkDinPins.DIN6),
    (DinPins.DIN7, sdkDinPins.DIN7),
    (DinPins.DIN8, sdkDinPins.DIN8),
])
def test_digital_input_state(din_service, pin, sdk_pin):
    """Test client call for set_dout_state and compares results using sdk method and enum"""
    edgepi_din = EdgePiDigitalInput()
    client_din = din_service
    response =client_din.digital_input_state(pin)
    din_state = edgepi_din.digital_input_state(sdk_pin)
    assert response == din_state
