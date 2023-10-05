"""
Client for tc service. Utilizes ClientRpcChannel to send/recieve
and serialize/deserialize messages.
"""
import logging
from edgepirpc.protos import tc_pb2 as tc_pb
from edgepi_rpc_client.util.helpers import (
    create_config_request_from_args, filter_arg_values, get_server_response
)
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
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

# pylint: disable=no-member
class ClientTcService():
    """Client Methods for Tc Service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = tc_pb.TcService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def _generate_faults_dict(self, faults_msg):
        faults_dict = {}

        for fault_msg in faults_msg.fault:
            faults_dict[fault_msg.fault_type] = {
                'Fault Type': fault_msg.fault_type,
                'At Fault': fault_msg.at_fault,
                'Fault Message': fault_msg.err_msg,
                'Fault Masked': fault_msg.is_masked
            }

        return faults_dict

    # pylint: disable=unused-argument, too-many-arguments, too-many-locals
    def set_config(self, conversion_mode: ConvMode = None,
        open_circuit_mode: OpenCircuitMode = None,
        cold_junction_mode: CJMode = None,
        fault_mode: FaultMode = None,
        noise_filter_mode: NoiseFilterMode = None,
        average_mode: AvgMode = None,
        tc_type: TCType = None,
        voltage_mode: VoltageMode = None,
        cj_high_mask: CJHighMask = None,
        cj_low_mask: CJLowMask = None,
        tc_high_mask: TCHighMask = None,
        tc_low_mask: TCLowMask = None,
        ovuv_mask: OvuvMask = None,
        open_mask: OpenMask = None,
        cj_high_threshold: int = None,
        cj_low_threshold: int = None,
        lt_high_threshold: int = None,
        lt_high_threshold_decimals: DecBits4 = None,
        lt_low_threshold: int = None,
        lt_low_threshold_decimals: DecBits4 = None,
        cj_offset: int = None,
        cj_offset_decimals: DecBits4 = None,
        cj_temp: int = None,
        cj_temp_decimals: DecBits6 = None,
    ):
        """set_config method for sdk tc module."""
        # Get a dictionary of arguments that are not None.
        config_args_dict= filter_arg_values(locals(), 'self', None)
        _logger.debug("Config argument dictionary: %s", config_args_dict)

        # Create config request
        config_msg = tc_pb.Config()
        arg_msg = tc_pb.Config().ConfArg()
        request = create_config_request_from_args(config_msg, arg_msg, config_args_dict)

        # Call the SDK method through the rpc channel client
        rpc_response = self.service_stub.set_config(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.SuccessMsg)

        return response.content

    def single_sample(self):
        """single_sample method for sdk tc module"""
        request = tc_pb.EmptyMsg()
        # call the SDK method through rpc channel client
        rpc_response = self.service_stub.single_sample(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.TempReading)

        temps = (response.cj_temp, response.lin_temp)

        return temps

    def read_temperatures(self):
        """read_temperatures method for sdk tc module"""
        request = tc_pb.EmptyMsg()
        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.read_temperatures(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.TempReading)

        temps = (response.cj_temp, response.lin_temp)

        return temps

    def read_faults(self,filter_at_fault = True):
        """read_faults method for sdk tc module"""
        request = tc_pb.FilterFaults()
        request.filter_at_fault = filter_at_fault

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.read_faults(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.Faults)

        result_dict = self._generate_faults_dict(response)

        return result_dict

    def clear_faults(self):
        """clear_faults method for sdk tc module"""
        request = tc_pb.EmptyMsg()

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.clear_faults(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.SuccessMsg)

        return response.content

    def reset_registers(self):
        """reset_registers method for sdk tc module"""
        request = tc_pb.EmptyMsg()

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.reset_registers(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.SuccessMsg)

        return response.content

    def overwrite_cold_junction_temp(self, cj_temp: int, cj_temp_decimals: DecBits6):
        """overwrite_cold_junction_temp for sdk tc module"""
        request = tc_pb.CJtemp(
            cj_temp = cj_temp,
            cj_temp_decimals = cj_temp_decimals.value
        )

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.overwrite_cold_junction_temp(self.rpc_controller,request)

        response = get_server_response(rpc_response, tc_pb.SuccessMsg)

        return response.content
