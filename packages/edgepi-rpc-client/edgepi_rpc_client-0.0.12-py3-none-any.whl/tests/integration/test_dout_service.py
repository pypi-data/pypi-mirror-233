"""
DoutService integration tests. TODO: 
use get_state rpc service method once implement to compare expected resulst instead of edgepi sdk
"""
import pytest
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput
from edgepi.digital_output.digital_output_constants import (
    DoutPins as sdkDoutPins, DoutTriState as sdkDoutTriState)
from edgepi_rpc_client.services.dout.client_dout_service import ClientDoutService
from edgepi_rpc_client.services.dout.dout_pb_enums import DoutPins,DoutTriState

@pytest.fixture(name='dout_service')
def fixture_test_dout_service():
    """Inits new led serviceclient for testing"""
    return ClientDoutService('tcp://localhost:5555')

@pytest.mark.parametrize("pin, sdk_pin", [
    (DoutPins.DOUT1, sdkDoutPins.DOUT1),
    (DoutPins.DOUT2, sdkDoutPins.DOUT2),
    (DoutPins.DOUT3, sdkDoutPins.DOUT3),
    (DoutPins.DOUT4, sdkDoutPins.DOUT4),
    (DoutPins.DOUT5, sdkDoutPins.DOUT5),
    (DoutPins.DOUT6, sdkDoutPins.DOUT6),
    (DoutPins.DOUT7, sdkDoutPins.DOUT7),
    (DoutPins.DOUT8, sdkDoutPins.DOUT8),
])
def test_output_high(dout_service,pin, sdk_pin):
    """Test client call for set_dout_state and compares results using sdk method and enum"""
    edgepi_dout = EdgePiDigitalOutput()
    client_dout = dout_service
    response =client_dout.set_dout_state(pin, DoutTriState.HIGH)
    dout_state = edgepi_dout.get_state(sdk_pin)
    assert dout_state == sdkDoutTriState.HIGH
    assert response == f'Successfully set {sdk_pin} to DoutTriState.HIGH.'

@pytest.mark.parametrize("pin, sdk_pin", [
    (DoutPins.DOUT1, sdkDoutPins.DOUT1),
    (DoutPins.DOUT2, sdkDoutPins.DOUT2),
    (DoutPins.DOUT3, sdkDoutPins.DOUT3),
    (DoutPins.DOUT4, sdkDoutPins.DOUT4),
    (DoutPins.DOUT5, sdkDoutPins.DOUT5),
    (DoutPins.DOUT6, sdkDoutPins.DOUT6),
    (DoutPins.DOUT7, sdkDoutPins.DOUT7),
    (DoutPins.DOUT8, sdkDoutPins.DOUT8),
])
def test_output_z(dout_service,pin, sdk_pin):
    """Test client call for set_dout_state and compares results using sdk method and enum"""
    edgepi_dout = EdgePiDigitalOutput()
    client_dout = dout_service
    response = client_dout.set_dout_state(pin, DoutTriState.HI_Z)
    dout_state = edgepi_dout.get_state(sdk_pin)
    assert dout_state == sdkDoutTriState.HI_Z
    assert response == f'Successfully set {sdk_pin} to DoutTriState.HI_Z.'

@pytest.mark.parametrize("pin, sdk_pin", [
    (DoutPins.DOUT1, sdkDoutPins.DOUT1),
    (DoutPins.DOUT2, sdkDoutPins.DOUT2),
    (DoutPins.DOUT3, sdkDoutPins.DOUT3),
    (DoutPins.DOUT4, sdkDoutPins.DOUT4),
    (DoutPins.DOUT5, sdkDoutPins.DOUT5),
    (DoutPins.DOUT6, sdkDoutPins.DOUT6),
    (DoutPins.DOUT7, sdkDoutPins.DOUT7),
    (DoutPins.DOUT8, sdkDoutPins.DOUT8),
])
def test_output_low(dout_service,pin, sdk_pin):
    """Test client call for set_dout_state and compares results using sdk method and enum"""
    edgepi_dout = EdgePiDigitalOutput()
    client_dout = dout_service
    response = client_dout.set_dout_state(pin, DoutTriState.LOW)
    dout_state = edgepi_dout.get_state(sdk_pin)
    assert dout_state == sdkDoutTriState.LOW
    assert response == f'Successfully set {sdk_pin} to DoutTriState.LOW.'
