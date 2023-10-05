"""Client Enum to Protobuf Enum mapping"""
from enum import Enum, unique
from edgepirpc.protos import din_pb2 as din_pb

# pylint: disable=no-member
@unique
class DinPins(Enum):
    """DinPins Enum"""
    DIN1 = din_pb.DinPins.DIN1
    DIN2 = din_pb.DinPins.DIN2
    DIN3 = din_pb.DinPins.DIN3
    DIN4 = din_pb.DinPins.DIN4
    DIN5 = din_pb.DinPins.DIN5
    DIN6 = din_pb.DinPins.DIN6
    DIN7 = din_pb.DinPins.DIN7
    DIN8 = din_pb.DinPins.DIN8
