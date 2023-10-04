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
import json
import sys

from jsonschema import ValidationError
from pydantic import BaseModel, Field


def eval_with_try(value, vars: None):
    try:
        return eval(value, vars)
    except (NameError, SyntaxError) as e:
        '''
        if the input was a string then return it as is.
        The NameError or SyntaxError is raised because the string is not enclosed in quotes

        >>> eval(foo)
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        NameError: name 'foo' is not defined

        >>> eval('kubectl get ns')
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<string>", line 1
            kubectl get ns
            ^
        SyntaxError: invalid syntax
        '''
        if isinstance(value, str):
            return value
        raise e
    except ValueError as e:
        print(f'ValueError: Could not evaluate argument {value}, {e}')
        raise e
    except Exception as e:
        print(f'Could not evaluate argument {value}, {e}')
        raise e


class CellParams():
    """
    CellParams is the class that will hold the input parameters
    for a given cell, the lego name and the schema with which
    the input parameters should be verified.
    """
    cellparams = {}
    data_dir = ''
    """
    input parameters are passed as json string to the following function.
    This is how the json string would look like
    {
        "db_name": {
            "constant": true,
            "value": "<input value>"
        }
    }
    """

    def __init__(self, input_schema_class_name, input_params: str):
        res = json.loads(input_params)
        mainModule = sys.modules["__main__"]
        inputSchema = input_schema_class_name.schema()
        for k, v in res.items():
            if v["constant"]:
                """
                For object and array type of fields, we need to do json.loads on the value.
                """
                if 'type' in inputSchema['properties'][k] and inputSchema['properties'][k]['type'] in ['array', 'object']:
                    self.cellparams[k] = json.loads(v["value"])
                else:
                    self.cellparams[k] = v["value"]
            else:
                # Do the type check
                if 'type' in v:
                    if type == 'Variable':
                        self.cellparams[k] = getattr(mainModule, v["value"])
                    else:
                        nbParamsObj = getattr(mainModule, "nbParamsObj")
                        self.cellparams[k] = nbParamsObj.get(v["value"])
                else:
                    self.cellparams[k] = getattr(mainModule, v["value"])

        try:
            self.inputObject = input_schema_class_name(**self.cellparams)
        except ValidationError as e:
            raise e

    def getInputObject(self):
        return self.inputObject

    def get_param(self, key: str) -> str:
        res = self.cellparams[key]
        if res is None:
            raise Exception("key %s not found", key)
        return res


class TaskParamsEvaluate():
    def __init__(self, v, iter):
        self.v = v
        self.iter = iter
        pass

    def evaluate(self, d: dict):
        newDict = {}
        for key, value in d.items():
            # the iter handlers have already evaluated this argument and stuffed it into iter as a value
            if value == "iter_item":
                assert (self.iter is not None)
                newDict[key] = self.iter
            elif isinstance(value, str) and value.startswith("iter.get"):
                assert (self.iter is not None)
                newDict[key] = eval_with_try(value, {'iter': self.iter})
            else:
                newDict[key] = eval_with_try(value, self.v)

        return newDict


class TaskParams():
    """
    TaskParams is the class that will hold the input parameters
    for a given cell, the lego name and the schema with which
    the input parameters should be verified.
    """

    """
    input parameters are passed as json string to the following function.
    This is how the json string would look like
    {
        "db_name": {
            "constant": true,
            "value": "<input value>"
        }
    }
    """

    def __init__(self, input_schema_class_name, input_params: str, iter_item=None, vars: dict() = None, inputIsJson=True):
        self.cellparams = {}
        self.inputObject = None

        if input_params is not None:
            e = TaskParamsEvaluate(vars, iter_item)
            """
            To support bash commands, wherein the inputParamsJson is just a string, not json string
            If its a string, its bash command
            """
            if inputIsJson:
                try:
                    params = json.loads(input_params, object_hook=e.evaluate)
                except NameError:
                    raise ValueError(
                        'Make sure to enclose the input within double quotes so that python can evaluate it, eg: "foo"')
            else:
                params = {"command": input_params}
            self.cellparams = params

        try:
            # self.inputObject = input_schema_class_name(**self.cellparams)
            self.inputObject = self.cellparams
        except ValidationError as e:
            raise e
        except TypeError as e:
            raise e

    def getInputObject(self):
        return self.inputObject

    def get_param(self, key: str) -> str:
        res = self.cellparams[key]
        if res is None:
            raise Exception("key %s not found", key)
        return res

    def get_params_kwargs(self):
        return self.cellparams
