##
# Copyright (c) 2021 unSkript, Inc
# All rights reserved.
##

from typing import Union, Optional
from enum import Enum
from xmlrpc.client import boolean
from pydantic import BaseModel, Field

"""
    individual tasks can be iterated using an iterator
    this is a feature of the framework and the actual Action is
    oblivious of the iteration
"""
class TaskIteratorSchema(BaseModel):
    iter_enabled: bool = Field(
        title="Enable Iteration",
        description="Is the iterator enabled on this task"
    )
    iter_list_is_const: bool = Field(
        title="Loop over list is a constant",
    )
    iter_list: Union[list, str] = Field(
        title="Loop over list with given name or value",
    )
    iter_parameter: Union[str, list] = Field(
        title="Loop Parameter Mapping",
        description="Iterator will loop over list and use this dict to assign parameters from key"
    )


class TaskPollValueTypeEnum(str, Enum):
    boolean = "VALUE_TYPE_BOOL"
    string = "VALUE_TYPE_STR"
    number = "VALUE_TYPE_NUMBER"
    #expr = "VALUE_TYPE_EXP"


class TaskPollSchema(BaseModel):
    poll_enabled: bool = Field(
        title="Poll till specified condition is met",
        description="Is the poll enabled on this task"
    )
    poll_check_output_type: TaskPollValueTypeEnum = Field(
        title="Type",
        description="Type of output of value being polled"
    )
    poll_check_output_value: Union[bool, int, str] = Field(
        title="Value",
        description="Polling will end once the function returns this value"
    )
    # poll_condition_lhs_cfg: Optional[str]  = Field(
    #     title="Poll End condition",
    #     description="Polling will end once the function return value matches this expression",
    #     default="output"
    # )
    poll_step_interval: int = Field(
        title="Interval (secs)",
        description="Number of seconds to wait before retrying the poll"
    )
    poll_timeout: Optional[int] = Field(
        title="Timeout (secs)",
        description="Number of seconds before giving up on the poll, never if unspecified"
    )


# what do we do about timeout, how to indicate to user
# seems like exiting runbook is the usual out.
# one could also have the user specify a exception handler
