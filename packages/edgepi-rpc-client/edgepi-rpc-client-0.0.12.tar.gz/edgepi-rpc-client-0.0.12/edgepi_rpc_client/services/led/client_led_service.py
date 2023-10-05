"""
Client for led service. Utilizes ClientRpcChannel to send/receive and
serialize/deserialize messages
"""
from edgepirpc.protos import led_pb2 as led_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.services.led.led_pb_enums import LEDPins
from edgepi_rpc_client.util.helpers import get_server_response

# pylint: disable=no-member
class ClientLEDService():
    """Client methods for LED service"""
    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = led_pb.LEDService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    def turn_led_on(self, led_pin: LEDPins):
        """turn_on led method for sdk led module"""
        request = led_pb.LEDPin(
            led_pin = led_pin.value
        )
        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.turn_led_on(self.rpc_controller,request)

        response = get_server_response(rpc_response, led_pb.SuccessMsg)

        return response.content

    def turn_led_off(self, led_pin: LEDPins):
        """turn_off led method for sdk led module"""
        request = led_pb.LEDPin(
            led_pin = led_pin.value
        )
        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.turn_led_off(self.rpc_controller,request)

        response = get_server_response(rpc_response, led_pb.SuccessMsg)

        return response.content

    def toggle_led(self, led_pin: LEDPins):
        """toggle_led method for sdk led module"""
        request = led_pb.LEDPin(
            led_pin = led_pin.value
        )
        # Call SDK method through rpc channel client
        rpc_response = self.service_stub.toggle_led(self.rpc_controller,request)

        response = get_server_response(rpc_response, led_pb.SuccessMsg)

        return response.content
