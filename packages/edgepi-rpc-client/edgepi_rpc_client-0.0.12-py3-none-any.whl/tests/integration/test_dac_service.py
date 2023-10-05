"""Integration tests DAC service"""
import pytest
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi_rpc_client.services.dac.client_dac_service import ClientDacService
from edgepi_rpc_client.services.dac.dac_pb_enums import DACChannel

@pytest.fixture(name="dac_service")
def fixture_test_dac_service():
    """Inits new dac service client for testing"""
    return ClientDacService('tcp://localhost:5555')


def test_reset(dac_service):
    """Tests client call for dac reset"""
    response = dac_service.reset()

    assert response == "Successfully reset DAC."

@pytest.mark.parametrize("channel, voltage,", [
    (DACChannel.AOUT1, 3.0),
    (DACChannel.AOUT2, 3.0),
    (DACChannel.AOUT3, 3.0),
    (DACChannel.AOUT4, 3.0),
    (DACChannel.AOUT5, 3.0),
    (DACChannel.AOUT6, 3.0),
    (DACChannel.AOUT7, 3.0),
    (DACChannel.AOUT8, 3.0)
])
def test_write_read_voltage(dac_service, channel, voltage):
    """Test client call for write voltage and compare with result of client call of get_state"""

    write_response = dac_service.write_voltage(channel,voltage)

    assert write_response == f"Successfully wrote {voltage}v to {channel}."

    _,read_voltage,_ = dac_service.get_state(channel, False, True, False)

    # assert read_voltage is voltage
    assert read_voltage == pytest.approx(voltage, abs=1e-3)

    # Reset
    dac_service.reset()

@pytest.mark.parametrize("gain", [
    (True),
    (False)
])
def test_set_get_gain(dac_service, gain):
    """Test client call for setting gain and then compare with client call of getting gain"""

    gain_state = dac_service.set_dac_gain(gain)

    _,_,read_gain = dac_service.get_state(DACChannel.AOUT1, False, False, True)

    assert gain_state == gain and gain == read_gain

    dac_service.reset()

def test_code(dac_service):
    """Tests that auto_code_change functionality works and that reading code works"""
    # Init dac (sdk)
    edgepi_dac = EdgePiDAC()

    # Enforce gain and auto code change to false
    dac_service.set_dac_gain(False,False)

    # write voltage
    dac_service.write_voltage(DACChannel.AOUT1, 3.3)

    # change gain with auto_code_change enabled
    dac_service.set_dac_gain(True,True)

    # read code and voltage
    read_code,read_voltage,_ = dac_service.get_state(DACChannel.AOUT1, True, True, True)

    # check voltage stayed the same and code is correct
    assert read_voltage == pytest.approx(3.3, abs=1e-3)
    assert read_code == edgepi_dac.dac_ops.voltage_to_code(DACChannel.AOUT1.value, read_voltage, 2)

    # Reset
    dac_service.reset()
