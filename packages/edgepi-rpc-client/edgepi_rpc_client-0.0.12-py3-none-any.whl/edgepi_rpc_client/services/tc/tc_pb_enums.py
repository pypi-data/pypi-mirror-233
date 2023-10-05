"""Client enums to protobuf tc enums"""
#pylint: disable=no-member
from enum import Enum, unique
from edgepirpc.protos import tc_pb2 as tc_pb

@unique
class ConvMode(Enum):
    """ConvMode Enum"""
    SINGLE = tc_pb.ConvMode.SINGLE
    AUTO = tc_pb.ConvMode.AUTO

@unique
class OpenCircuitMode(Enum):
    """OpenCircuitMode Enum"""
    DISABLED = tc_pb.OpenCircuitMode.DISABLED
    LOW_INPUT_IMPEDANCE = tc_pb.OpenCircuitMode.LOW_INPUT_IMPEDANCE
    MED_INPUT_IMPEDANCE = tc_pb.OpenCircuitMode.MED_INPUT_IMPEDANCE
    HIGH_INPUT_IMPEDANCE = tc_pb.OpenCircuitMode.HIGH_INPUT_IMPEDANCE

@unique
class CJMode(Enum):
    """CJMode Eum"""
    ENABLE = tc_pb.CJMode.ENABLE
    DISABLE = tc_pb.CJMode.DISABLE

@unique
class FaultMode(Enum):
    """FaultMode Enum"""
    COMPARATOR = tc_pb.FaultMode.COMPARATOR
    INTERRUPT = tc_pb.FaultMode.INTERRUPT

@unique
class NoiseFilterMode(Enum):
    """NoiseFilterMode Enum"""
    HZ_60 = tc_pb.NoiseFilterMode.HZ_60
    HZ_50 = tc_pb.NoiseFilterMode.HZ_50

@unique
class AvgMode(Enum):
    """AvgMode Enum"""
    AVG_1 = tc_pb.AvgMode.AVG_1
    AVG_2 = tc_pb.AvgMode.AVG_2
    AVG_4 = tc_pb.AvgMode.AVG_4
    AVG_8 = tc_pb.AvgMode.AVG_8
    AVG_16 = tc_pb.AvgMode.AVG_16

@unique
class TCType(Enum):
    """TCType Enum"""
    TYPE_B = tc_pb.TCType.TYPE_B
    TYPE_E = tc_pb.TCType.TYPE_E
    TYPE_J = tc_pb.TCType.TYPE_J
    TYPE_K = tc_pb.TCType.TYPE_K
    TYPE_N = tc_pb.TCType.TYPE_N
    TYPE_R = tc_pb.TCType.TYPE_R
    TYPE_S = tc_pb.TCType.TYPE_S
    TYPE_T = tc_pb.TCType.TYPE_T

@unique
class VoltageMode(Enum):
    """VoltageMode Enum"""
    GAIN_8 = tc_pb.VoltageMode.GAIN_8
    GAIN_32 = tc_pb.VoltageMode.GAIN_32

@unique
class CJHighMask(Enum):
    """CJHighMask Enum"""
    CJHIGH_MASK_ON = tc_pb.CJHighMask.CJHIGH_MASK_ON
    CJHIGH_MASK_OFF = tc_pb.CJHighMask.CJHIGH_MASK_OFF

@unique
class CJLowMask(Enum):
    """CJLowMask Enum"""
    CJLOW_MASK_ON = tc_pb.CJLowMask.CJLOW_MASK_ON
    CJLOW_MASK_OFF = tc_pb.CJLowMask.CJLOW_MASK_OFF

@unique
class TCHighMask(Enum):
    """TCHighMask Enum"""
    TCHIGH_MASK_ON = tc_pb.TCHighMask.TCHIGH_MASK_ON
    TCHIGH_MASK_OFF = tc_pb.TCHighMask.TCHIGH_MASK_OFF

@unique
class TCLowMask(Enum):
    """TcLowMask Enum"""
    TCLOW_MASK_ON = tc_pb.TCLowMask.TCLOW_MASK_ON
    TCLOW_MASK_OFF = tc_pb.TCLowMask.TCLOW_MASK_OFF

@unique
class OvuvMask(Enum):
    """OvuvMask Enum"""
    OVUV_MASK_ON = tc_pb.OvuvMask.OVUV_MASK_ON
    OVUV_MASK_OFF = tc_pb.OvuvMask.OVUV_MASK_OFF

@unique
class OpenMask(Enum):
    """OpenMask Enum"""
    OPEN_MASK_ON = tc_pb.OpenMask.OPEN_MASK_ON
    OPEN_MASK_OFF = tc_pb.OpenMask.OPEN_MASK_OFF

@unique
class DecBits4(Enum):
    """OpenMask Enum"""
    P0 = tc_pb.DecBits4.P0
    P0_5 = tc_pb.DecBits4.P0_5
    P0_75 = tc_pb.DecBits4.P0_75
    P0_875 = tc_pb.DecBits4.P0_875
    P0_9375 = tc_pb.DecBits4.P0_9375
    P0_4375 = tc_pb.DecBits4.P0_4375
    P0_1875 = tc_pb.DecBits4.P0_1875
    P0_0625 = tc_pb.DecBits4.P0_0625
    P0_5625 = tc_pb.DecBits4.P0_5625
    P0_8125 = tc_pb.DecBits4.P0_8125
    P0_6875 = tc_pb.DecBits4.P0_6875
    P0_25 = tc_pb.DecBits4.P0_25
    P0_125 = tc_pb.DecBits4.P0_125
    P0_625 = tc_pb.DecBits4.P0_625
    P0_3125 = tc_pb.DecBits4.P0_3125
    P0_375 = tc_pb.DecBits4.P0_375

@unique
class DecBits6(Enum):
    "DecBits6 Enum"
    P0 = tc_pb.DecBits6.P0_
    P0_015625 = tc_pb.DecBits6.P0_015625
    P0_03125 = tc_pb.DecBits6.P0_03125
    P0_046875 = tc_pb.DecBits6.P0_046875
    P0_0625 = tc_pb.DecBits6.P0_0625_
    P0_078125 = tc_pb.DecBits6.P0_078125
    P0_09375 = tc_pb.DecBits6.P0_09375
    P0_109375 = tc_pb.DecBits6.P0_109375
    P0_125 = tc_pb.DecBits6.P0_125_
    P0_140625 = tc_pb.DecBits6.P0_140625
    P0_15625 = tc_pb.DecBits6.P0_15625
    P0_171875 = tc_pb.DecBits6.P0_171875
    P0_1875 = tc_pb.DecBits6.P0_1875_
    P0_203125 = tc_pb.DecBits6.P0_203125
    P0_21875 = tc_pb.DecBits6.P0_21875
    P0_234375 = tc_pb.DecBits6.P0_234375
    P0_25 = tc_pb.DecBits6.P0_25_
    P0_265625 = tc_pb.DecBits6.P0_265625
    P0_28125 = tc_pb.DecBits6.P0_28125
    P0_296875 = tc_pb.DecBits6.P0_296875
    P0_3125 = tc_pb.DecBits6.P0_3125_
    P0_328125 = tc_pb.DecBits6.P0_328125
    P0_34375 = tc_pb.DecBits6.P0_34375
    P0_359375 = tc_pb.DecBits6.P0_359375
    P0_375 = tc_pb.DecBits6.P0_375_
    P0_390625 = tc_pb.DecBits6.P0_390625
    P0_40625 = tc_pb.DecBits6.P0_40625
    P0_421875 = tc_pb.DecBits6.P0_421875
    P0_4375 = tc_pb.DecBits6.P0_4375_
    P0_453125 = tc_pb.DecBits6.P0_453125
    P0_46875 = tc_pb.DecBits6.P0_46875
    P0_484375 = tc_pb.DecBits6.P0_484375
    P0_5 = tc_pb.DecBits6.P0_5_
    P0_515625 = tc_pb.DecBits6.P0_515625
    P0_53125 = tc_pb.DecBits6.P0_53125
    P0_546875 = tc_pb.DecBits6.P0_546875
    P0_5625 = tc_pb.DecBits6.P0_5625_
    P0_578125 = tc_pb.DecBits6.P0_578125
    P0_59375 = tc_pb.DecBits6.P0_59375
    P0_609375 = tc_pb.DecBits6.P0_609375
    P0_625 = tc_pb.DecBits6.P0_625_
    P0_640625 = tc_pb.DecBits6.P0_640625
    P0_65625 = tc_pb.DecBits6.P0_65625
    P0_671875 = tc_pb.DecBits6.P0_671875
    P0_6875 = tc_pb.DecBits6.P0_6875_
    P0_703125 = tc_pb.DecBits6.P0_703125
    P0_71875 = tc_pb.DecBits6.P0_71875
    P0_734375 = tc_pb.DecBits6.P0_734375
    P0_75 = tc_pb.DecBits6.P0_75_
    P0_765625 = tc_pb.DecBits6.P0_765625
    P0_78125 = tc_pb.DecBits6.P0_78125
    P0_796875 = tc_pb.DecBits6.P0_796875
    P0_8125 = tc_pb.DecBits6.P0_8125_
    P0_828125 = tc_pb.DecBits6.P0_828125
    P0_84375 = tc_pb.DecBits6.P0_84375
    P0_859375 = tc_pb.DecBits6.P0_859375
    P0_875 = tc_pb.DecBits6.P0_875_
    P0_890625 = tc_pb.DecBits6.P0_890625
    P0_90625 = tc_pb.DecBits6.P0_90625
    P0_921875 = tc_pb.DecBits6.P0_921875
    P0_9375 = tc_pb.DecBits6.P0_9375_
    P0_953125 = tc_pb.DecBits6.P0_953125
    P0_96875 = tc_pb.DecBits6.P0_96875
    P0_984375 = tc_pb.DecBits6.P0_984375
