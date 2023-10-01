##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

from typing import Optional
from pydantic import BaseModel, Field


class TaskStartConditionSchema(BaseModel):
    condition_enabled: bool = Field(
        title="Execute this Action only if the given condition evaluates to true",
        default=False
    )
    condition_cfg: str = Field(
        title="Boolean expression",
        description="Boolean expression to evaluate in order to start execution of this Action. Eg len(my_list) > 10"
    )
    condition_result: bool = Field(
        title="Truth value of boolean expression",
        default=True,
        description="Truth value of the given expression to compare against. true or false"
    )