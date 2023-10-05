"""
Client for Din service. Utilizes ClientRpcChannel to send/receive and
serialize/deserialize messages
"""
from edgepirpc.protos import din_pb2 as din_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.services.din.din_pb_enums import DinPins
from edgepi_rpc_client.util.helpers import get_server_response

# pylint: disable=no-member
# pylint: disable=too-few-public-methods
class ClientDinService():
    """Client methods for Din Service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = din_pb.DinService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def digital_input_state(self, din_pin: DinPins):
        """digital_input_state method for sdk din module"""
        request = din_pb.DinPin(
            din_pin = din_pin.value
        )
        # Call SDK method through rpc channel
        rpc_response = self.service_stub.digital_input_state(self.rpc_controller, request)

        response = get_server_response(rpc_response, din_pb.State)

        return response.state_bool
