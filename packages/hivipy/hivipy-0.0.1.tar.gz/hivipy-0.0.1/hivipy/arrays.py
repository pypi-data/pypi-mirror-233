from typing import *
import asyncio
import logging
import traceback
import sys
import copy
import json
import numpy
import codecs
from copy import deepcopy
import pandas as pd
from werkzeug.local import LocalProxy

from .utils import cleanBodies, cleanBody, getClientVisitorDatas


log = logging.getLogger(__name__)

def getArrayAttributValueInArrayObject(
    values: 'list|tuple',
    attributName: str,
) -> 'list|tuple':
    if type(attributName) == str :
        attributName = deepcopy(str(attributName))
        values = deepcopy(list(values)) if type(values) in (list, tuple) else []
        return list(
            map(
                lambda value: value[attributName],
                (
                    tuple(
                        filter(
                            lambda value: (
                                type(value) == dict and
                                attributName in value.keys()
                            ),
                            values,
                        )
                    )
                ),
            )
        )
    return []
def checkIfArrayDataIsInArray(
    values: 'list|tuple',
    possibleValues: 'list|tuple',
    strict: bool = False,
):
    strict = strict if type(strict) == bool else False
    values = deepcopy(values) if type(values) in (list, tuple, str, int, float, bool, str) else []
    if not(type(values) in (list, tuple)):
        values = [values]
    values = deepcopy(list(values))
    possibleValues = deepcopy(list(possibleValues)) if type(possibleValues) in (list, tuple) else []
    allExists = list(
        map(
            lambda value: value in possibleValues,
            values,
        )
    )

    if strict == True :
        return not(
            False in allExists
        )
    return (
        True in allExists
    )


# namesOfActionsNT = ['find-all', 'count-all', 'find-one', 'exists', 'export', 'extract', 'extract-add', 'extract-update', 'extract-edit', 'add-multiple', 'update-multiple', 'edit-multiple', 'init', 'delete-multiple', 'archive-or-restore-multiple', 'block-or-unblock-multiple', 'add', 'update', 'edit', 'delete', 'archive-or-restore', 'block-or-unblock']
# checkRes = checkIfArrayDataIsInArray(
#     namesOfActionsNT,
#     ['find-all', 'count-all', 'find-one', 'exists', 'export', 'extract'],
#     strict = False,
# )

# print('[HIVIPY - ARRAY] namesOfActionsNT:: ', namesOfActionsNT)
# print('[HIVIPY - ARRAY] checkRes:: ', checkRes)