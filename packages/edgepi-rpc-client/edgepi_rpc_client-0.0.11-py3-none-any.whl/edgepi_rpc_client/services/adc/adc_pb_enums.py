"""Client enums to protobuf adc enums"""
from enum import Enum
from edgepirpc.protos import adc_pb2 as adc_pb

# pylint: disable=no-member
class AnalogIn(Enum):
    """AnalogIn Enum"""
    AIN1 = adc_pb.AnalogIn.AIN1
    AIN2 = adc_pb.AnalogIn.AIN2
    AIN3 = adc_pb.AnalogIn.AIN3
    AIN4 = adc_pb.AnalogIn.AIN4
    AIN5 = adc_pb.AnalogIn.AIN5
    AIN6 = adc_pb.AnalogIn.AIN6
    AIN7 = adc_pb.AnalogIn.AIN7
    AIN8 = adc_pb.AnalogIn.AIN8
    AINCOM = adc_pb.AnalogIn.AINCOM
    FLOAT = adc_pb.AnalogIn.FLOAT

class ADC1DataRate(Enum):
    """ADC1DataRate Enum"""
    SPS_2P5 = adc_pb.ADC1DataRate.SPS_2P5
    SPS_5 = adc_pb.ADC1DataRate.SPS_5
    SPS_10_ = adc_pb.ADC1DataRate.SPS_10_
    SPS_16P6 = adc_pb.ADC1DataRate.SPS_16P6
    SPS_20 = adc_pb.ADC1DataRate.SPS_20
    SPS_50 = adc_pb.ADC1DataRate.SPS_50
    SPS_60 = adc_pb.ADC1DataRate.SPS_60
    SPS_100_ = adc_pb.ADC1DataRate.SPS_100_
    SPS_400_ = adc_pb.ADC1DataRate.SPS_400_
    SPS_1200 = adc_pb.ADC1DataRate.SPS_1200
    SPS_2400 = adc_pb.ADC1DataRate.SPS_2400
    SPS_4800 = adc_pb.ADC1DataRate.SPS_4800
    SPS_7200 = adc_pb.ADC1DataRate.SPS_7200
    SPS_14400 = adc_pb.ADC1DataRate.SPS_14400
    SPS_19200 = adc_pb.ADC1DataRate.SPS_19200
    SPS_38400 = adc_pb.ADC1DataRate.SPS_38400

class ADC2DataRate(Enum):
    """ADC2DataRate Enum"""
    SPS_10 = adc_pb.ADC2DataRate.SPS_10
    SPS_100 = adc_pb.ADC2DataRate.SPS_100
    SPS_400 = adc_pb.ADC2DataRate.SPS_400
    SPS_800 = adc_pb.ADC2DataRate.SPS_800

class FilterMode(Enum):
    """FilterMode Enum"""
    SINC1 = adc_pb.FilterMode.SINC1
    SINC2 = adc_pb.FilterMode.SINC2
    SINC3 = adc_pb.FilterMode.SINC3
    SINC4 = adc_pb.FilterMode.SINC4
    FIR = adc_pb.FilterMode.FIR

class ConvMode(Enum):
    """ConvMode Enum"""
    CONTINUOUS = adc_pb.ConvMode.CONTINUOUS
    PULSE = adc_pb.ConvMode.PULSE

class ADCNum(Enum):
    """ADCNum Enum"""
    ADC_1 = adc_pb.ADCNum.ADC_1
    ADC_2 = adc_pb.ADCNum.ADC_2

class DiffMode(Enum):
    """DiffMode Enum"""
    DIFF_1 = adc_pb.DiffMode.DIFF_1
    DIFF_2 = adc_pb.DiffMode.DIFF_2
    DIFF_3 = adc_pb.DiffMode.DIFF_3
    DIFF_4 = adc_pb.DiffMode.DIFF_4
    DIFF_OFF = adc_pb.DiffMode.DIFF_OFF
    