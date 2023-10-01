from random import *
from typing import *
import asyncio
import logging
import traceback
import sys
import re
from copy import deepcopy
import json

from .config import tabNumerique, tabAlphabetique, tabAlphanumerique, tabAlphabetiqueInsensitive, tabAlphanumeriqueInsensitive
from .utils import getLang

log = logging.getLogger(__name__)


allLetters = r"[^abcdefghijklmnopqrstuvwxyz]"
allVowels = r"[^aeiouy]"
allConsonants = r"[^bcdfghjklmnpqrstvwxz]"


def IdentifierStringToArrayIdentifierString(
    value,
    sep = ',',      
):
    regExpIdentifier = re.compile(r'[^a-zA-Z0-9\-_]')
    sep = sep if (
        type(sep) == str and
        len(sep) > 0
    ) else ','
    result: list = None
    if(
        type(value) in (list, tuple)
    ):
        result = deepcopy(value)
    elif(
        type(value) == str
    ):
        result = str(value).split(sep)

    if(result is not None):
        result = list(
            map(
                lambda element: re.sub(regExpIdentifier, '', element),
                result,
            )
        )

    return result

def ArrayIdentifierStringToIdentifierString(
    value,
    sep = ',',      
):
    regExpIdentifier = re.compile(r'[^a-zA-Z0-9\-_\,]')
    sep = sep if (
        type(sep) == str and
        len(sep) > 0
    ) else ','
    result: list = None

    if(
        type(value) in (list, tuple)
    ):
        result = sep.join(value)
    elif(
        type(value) == str
    ):
        result = value

    if(result is not None):
        result = re.sub(regExpIdentifier, '', result)

    return result


sep = ','
identifiersString = 'bi-lo_ng|dfdj,ntouba,celestin'
identifiers = IdentifierStringToArrayIdentifierString(
    identifiersString,
    sep,
)
identifiersStringRetro = ArrayIdentifierStringToIdentifierString(
    identifiers,
    sep,
)

def getNFirstLetter(value: str, length: int = 1):
    length = length if type(length) == int else 1
    if(not(type(value) in (int, float, str, bool))):
        return None
    return str(value)[:length]
def getVowels(value: str):
    sep: str = ''
    if type(value) == str and value is not None:
        res = ''
        for index, element in enumerate(re.sub(allVowels,"++++",value).split('++++')):
            res = res + (sep if index > 0 else '') + element.lower()
        return res
    return value
def getConsonants(value: str):
    sep: str = ''
    if type(value) == str and value is not None:
        res = ''
        for index, element in enumerate(re.sub(allConsonants,"++++",value).split('++++')):
            res = res + (sep if index > 0 else '') + element.lower()
        return res
    return value
def tocamelcase(value: str, allState: bool = False):
    allState = allState if type(allState) == bool else False
    if type(value) == str and value is not None:
        res = ''
        for index, element in enumerate(re.sub(r"[^a-zA-Z0-9]","++++",value).split('++++')):
            if allState == True:
                res = res + element.capitalize()
            else:
                res = res + ( element.capitalize() if index > 0 else element.lower() )
        return res
    return value
def toStringToSpecifFormat(value: str, sep: str = '-'):
    sep = sep if type(sep) == str and len(sep) > 0 else ''
    if type(value) == str and value is not None:
        res = ''
        for index, element in enumerate(re.sub(r"[^a-zA-Z0-9]","++++",value).split('++++')):
            res = res + (sep if index > 0 else '') + element.lower()
        return res
    return value
def sanitizeRouteaUrl(value: str):
    value = '/'.join(deepcopy(value).split('\\'))
    arrValue: list = value.split('/') if type(value) == str else []
    arrValue = list(
        map(
            lambda seg: toStringToSpecifFormat(value=seg, sep='-'),
            arrValue
        )
    )

    return '/'.join(arrValue)

def ucFirst(value: str):
    try:
        value = str(value)
        return value[0].upper() + value[1:].lower()
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        log.error(stack)

def RandomStr(typeStr = 'alphanumeric', lengthStr = 20, variationState = False, mapF = lambda data: data) :
    mapF = mapF if callable(mapF) else (lambda data: data)
    typesStr = ['alphanumeric', 'alphabetical', 'alphanumeric-insensitive', 'alphabetical-insensitive', 'numeric']
    typesStr_tab = {
        'alphanumeric': tabAlphanumerique,
        'alphabetical': tabAlphabetique,
        'alphanumeric-insensitive': tabAlphanumeriqueInsensitive,
        'alphabetical-insensitive': tabAlphabetiqueInsensitive,
        'numeric': tabNumerique,
    }
    typeStr = typeStr if typeStr in typesStr else typesStr[0]

    tabSelected = typesStr_tab[typeStr] if typeStr in list(typesStr_tab.keys()) else typesStr_tab[typesStr[0]]
    # print("> String - RandomStr | tabSelected:: ", tabSelected)
    # print("> String - RandomStr | typesStr:: ", typesStr)
    variationState = variationState if type(variationState) == bool else False
    lengthStr = randint(1, lengthStr) if variationState else lengthStr
    result = list(
        range(1, lengthStr + 1, 1)
    )
    result = ''.join(
        list(
            map(lambda x: choice(tabSelected), result)
        )
    )
    if type(result) in (int, float, str):
        result = mapF(result)

    return result
def RandomIdentifier(typeStr = 'alphanumeric', lengthStr = 20, variationState = False, mapF = lambda data: data):
    mapF = mapF if callable(mapF) else (lambda data: data)
    if not(lengthStr >= 2) :
        lengthStr = 2
    firstLength = 1
    lengthStrOther = lengthStr - 1
    firstLetter = RandomStr(typeStr='alphabetical', lengthStr=firstLength, variationState=False)
    otherLetters = RandomStr(typeStr=typeStr, lengthStr=lengthStrOther, variationState=variationState)
    resRI = firstLetter + otherLetters
    if type(resRI) in (int, float, str):
        resRI = mapF(resRI)
    # print("> String - RandomIdentifier | resRI:: ", resRI)
    return resRI


def urlToStringFormat(value: any):
    value = str(value) if type(value) in (str, int, float, bool) else None
    res: str = value

    occurrences = re.findall(r'<{1,1}([a-zA-Z0-9_]{1,})>{1,1}', value)

    for index, occurrence in enumerate(occurrences):
        res = res.replace('<' + occurrence + '>', '{' + occurrence + '}')

    return res