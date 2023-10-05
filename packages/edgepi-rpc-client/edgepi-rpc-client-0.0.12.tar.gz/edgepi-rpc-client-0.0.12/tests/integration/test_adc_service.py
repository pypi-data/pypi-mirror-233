"""AdcService integration test"""
import logging
import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi_rpc_client.services.adc.client_adc_service import ClientAdcService
from edgepi_rpc_client.services.adc.adc_pb_enums import (
    AnalogIn, ConvMode, ADC1DataRate, FilterMode, ADC2DataRate, ADCNum, DiffMode)

_logger = logging.getLogger(__name__)

@pytest.fixture(name="adc_service")
def fixture_test_tc_service():
    """Inits new tc service client for testing"""
    return ClientAdcService('tcp://localhost:5555')



@pytest.mark.parametrize(
    "args",
    [
        (
            {
                "adc_1_analog_in": AnalogIn.AIN1
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN2
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN3
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN4
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN5
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN6
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN7
            }
        ),
        (
            {
                "adc_1_analog_in": AnalogIn.AIN8
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN1
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN2
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN3
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN4
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN5
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN6
            }

        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN7
            }
        ),
        (
            {
                "adc_2_analog_in": AnalogIn.AIN8
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_2P5
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_5
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_10_
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_16P6
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_20
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_50
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_60
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_100_
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_400_
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_1200
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_2400
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_4800
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_7200
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_14400
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_19200
            }
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_38400
            }
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_10
            }
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_100
            }
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_400
            }
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_800
            }
        ),
        (
            {
                "filter_mode": FilterMode.SINC1
            }
        ),
        (
            {
                "filter_mode": FilterMode.SINC2
            }
        ),
        (
            {
                "filter_mode": FilterMode.SINC3
            }
        ),
        (
            {
                "filter_mode": FilterMode.SINC4
            }
        ),
        (
            {
                "filter_mode": FilterMode.FIR
            }
        ),
        (
            {
                "conversion_mode": ConvMode.PULSE
            }
        ),
        (
            {
                "conversion_mode": ConvMode.CONTINUOUS
            }
        )
    ]
)
def test_set_config(adc_service, args):
    """Test for set_config ADC"""
    adc = EdgePiADC()

    response = adc_service.set_config(**args)
    assert response == "Successfully applied adc configurations using set_config"
    adc.reset()

def test_pulse_conversion_mode(adc_service):
    """"test for pulse conversion mode for adc service method"""

    # set config
    response = adc_service.set_config(adc_1_analog_in=AnalogIn.AIN1,
         conversion_mode=ConvMode.PULSE, adc_1_data_rate=ADC1DataRate.SPS_38400)

    # single sample
    out = adc_service.single_sample()

    _logger.debug('%s', out)

    assert response == "Successfully applied adc configurations using set_config"
    assert out != 0

@pytest.mark.parametrize(
    "diff_args, diff_str",
    [
        (
            {
                "adc": ADCNum.ADC_1,
                "diff_mode": DiffMode.DIFF_1
            },
            "DiffMode.DIFF_1"
        ),
        (
            {
                "adc": ADCNum.ADC_1,
                "diff_mode": DiffMode.DIFF_2
            },
            "DiffMode.DIFF_2"
        ),
        (
            {
                "adc": ADCNum.ADC_1,
                "diff_mode": DiffMode.DIFF_3
            },
            "DiffMode.DIFF_3"
        ),
        (
            {
                "adc": ADCNum.ADC_1,
                "diff_mode": DiffMode.DIFF_4
            },
            "DiffMode.DIFF_4"
        ),
        (
            {
                "adc": ADCNum.ADC_1,
                "diff_mode": DiffMode.DIFF_OFF
            },
            "DiffMode.DIFF_OFF"
        ),
        (
            {
                "adc": ADCNum.ADC_2,
                "diff_mode": DiffMode.DIFF_1
            },
            "DiffMode.DIFF_1"
        ),
        (
            {
                "adc": ADCNum.ADC_2,
                "diff_mode": DiffMode.DIFF_2
            },
            "DiffMode.DIFF_2"
        ),
        (
            {
                "adc": ADCNum.ADC_2,
                "diff_mode": DiffMode.DIFF_3
            },
            "DiffMode.DIFF_3"
        ),
        (
            {
                "adc": ADCNum.ADC_2,
                "diff_mode": DiffMode.DIFF_4
            },
            "DiffMode.DIFF_4"
        ),
        (
            {
                "adc": ADCNum.ADC_2,
                "diff_mode": DiffMode.DIFF_OFF
            },
            "DiffMode.DIFF_OFF"
        )
    ]
)
def test_continuous_differential(adc_service, diff_args, diff_str):
    """test differential functionality"""
    # config to pulse mode
    adc_service.set_config(conversion_mode=ConvMode.CONTINUOUS)

    # select differential
    diff_response = adc_service.select_differential(**diff_args)
    assert diff_response == f"Successfully selected {diff_str}."

    # don't continue on diff off
    if diff_args["diff_mode"] == DiffMode.DIFF_OFF:
        return

    # start conversions
    start_conv_response = adc_service.start_conversions(diff_args["adc"])
    assert start_conv_response == "Successfully started conversions."

    # read voltage
    voltage = adc_service.read_voltage(diff_args["adc"])
    assert isinstance(voltage, float)

    # stop conversions
    stop_conv_response = adc_service.stop_conversions(diff_args["adc"])
    assert stop_conv_response == "Successfully stopped conversions."

@pytest.mark.parametrize(
    "set_rtd_args, set_rtd_str",
    [
        (
            {
                "set_rtd": True,
                "adc": ADCNum.ADC_1
            },
            "on"
        ),
        (
            {
                "set_rtd": False,
                "adc": ADCNum.ADC_1
            },
            "off"
        ),
        (
            {
                "set_rtd": True,
                "adc": ADCNum.ADC_2
            },
            "on"
        ),
        (
            {
                "set_rtd": False,
                "adc": ADCNum.ADC_2
            },
            "off"
        ),
    ]
)
def test_rtd(adc_service, set_rtd_args, set_rtd_str):
    """test rtd functionaltiy"""
    # config to pulse mode
    adc_service.set_config(conversion_mode=ConvMode.PULSE)

    # set rtd
    response = adc_service.set_rtd(**set_rtd_args)
    assert response == f'Successfully set RTD {set_rtd_str}.'

    if set_rtd_args["set_rtd"] and set_rtd_args["adc"] == ADCNum.ADC_1:
        temp = adc_service.single_sample_rtd()
        assert isinstance(temp, float)


@pytest.mark.parametrize(
    "adc",
    [
        (ADCNum.ADC_1),(ADCNum.ADC_2),
    ]
)
def test_read_rtd_temperature(adc_service, adc):
    """test read_rtd_temperature functionality"""
    # config to continuous mode
    adc_service.set_config(conversion_mode=ConvMode.CONTINUOUS)

    # start conversions
    adc_service.start_conversions(adc)

    # set rtd conversions
    adc_service.set_rtd(True, adc)

    temp = adc_service.read_rtd_temperature()
    assert isinstance(temp, float)

    # stop conversions
    adc_service.stop_conversions(adc)

    # set rtd conversions
    adc_service.set_rtd(False, adc)
