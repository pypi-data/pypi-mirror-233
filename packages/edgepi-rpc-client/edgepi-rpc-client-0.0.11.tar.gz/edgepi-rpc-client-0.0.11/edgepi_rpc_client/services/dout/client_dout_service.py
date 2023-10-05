"""
Client for Dout service. Utilizes ClientRpcChannel to send/receive and
serialize/deserialize messages
"""
from edgepirpc.protos import dout_pb2 as dout_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.services.dout.dout_pb_enums import DoutPins, DoutTriState
from edgepi_rpc_client.util.helpers import get_server_response

# pylint: disable=no-member, too-few-public-methods
class ClientDoutService():
    """Client methods for Dout service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = dout_pb.DoutService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def set_dout_state(self, dout_pin: DoutPins, state:DoutTriState):
        """set_dout_state method for sdk dout module"""
        request = dout_pb.PinAndState(
            dout_pin = dout_pin.value,
            state = state.value
        )
        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.set_dout_state(self.rpc_controller,request)

        response = get_server_response(rpc_response, dout_pb.SuccessMsg)

        return response.content
