"""Client enums to protobuf led enums"""
# pylint: disable=no-member
from enum import Enum, unique
from edgepirpc.protos import dout_pb2 as dout_pb

@unique
class DoutPins(Enum):
    """DoutPins Enum"""
    DOUT1 = dout_pb.DoutPins.DOUT1
    DOUT2 = dout_pb.DoutPins.DOUT2
    DOUT3 = dout_pb.DoutPins.DOUT3
    DOUT4 = dout_pb.DoutPins.DOUT4
    DOUT5 = dout_pb.DoutPins.DOUT5
    DOUT6 = dout_pb.DoutPins.DOUT6
    DOUT7 = dout_pb.DoutPins.DOUT7
    DOUT8 = dout_pb.DoutPins.DOUT8

@unique
class DoutTriState(Enum):
    """DoutPins Enum"""
    HI_Z = dout_pb.DoutTriState.HI_Z
    HIGH = dout_pb.DoutTriState.HIGH
    LOW = dout_pb.DoutTriState.LOW
