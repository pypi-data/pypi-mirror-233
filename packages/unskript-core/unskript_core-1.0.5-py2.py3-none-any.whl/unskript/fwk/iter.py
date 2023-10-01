#
# Copyright (c) 2021 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
from __future__ import annotations
from json import loads as json_loads
import sys
from typing import List

from jsonschema import ValidationError
from pydantic import BaseModel, Field
from unskript.schemas.iterator import TaskIteratorSchema, TaskPollSchema, TaskPollValueTypeEnum


class IterSchema(BaseModel):
    iter_list: list = Field(
        title='List',
        description='List of items to iterate on.'
    )
    iter_item: str = Field(
        title='Input Schema Field',
        description='Element of the list should be used for which input schema field.'
    )


class Iter():
    iterParams = {}

    def __init__(self, iter_params: str):
        res = json_loads(iter_params)
        mainModule = sys.modules["__main__"]
        for k, v in res.items():
            if v["constant"]:
                if k == "iter_list":
                    self.iterParams[k] = json_loads(v["value"])
                else:
                    self.iterParams[k] = v["value"]
            else:
                self.iterParams[k] = getattr(mainModule, v["value"])
        try:
            self.iterObject = IterSchema(**self.iterParams)
        except ValidationError as e:
            raise e

    def getIterObject(self):
        return self.iterObject


class IterCfg():

    def __init__(self, iter_cfg: str):

        self.iter_cfg = None
        if iter_cfg == None:
            return

        # parse the Iterator JSON
        iter = json_loads(iter_cfg)
        try:
            self.iter_cfg = TaskIteratorSchema(**iter)
        except ValidationError as e:
            return

        pass

    def getIterEnabled(self) -> bool:
        if self.iter_cfg == None or self.iter_cfg.iter_enabled is False:
            return False

        return True

    def getIterListIsConstant(self) -> bool:
        if self.iter_cfg == None or self.iter_cfg.iter_enabled is False:
            return False

        return self.iter_cfg.iter_list_is_const

    def getIterListName(self) -> str:
        if self.iter_cfg == None or self.iter_cfg.iter_enabled is False:
            return None

        if self.iter_cfg.iter_list_is_const is True:
            return None

        return self.iter_cfg.iter_list

    def getIterListValue(self) -> List:
        if self.iter_cfg == None or self.iter_cfg.iter_enabled is False:
            return None

        if self.iter_cfg.iter_list_is_const is False:
            return None

        return self.iter_cfg.iter_list

    def getIterParamName(self) -> str:
        if self.iter_cfg == None or self.iter_cfg.iter_enabled is False:
            return None

        return self.iter_cfg.iter_parameter


class PollCfg:
    def __init__(self, poll_cfg: str):
        self.poll_cfg = None
        if poll_cfg == None:
            return

        # parse the PollCfg JSON
        poll = json_loads(poll_cfg)
        try:
            self.poll_cfg = TaskPollSchema(**poll)
        except ValidationError as e:
            return

        print(self.poll_cfg)
        pass

    def getPollEnabled(self) -> bool:
        if self.poll_cfg != None:
            return self.poll_cfg.poll_enabled

        return False

    def getPollStepInterval(self) -> int:
        if self.getPollEnabled() is False:
            return None

        return self.poll_cfg.poll_step_interval

    def getPollTimeout(self) -> int:
        if self.getPollEnabled() is False:
            return None

        return self.poll_cfg.poll_timeout

    def getPollCheckIsValue(self) -> bool:
        if self.getPollEnabled() is False:
            return False

        if self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.string:
            return True
        elif self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.number:
            return True
        elif self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.boolean:
            return True
        else:
            return False

    def getPollCheckValueStr(self) -> str:
        if self.getPollEnabled() is False:
            return None

        if self.getPollCheckIsValue() is True and self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.string:
            return self.poll_cfg.poll_check_output_value

        return None

    def getPollCheckValueInt(self) -> int:
        if self.getPollEnabled() is False:
            return None

        if self.getPollCheckIsValue() is True and self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.number:
            return self.poll_cfg.poll_check_output_value

        return None

    def getPollCheckValueBool(self) -> bool:
        if self.getPollEnabled() is False:
            return None

        if self.getPollCheckIsValue() is True and self.poll_cfg.poll_check_output_type is TaskPollValueTypeEnum.boolean:
            return self.poll_cfg.poll_check_output_value

        return None

    # def getPollConditionCfg(self) -> str:
    #     if self.getPollEnabled() is False:
    #         return None
    #     return self.poll_cfg.poll_condition_lhs_cfg
