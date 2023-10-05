"""
Client for Dac service. Utilizes ClientRpcChannel to send/receive and
serialize/deserialize messages
"""
from edgepirpc.protos import dac_pb2 as dac_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.services.dac.dac_pb_enums import DACChannel
from edgepi_rpc_client.util.helpers import get_server_response

# pylint: disable=no-member
class ClientDacService():
    """Client methods for Dac Service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = dac_pb.DacService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def set_dac_gain(self, set_gain: bool, auto_code_change: bool = False):
        """set_dac_gain method for sdk dac module"""
        request = dac_pb.Gain(
            set_gain=set_gain,
            auto_code_change=auto_code_change
        )

        # Call SDK method through rpc channel
        rpc_response = self.service_stub.set_dac_gain(self.rpc_controller, request)

        response = get_server_response(rpc_response, dac_pb.GainState)

        return response.gain_state

    def write_voltage(self, analog_out: DACChannel, voltage: float):
        """write_voltage method for sdk dac module"""
        request = dac_pb.WriteVoltage(
            dac_channel=analog_out.value,
            voltage=voltage
        )

        rpc_response = self.service_stub.write_voltage(self.rpc_controller, request)

        response = get_server_response(rpc_response, dac_pb.SuccessMsg)

        return response.content

    def get_state(self, analog_out: DACChannel = None, code: bool = None,
                        voltage: bool = None, gain: bool = None):
        """get_state method for sdk dac module"""
        request = dac_pb.GetState(
            dac_channel=analog_out.value,
            code=code,
            voltage=voltage,
            gain=gain
        )

        rpc_response = self.service_stub.get_state(self.rpc_controller, request)

        response = get_server_response(rpc_response, dac_pb.State)

        return response.code_val, response.voltage_val, response.gain_state

    def reset(self):
        """reset method for sdk dac module"""
        request = dac_pb.EmptyMsg()

        rpc_response = self.service_stub.reset(self.rpc_controller, request)

        response = get_server_response(rpc_response, dac_pb.SuccessMsg)

        return response.content
