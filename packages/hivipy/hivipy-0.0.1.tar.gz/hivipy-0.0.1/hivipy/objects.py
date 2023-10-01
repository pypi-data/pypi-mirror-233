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

def mergeDict(*dicts: 'list|tuple') -> dict:
    values = {}
    dicts = tuple(
        filter(
            lambda value: type(value) == dict,
            dicts,
        )
    ) if type(dicts) in (list, tuple) else []

    for index, value in enumerate(dicts):
        values = {**values, **value}

    return values

def getArrayWithPossibleValues(values: list, possibleValues: list):
    possibleValues = possibleValues if type(possibleValues) in (list, tuple) else []
    values = values if type(values) in (list, tuple) else []

    return list(
        filter(
            lambda value: value in possibleValues,
            values,
        )
    )
def getDictAttributValueByAttributName(value: dict, attributName: str):
    # value = deepcopy(value)
    attributName = deepcopy(attributName)
    if not(
        type(value) == dict and 
        type(attributName) == str and
        len(attributName) > 0 and
        attributName in value.keys()
    ) :
        return None
    return value[attributName]

def objectToString(value: dict, encoder = "UTF-8"):
    value = cleanBody(value, encoder=encoder)
    return json.dumps(value, separators=(',', ':')) if type(value) == dict and len(value.keys()) > 0 else None
def listToString(value: dict, encoder = "UTF-8"):
    value = cleanBodies(value, encoder=encoder)
    return json.dumps(value, separators=(',', ':')) if type(value) in (list, tuple) else None

def mergeObjects(*objects):
    objects = list(
        filter(
            lambda obj: type(obj) == dict,
            objects,
        )
    )
    res = {} if type(objects) in (list, tuple) and len(objects) > 0 else None
    if res is not None:
        for index, obj in enumerate(objects):
            res.update(obj)

    return res

def getCleanedClientVisitorDatas(request: LocalProxy):
    return removeAttributesOfObject(getClientVisitorDatas(request))

def removeAttributesOfObject(
    data: dict,
    mapCheck = (lambda index, key, element, data: element is None),
    map = lambda index, key, element, data: element
):
    map = map if callable(map) else (lambda index, key, element, data: element)
    mapCheck = mapCheck if callable(mapCheck) else (lambda index, key, element, data: element is None)
    dataClone = None
    if type(data) == dict:
        data = dict(data)
        dataClone = dict(data)
        for index, (key, element) in enumerate(data.items()):
            data[key] = map(index=index, key=key, element=element, data=data)
            test: bool = mapCheck(index=index, key=key, element=data[key], data=data)
            if test == True:
                del dataClone[key]
        for index, (key, element) in enumerate(dataClone.items()):
            dataClone[key] = removeAttributesOfObject(data=dataClone[key], mapCheck=mapCheck, map=map)
    elif type(data) in (list, tuple):
        data = list(data)
        dataClone = list(data)
        for index, element in enumerate(data):
            key: int = index
            data[index] = map(index=index, key=index, element=element, data=data)
            test: bool = mapCheck(index=index, key=key, element=data[index], data=data)
            if test == True:
                del dataClone[index]
        for index, element in enumerate(data):
            dataClone[index] = removeAttributesOfObject(data=dataClone[index], mapCheck=mapCheck, map=map)
    else:
        # if(not(data is None)):
        dataClone = data
    return dataClone
def loopObject(data: dict, map = lambda index, key, element, data: element):
    map = map if callable(map) else (lambda index, key, element, data: element)
    if type(data) == dict:
        for index, (key, element) in enumerate(data.items()):
            data[key] = map(index=index, key=key, element=element, data=data)
            data[key] = loopObject(data=data[key], map=map)
    elif type(data) in (list, tuple):
        data = list(data)
        for index, element in enumerate(data):
            data[index] = map(index=index, key=index, element=element, data=data)
            data[index] = loopObject(data=data[index], map=map)
    return data

def pdDataframeToObject(data: pd.DataFrame, isArray: bool = False):
    isArray = isArray if type(isArray) == bool else False
    if type(data) is pd.DataFrame:
        data = data.replace({pd.NaT: None})
        data = tuple(data.T.to_dict().values()) if isArray == True else data.iloc[0].to_dict()
        return data
    else:
        return None

def loadJsonFile(filePath: str, mode: str = 'r', encoder: str = 'utf-8'):
    try:
        data = None
        mode = deepcopy(mode) if type(mode) == str and len(mode) > 0 else 'r'
        encoder = deepcopy(encoder) if type(encoder) == str and len(encoder) > 0 else 'utf-8'
        json_file = codecs.open(filePath, mode, encoder).read()
        data = json.loads(json_file) if (
            type(json_file) == str and
            len(json_file) > 0
        ) else None
        return data
    except: 
        stack = str(traceback.format_exc())
        log.error(stack)

        return None
    
def loopObjectV2(data: dict, parent: str = None, pos: int = 0, map = lambda index, key, element, data, parent, pos: element):
    map = map if callable(map) else (lambda index, key, element, data, parent, pos: element)
    parent = deepcopy(parent) if type(parent) == str and len(parent) > 0 else None
    pos = deepcopy(pos) if type(pos) in (int, float) else 0
    if type(data) == dict:
        for index, (key, element) in enumerate(data.items()):
            data[key] = map(index=index, key=key, element=element, data=data, parent=parent, pos=pos)
            data[key] = loopObjectV2(data=data[key], pos = pos + 1, parent=key, map=map)
    elif type(data) in (list, tuple):
        data = list(data)
        for index, element in enumerate(data):
            data[index] = map(index=index, key=index, element=element, data=data, parent=parent, pos=pos)
            data[index] = loopObjectV2(data=data[index], pos = pos + 1, parent=parent, map=map)
    return data

def strIsJsonType(data: str):
    data = data if type(data) == str and len(data) > 0 else None
    if data is not None:
        try:
            res = json.loads(deepcopy(data))
            return True
        except:
            return False
    else:
        return False
def strToJsonType(data: str):
    data = data if type(data) == str and len(data) > 0 else None
    if data is not None:
        try:
            res = json.loads(deepcopy(data))
            return res
        except:
            return None
    else:
        return None