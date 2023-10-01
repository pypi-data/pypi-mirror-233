from typing import *
import asyncio
import logging
import os
import traceback
import sys
import json
import datetime
import re
import copy
import pytz
from copy import deepcopy

from jon.JON_sup import checkIfCorrectTypeSchema as checkIfCorrectTypeSchemaO, String as StringO, Number as NumberO, Boolean as BooleanO, Date as DateO, File as FileO, Enum as EnumO, NotInEnum as NotInEnumO, ChosenType as ChosenTypeO, Object as ObjectO, Array as ArrayO, Clone as CloneO

from werkzeug.datastructures import FileStorage


log = logging.getLogger(__name__)

def isFile(value: any) -> bool:
    res = (type(value) is FileStorage)
    return res
def checkIfCorrectTypeSchema(value: any):
    return (
        checkIfCorrectTypeSchemaO(value) or
        type(value) is File
    )


class String(StringO):
    pass
class Number(NumberO):
    pass
class Boolean(BooleanO):
    pass
class Date(DateO):
    pass
class File(FileO):
    pass
class Enum(EnumO):
    pass
class NotInEnum(NotInEnumO):
    pass
class ChosenType(ChosenTypeO):
    def choices(self, *values: list):
        self._choices = values if(
            len(
                list(
                    filter(
                        lambda val: checkIfCorrectTypeSchema(val),
                        values,
                    ),
                )
            ) > 0
        ) else None

        return self
    def getChoices(self,):
        return self._choices
class Object(ObjectO):
    def initStruct(self, values: dict):
        struct = {}
        try:
            values = values if type(values) == dict else {}

            otherValues = {}
            #subValues
            subValues = {}
            for index, key in enumerate(values):
                if(checkIfCorrectTypeSchema(values[key])):
                    subValues[key] = values[key]
                else:
                    otherValues[key] = values[key]
            struct = subValues

            #clone
            allClones: list = list(
                filter(
                    lambda val: (
                        type(val['value']) is Clone and
                        val['key'] and
                        val['value'].getTarget() is not None and
                        val['value'].getTarget() in subValues.keys()
                    ),
                    (
                        list(
                            map(
                                lambda key: {
                                    'key': key,
                                    'value': otherValues[key],
                                },
                                otherValues.keys(),
                            )
                        )
                    )
                )
            )
            allClones = list(
                map(
                    lambda val: {
                        'key': val['key'],
                        'value': subValues[val['value'].getTarget()].label(
                            "{parent}.{child}".format(parent = self.get_label(), child = val['key'])
                        ).lang(self._lang),
                    },
                    allClones,
                )
            )
            for index, data in enumerate(allClones):
                keyAC = data['key']
                valueAC = data['value']
                struct[keyAC] = valueAC

            for index, key in enumerate(struct):
                label = struct[key]._label
                if(label is None):
                    struct[key] = struct[key].label("{parent}.{child}".format(parent = self.get_label(), child = key))
                struct[key].set_lang(self._lang)

        except Exception as err:
            stack = str(traceback.format_exc())
            log.error(stack)
            struct = None
        return struct
    def typesValues(self, *values: list):
        self._types = list(
            filter(
                lambda type: checkIfCorrectTypeSchema(type),
                values,
            ),
        ) if type(values) in (list, tuple) else None

        # print("> JON.schemas | Object - typesValues - self._types:: ", self._types)

        self.typesValuesRule()

        return self
class Array(ArrayO):
    def types(self, *values: list):
        self._types = list(
            filter(
                lambda type: checkIfCorrectTypeSchema(type),
                values,
            ),
        ) if type(values) in (list, tuple) else None

        # print("> JON.schemas | Array - types - self._types:: ", self._types)

        self.typesRule()

        return self

class Clone(CloneO) :
    pass