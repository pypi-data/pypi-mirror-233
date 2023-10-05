"""
Client for adc service
"""
import logging
from edgepirpc.protos import adc_pb2 as adc_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.util.helpers import (
    filter_arg_values, create_config_request_from_args, get_server_response
)
from edgepi_rpc_client.services.adc.adc_pb_enums import (
    AnalogIn, ConvMode, ADC1DataRate, ADC2DataRate, FilterMode, ADCNum, DiffMode
)

_logger = logging.getLogger(__name__)

# pylint: disable=no-member
class ClientAdcService():
    """Client Methods for Adc Service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = adc_pb.AdcService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    # pylint: disable=unused-argument, too-many-arguments
    def set_config(self,
            adc_1_analog_in: AnalogIn = None,
            adc_1_data_rate: ADC1DataRate = None,
            adc_2_analog_in: AnalogIn = None,
            adc_2_data_rate: ADC2DataRate = None,
            filter_mode: FilterMode = None,
            conversion_mode: ConvMode = None,
            override_updates_validation: bool = False
        ):
        """set config method for sdk adc module"""
        # Get a dictionary of arguments that are not None.
        config_args_dict= filter_arg_values(locals(), 'self', None)
        _logger.debug("Config argument dictionary: %s", config_args_dict)

        # Create config request
        config_msg = adc_pb.Config()
        arg_msg = adc_pb.Config().ConfArg()
        request = create_config_request_from_args(config_msg, arg_msg, config_args_dict)

        # Call the SDK method through the rpc channel client
        rpc_response = self.service_stub.set_config(self.rpc_controller,request)

        response = get_server_response(rpc_response, adc_pb.SuccessMsg)

        return response.content

    def single_sample(self):
        """single_sample method for sdk adc module"""
        request = adc_pb.EmptyMsg()
        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.single_sample(self.rpc_controller,request)

        response = get_server_response(rpc_response, adc_pb.VoltageRead)

        voltage = response.voltage_read

        return voltage

    def select_differential(self, adc: ADCNum, diff_mode: DiffMode ):
        """select_differential method for sdk adc module"""
        request = adc_pb.DiffConfig(
            adc_num = adc.value,
            diff = diff_mode.value
        )

        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.select_differential(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.SuccessMsg)

        return response.content

    def set_rtd(self, set_rtd: bool, adc: ADCNum = ADCNum.ADC_2):
        """set_rtd method for sdk adc module"""
        request = adc_pb.RtdConfig(
            set_rtd = set_rtd,
            adc_num = adc.value
        )

        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.set_rtd(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.SuccessMsg)

        return response.content

    def single_sample_rtd(self):
        """single_sample_rtd method for sdk adc module"""
        request = adc_pb.EmptyMsg()

        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.single_sample_rtd(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.TempReading)

        temp = response.temp

        return temp

    def start_conversions(self, adc_num: ADCNum):
        """start_conversions method for sdk adc module"""
        # call start or stop converions
        request = adc_pb.ADC(
            adc_num = adc_num.value
        )

        # call sdk method through rpc channel client
        rpc_response = self.service_stub.start_conversions(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.SuccessMsg)

        return response.content

    def stop_conversions(self, adc_num: ADCNum):
        """stop_conversions method for sdk adc module"""
        # call start or stop converions
        request = adc_pb.ADC(
            adc_num = adc_num.value
        )

        # call sdk method through rpc channel client
        rpc_response = self.service_stub.stop_conversions(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.SuccessMsg)

        return response.content

    def read_voltage(self, adc_num: ADCNum):
        """read_voltage method for sdk adc module"""
        request = adc_pb.ADC(
            adc_num = adc_num.value
        )

        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.read_voltage(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.VoltageRead)

        return response.voltage_read

    def read_rtd_temperature(self):
        """read_rtd_temperature method for sdk adc module"""
        request = adc_pb.EmptyMsg()

        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.read_rtd_temperature(self.rpc_controller, request)

        response = get_server_response(rpc_response, adc_pb.TempReading)

        temp = response.temp

        return temp
