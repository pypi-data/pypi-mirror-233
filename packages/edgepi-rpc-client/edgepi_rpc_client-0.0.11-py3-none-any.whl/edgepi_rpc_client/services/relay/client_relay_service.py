"""
Client for Relay Service
"""
from edgepirpc.protos import relay_pb2 as relay_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.util.helpers import get_server_response


# pylint: disable=no-member
class ClientRelayService():
    """Client methods for relay service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = relay_pb.RelayService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def open_relay(self):
        """open_relay method for sdk relay module"""
        request = relay_pb.EmptyMsg()

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.open_relay(self.rpc_controller,request)

        response = get_server_response(rpc_response, relay_pb.SuccessMsg)

        return response.content

    def close_relay(self):
        """close_relay method for sdk relay module"""
        request = relay_pb.EmptyMsg()

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.close_relay(self.rpc_controller,request)

        response = get_server_response(rpc_response, relay_pb.SuccessMsg)

        return response.content

    def get_state_relay(self):
        """get_state_relay method for sdk relay module"""
        request = relay_pb.EmptyMsg()

        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.get_state_relay(self.rpc_controller,request)

        response = get_server_response(rpc_response, relay_pb.State)

        return response.state_bool
