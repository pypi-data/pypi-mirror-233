"""TcService integration test"""
import logging
import pytest
from edgepi.tc.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import TCAddresses, CJMode as sdkCJMode, ConvMode as sdkConvMode
from edgepi_rpc_client.services.tc.client_tc_service import ClientTcService
from edgepi_rpc_client.services.tc.tc_pb_enums import (
    AvgMode,
    CJHighMask,
    CJLowMask,
    CJMode,
    ConvMode,
    DecBits4,
    DecBits6,
    FaultMode,
    NoiseFilterMode,
    OpenCircuitMode,
    OpenMask,
    OvuvMask,
    TCHighMask,
    TCLowMask,
    TCType,
    VoltageMode,
)

_logger = logging.getLogger(__name__)

@pytest.fixture(name="tc_service")
def fixture_test_tc_service():
    """Inits new tc service client for testing"""
    return ClientTcService('tcp://localhost:5555')

@pytest.fixture(name="edgepi_tc")
def fixture_test_edgepi_tc():
    """Inits new EdgePiTc for testing"""
    return EdgePiTC()


@pytest.mark.parametrize(
    "args, set_reg_value, updated_regs",
    [
        (
            {"conversion_mode": ConvMode.SINGLE},
            {TCAddresses.CR0_W.value: 0x80},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"conversion_mode": ConvMode.AUTO},
            None,
            {TCAddresses.CR0_W.value: 0x80},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.HIGH_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x30},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.MED_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x20},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.LOW_INPUT_IMPEDANCE},
            None,
            {TCAddresses.CR0_W.value: 0x10},
        ),
        (
            {"open_circuit_mode": OpenCircuitMode.DISABLED},
            {TCAddresses.CR0_W.value: 0x10},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"cold_junction_mode": CJMode.DISABLE},
            None,
            {TCAddresses.CR0_W.value: 0x08},
        ),
        (
            {"cold_junction_mode": CJMode.ENABLE},
            {TCAddresses.CR0_W.value: 0x08},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"fault_mode": FaultMode.INTERRUPT},
            None,
            {TCAddresses.CR0_W.value: 0x04},
        ),
        (
            {"fault_mode": FaultMode.COMPARATOR},
            {TCAddresses.CR0_W.value: 0x04},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"noise_filter_mode": NoiseFilterMode.HZ_60},
            {TCAddresses.CR0_W.value: 0x01},
            {TCAddresses.CR0_W.value: 0x00},
        ),
        (
            {"noise_filter_mode": NoiseFilterMode.HZ_50},
            None,
            {TCAddresses.CR0_W.value: 0x01},
        ),
        (
            {"average_mode": AvgMode.AVG_16},
            None,
            {TCAddresses.CR1_W.value: 0x43},
        ),
        (
            {"average_mode": AvgMode.AVG_8},
            None,
            {TCAddresses.CR1_W.value: 0x33},
        ),
        (
            {"average_mode": AvgMode.AVG_4},
            None,
            {TCAddresses.CR1_W.value: 0x23},
        ),
        (
            {"average_mode": AvgMode.AVG_2},
            None,
            {TCAddresses.CR1_W.value: 0x13},
        ),
        (
            {"average_mode": AvgMode.AVG_1},
            {TCAddresses.CR1_W.value: 0x13},
            {TCAddresses.CR1_W.value: 0x03},
        ),
        (
            {"tc_type": TCType.TYPE_B},
            None,
            {TCAddresses.CR1_W.value: 0x00},
        ),
        (
            {"tc_type": TCType.TYPE_E},
            None,
            {TCAddresses.CR1_W.value: 0x01},
        ),
        (
            {"tc_type": TCType.TYPE_J},
            None,
            {TCAddresses.CR1_W.value: 0x02},
        ),
        (
            {"tc_type": TCType.TYPE_K},
            None,
            {TCAddresses.CR1_W.value: 0x03},
        ),
        (
            {"tc_type": TCType.TYPE_N},
            None,
            {TCAddresses.CR1_W.value: 0x04},
        ),
        (
            {"tc_type": TCType.TYPE_R},
            None,
            {TCAddresses.CR1_W.value: 0x05},
        ),
        (
            {"tc_type": TCType.TYPE_S},
            None,
            {TCAddresses.CR1_W.value: 0x06},
        ),
        (
            {"tc_type": TCType.TYPE_T},
            None,
            {TCAddresses.CR1_W.value: 0x07},
        ),
        (
            {"voltage_mode": VoltageMode.GAIN_8},
            None,
            {TCAddresses.CR1_W.value: 0x08},
        ),
        (
            {"voltage_mode": VoltageMode.GAIN_32},
            None,
            {TCAddresses.CR1_W.value: 0x0C},
        ),
        (
            {"cj_high_mask": CJHighMask.CJHIGH_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xDF},
        ),
        (
            {"cj_high_mask": CJHighMask.CJHIGH_MASK_ON},
            {TCAddresses.MASK_W.value: 0xDF},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xEF},
        ),
        (
            {"cj_low_mask": CJLowMask.CJLOW_MASK_ON},
            {TCAddresses.MASK_W.value: 0xEF},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xF7},
        ),
        (
            {"tc_high_mask": TCHighMask.TCHIGH_MASK_ON},
            {TCAddresses.MASK_W.value: 0xF7},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFB},
        ),
        (
            {"tc_low_mask": TCLowMask.TCLOW_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFB},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFD},
        ),
        (
            {"ovuv_mask": OvuvMask.OVUV_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFD},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_OFF},
            None,
            {TCAddresses.MASK_W.value: 0xFE},
        ),
        (
            {"open_mask": OpenMask.OPEN_MASK_ON},
            {TCAddresses.MASK_W.value: 0xFE},
            {TCAddresses.MASK_W.value: 0xFF},
        ),
        (
            {"cj_high_threshold": 100},
            None,
            {TCAddresses.CJHF_W.value: 0x64},
        ),
        ({"cj_low_threshold": -16}, None, {TCAddresses.CJLF_W.value: 0x90}),
        (
            {"lt_high_threshold": 1000, "lt_high_threshold_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.LTHFTH_W.value: 0x3E, TCAddresses.LTHFTL_W.value: 0x8F},
        ),
        (
            {"lt_low_threshold": -55, "lt_low_threshold_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.LTLFTH_W.value: 0x83, TCAddresses.LTLFTL_W.value: 0x7F},
        ),
        (
            {"cj_offset": 4, "cj_offset_decimals": DecBits4.P0_9375},
            None,
            {TCAddresses.CJTO_W.value: 0x4F},
        ),
        (
            {"cj_temp": 100, "cj_temp_decimals": DecBits6.P0_984375},
            {TCAddresses.CR0_W.value: 0x08},  # disable cold junction sensor
            {TCAddresses.CJTH_W.value: 0x64, TCAddresses.CJTL_W.value: 0xFC},
        ),
    ],
)

def test_set_config(tc_service,edgepi_tc, args, set_reg_value, updated_regs):
    """Tests set_config tc service method"""

    # reset registers to default values
    edgepi_tc.reset_registers()

    # modify default values for this test only if needed
    if set_reg_value is not None:
        for addx, value in set_reg_value.items():
            # pylint: disable=protected-access
            edgepi_tc._EdgePiTC__write_to_register(addx, value)

    # update registers with user args
    response  = tc_service.set_config(**args)
    assert response == 'Successfully applied thermocouple configurations using set_config'

    # if overwriting cold junction temp, re-enable sensing to return
    # CR0 to default value for value comparison below
    if "cj_temp" in args.keys() or "cj_temp_decimals" in args.keys():
        tc_service.set_config(cold_junction_mode=CJMode.ENABLE)

    # read updated register values. pylint: disable=protected-access
    reg_values = edgepi_tc._EdgePiTC__read_registers_to_map()

    # compare to expected register values
    for addx, value in reg_values.items():
        # these require cold-junction sensor to be disabled, otherwise
        # they are continously updated and cannot be tested against default values
        if addx in (TCAddresses.CJTH_W.value, TCAddresses.CJTL_W.value):
            continue

        # check registers not updated have not been changed
        if addx not in updated_regs:
            assert value == edgepi_tc.default_reg_values[addx]
        # check updates were applied
        else:
            assert value == updated_regs[addx]


def test_single_sample(tc_service):
    """Test for single_sample method"""
    # test passes if both cold junction and linearized temp readings are float
    temps = tc_service.single_sample()
    assert len(temps) == 2
    for temp in temps:
        assert isinstance(temp,float)

def test_read_temperatures(tc_service):
    """Test for read_temperatures method"""
    # Call read_temperatures
    temps = tc_service.read_temperatures()

    _logger.info("%s", temps)
    assert len(temps) == 2
    for temp in temps:
        assert isinstance(temp,float)

@pytest.mark.parametrize(
        'filter_at_fault',
        [
            (True), (False)
        ]
)

def test_read_faults(tc_service, edgepi_tc, filter_at_fault):
    """Test for read_faults method"""

    # Call method
    response =  tc_service.read_faults(filter_at_fault)

    _logger.debug("RESPONSE FAULT DICT: %s", response)

    # Do actual SDK fault reading method
    edgepi_faults = edgepi_tc.read_faults()

    # Compare
    for _,fault in edgepi_faults.items():
        fault_type = str(fault.fault_type)
        assert fault.fault_type in response
        assert response[fault_type]['Fault Type'] == fault_type
        assert response[fault_type]['At Fault'] == fault.at_fault
        assert response[fault_type]['Fault Message'] == str(fault.err_msg.value)
        assert response[fault_type]['Fault Masked'] == fault.is_masked

def test_clear_faults(tc_service):
    """Test for clear_faults method"""
    response = tc_service.clear_faults()

    assert response == 'Successfully called clear_faults'


def test_reset_registers(tc_service):
    """Test for reset_registers method"""
    response = tc_service.reset_registers()

    assert response == 'Successfully called reset_registers'

def test_overwrite_cold_junction_temp(tc_service,edgepi_tc):
    """Test for overwrite cold_junction_temp"""
    # Disable cold junction sensor and set to single conversion mode
    edgepi_tc.set_config(conversion_mode = sdkConvMode.SINGLE, cold_junction_mode=sdkCJMode.DISABLE)
    assert edgepi_tc.tc_state.cold_junction

    # Call method
    response = tc_service.overwrite_cold_junction_temp(
        cj_temp=20, cj_temp_decimals=DecBits6.P0_765625)
    assert response == 'Successfully called overwrite_cold_junction_temp'
    # Verify the write
    cj_temp,_ = edgepi_tc.single_sample()
    assert cj_temp == 20.765625

    # Re-enable cold junction sensor
    edgepi_tc.set_config(cold_junction_mode=sdkCJMode.ENABLE)
    assert not edgepi_tc.tc_state.cold_junction
    # Verify the reset
    cj_temp,_ = edgepi_tc.single_sample()
    assert cj_temp != 20.765625
