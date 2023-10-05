"""Client Enum to Protobuf Enum mapping"""
from enum import Enum, unique
from edgepirpc.protos import dac_pb2 as dac_pb

# pylint: disable=no-member
@unique
class DACChannel(Enum):
    """DACChannels Enum"""
    AOUT1 = dac_pb.DACChannels.AOUT1
    AOUT2 = dac_pb.DACChannels.AOUT2
    AOUT3 = dac_pb.DACChannels.AOUT3
    AOUT4 = dac_pb.DACChannels.AOUT4
    AOUT5 = dac_pb.DACChannels.AOUT5
    AOUT6 = dac_pb.DACChannels.AOUT6
    AOUT7 = dac_pb.DACChannels.AOUT7
    AOUT8 = dac_pb.DACChannels.AOUT8
