"""Client enums to protobuf led enums"""
# pylint: disable=no-member
from enum import Enum, unique
from edgepirpc.protos import led_pb2 as led_pb

@unique
class LEDPins(Enum):
    """LEDPins Enum"""
    LED1 = led_pb.LEDPins.LED1
    LED2 = led_pb.LEDPins.LED2
    LED3 = led_pb.LEDPins.LED3
    LED4 = led_pb.LEDPins.LED4
    LED5 = led_pb.LEDPins.LED5
    LED6 = led_pb.LEDPins.LED6
    LED7 = led_pb.LEDPins.LED7
    LED8 = led_pb.LEDPins.LED8
