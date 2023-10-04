##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from unskript.enums.enum_by_name import EnumByName
import enum


@enum.unique
class SizingOption(str, EnumByName):
    Add = "Add"
    Multiple = "Multiple"


@enum.unique
class StatisticsType(str, EnumByName):
    SAMPLE_COUNT = "SampleCount"
    AVERAGE = "Average"
    SUM = "Sum"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    PERCENTILE = "Percentile"
