from typing import *
import asyncio
import logging
import traceback
import sys
import re
import copy
import math
import json
import pygeoip
from random import *
from datetime import datetime, date
from dateutil.parser import parse
from urllib.parse import urljoin, urlencode
from copy import deepcopy
from google_currency import convert as CurrencyConvert
import pandas as pd
import csv
import requests
import html
from deep_translator import GoogleTranslator

from sqlalchemy import null
from werkzeug.datastructures import FileStorage
from werkzeug.local import LocalProxy

from .config import langs, langCodes, pagesPossibles, tabNumerique, tabAlphabetique, tabAlphanumerique
from .hivi_init import Manager, createDir, createStaticMediaPath
from .config import pagesPossibles, responsesPossibles


manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)



def JSONStringify(value):
    try:
        res = json.dumps(value, ensure_ascii=False)
        if res is not None:
            res = html.unescape(deepcopy(str(res)))
        return res
    except Exception as err:
        stack = str(traceback.format_exc())
        # log.error(stack)
        return None

def dataBinding(value):
    return "{{" + ("{0}".format(value)) + "}}"

def translateText(value: str, startLang: str = None, endLang: str = 'fr'):
    try:
        startLang = getLang(startLang) if type(startLang) == str else 'auto'
        endLang = getLang(endLang) if type(endLang) == str else 'en'
        value = value if type(value) == str and len(value) > 0 else None
        
        # print('--> translateText - startLang:: ', startLang)
        # print('--> translateText - endLang:: ', endLang)
        # print('--> translateText - value:: ', value)

        translations = GoogleTranslator(source=startLang, target=endLang).translate(value)
        # print('--> translateText - translations:: ', translations)
        res = translations if type(translations) == str and len(translations) > 0 else None
        return res
    except Exception as err:
        stack = str(traceback.format_exc())
        log.error(stack)
        return None

def CurrencyConverterLimited(amount, oldCur: str, newCur: str):
    try:
        url = 'https://api.exchangerate.host/latest?base={base}'.format(
            base = newCur
        )
        response = requests.get(url)
        data = response.json()

        if(
            amount is not None and
            type(data) == dict and
            'rates' in data.keys() and
            type(data['rates']) == dict and
            oldCur in data['rates'].keys() and
            Manager().isNumber(data['rates'][oldCur])
        ):
            rate = data['rates'][oldCur]
            return amount / rate    
        return None
    except: 
        stack = str(traceback.format_exc())
        log.error(stack)

        return None
def CurrencyGoogleConverter(amount, oldCur: str, newCur: str):
    try:
        res = CurrencyConvert(currency_from=oldCur, currency_to=newCur, amnt=amount)
        if(
            amount is not None and
            type(res) in (str, bytes)
        ):
            result = float(json.loads( res )['amount'])
            return result if not(result == 0 and amount != 0 and oldCur != newCur) else None
        return None
    except: 
        stack = str(traceback.format_exc())
        log.error(stack)

        return None
def CurrencyConverter(amount, oldCur: str, newCur: str):
    result1 = CurrencyGoogleConverter(amount = amount, oldCur=oldCur, newCur=newCur)
    print('--> CurrencyConverter - result1:: ', result1)
    if result1 is not None:
        return result1
    result2 = CurrencyConverterLimited(amount = amount, oldCur=oldCur, newCur=newCur)
    print('--> CurrencyConverter - result2:: ', result2)
    return result2
    

def getDisplayable(
    displayable: tuple,
    displayablePossibilities: tuple = (),
    defaultDisplayable: tuple = (),
    noDataLabel = None,
    supAction = (lambda res, displayable, displayablePossibilities, defaultDisplayable, noDataLabel: res),
):
    supAction = supAction if callable(supAction) else (lambda res, displayable, displayablePossibilities, defaultDisplayable, noDataLabel: res)
    noDataLabel = copy.deepcopy(noDataLabel if type(noDataLabel) == str and len(noDataLabel) > 0 else None)
    displayablePossibilities = copy.deepcopy(displayablePossibilities if type(displayablePossibilities) in (list, tuple) else ())
    displayablePossibilities = displayablePossibilities if noDataLabel is None else tuple(list(displayablePossibilities) + list([noDataLabel]))
    defaultDisplayable = copy.deepcopy(defaultDisplayable if type(defaultDisplayable) in (list, tuple) and len(defaultDisplayable) > 0 else displayablePossibilities)
    
    displayable = copy.deepcopy(list(
        filter(
            lambda x: x in displayablePossibilities,
            displayable,
        )
    ) if type(displayable) in (list, tuple) else ())
    displayable = displayable if len(displayable) > 0 else defaultDisplayable

    res = (displayable if not(noDataLabel is not None and noDataLabel in displayable) else [])
    return supAction(
        res = res,
        displayable = displayable,
        displayablePossibilities = displayablePossibilities,
        defaultDisplayable = defaultDisplayable,
        noDataLabel = noDataLabel,
    )

def getAccessTokenCode(authorizationContent: str):
    authorizationContent = authorizationContent if type(authorizationContent) == str else None
    authorizationContentArr = authorizationContent.split(" ") if authorizationContent is not None else None
    res = authorizationContentArr[1] if (
        authorizationContent is not None and
        len(authorizationContentArr) == 2 and
        authorizationContentArr[0] == 'Bearer'
    ) else None

    return res



def getPurIdBody(
    body
):
    # body = deepcopy(body)
    if type(body) == dict:
        id = body['id'] if (
            'id' in body.keys()
        ) else None
        _id = body['_id'] if '_id' in body.keys() else None
        slug = body['slug'] if (
            _id is None and
            'slug' in body.keys()
        ) else _id

        finalId = (slug if slug else id)

        return finalId
    return None
def getIdBody(
    body,
    mapAction = (
        lambda id, _id: ({
            '_or': [
                {
                    'id': {
                        '$eq': id
                    },
                },
                {
                    'slug': {
                        '$eq': _id,
                    },
                },
            ]
        })
    ),
    elseValue = {
        '_or': [
            {
                'id': {
                    '$eq': None,
                },
            },
            {
                'slug': {
                    '$eq': None,
                },
            },
        ]
    },
):
    # body = deepcopy(body)

    mapAction = mapAction if callable(mapAction) else lambda id, _id: ({
        '_or': [
            {
                'id': {
                    '$eq': id,
                },
            },
            {
                'slug': {
                    '$eq': _id,
                },
            },
        ]
    })
    elseValue = elseValue if type(elseValue) == dict else {
        '_or': [
            {
                'id': {
                    '$eq': None,
                },
            },
            {
                'slug': {
                    '$eq': None,
                },
            },
        ]
    }
    # print('---> getIdBody -- body::: ', body)
    if type(body) == dict:
        id = body['id'] if (
            'id' in body.keys()
        ) else None
        _id = body['_id'] if '_id' in body.keys() else None
        slug = body['slug'] if (
            _id is None and
            'slug' in body.keys()
        ) else _id

        finalId = (slug if slug else id)
        res = mapAction(id, finalId)
        # print('---> getIdBody -- finalId::: ', finalId)
        # print('---> getIdBody -- _id::: ', _id)
        # print('---> getIdBody -- res::: ', res)
        return res
    return elseValue

def cleanBody(body: any, files = None, encoder = "UTF-8"):
    if(type(body) in (str, bytes)):
        body = json.loads( body.decode(encoder) )
    elif(type(body) == dict):
        body = body if type(body) == dict else {}
    else :
        body = {}
    files = files if type(files) == dict else {}

    resCB = body
    resCB.update(files)

    return resCB
def cleanBodies(bodies: any, files = None, encoder = "UTF-8"):
    if(type(bodies) in (str, bytes)):
        bodies = json.loads( bodies.decode(encoder) )
    elif(type(bodies) in (list, tuple)):
        bodies = list(
            filter(
                lambda body: type(body) == dict,
                bodies,
            )
        ) if type(bodies) in (list, tuple) else []
    else :
        bodies = []
    files = files if type(files) == dict else {}

    clonedBodies = []
    for index, val in enumerate(bodies):
        val.update(files)
        clonedBodies.append(val)

    resCB = clonedBodies

    return resCB

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
def CRUDCleanFinalDatas(data: any, exclusion: 'list | tuple' = None, singleid: bool = False):
    singleid = deepcopy(singleid) if type(singleid) == bool else False
    allExclusions: list = [r'(\w{0,})(id{1})(s{0,})'] if singleid == True else [
        r'(\w{0,})(id{1})(s{0,})',
        r'(\w{0,})(objectid{1})',
    ]
    allExclusions = deepcopy(allExclusions) + (
        exclusion if type(exclusion) in (list, tuple) else []
    )
    # data = data
    if type(data) == str and strIsJsonType(data):
        data = strToJsonType(data)

    if type(data) == dict :
        res: dict = {}
        for key, value in data.items():
            if len(
                list(
                    filter(
                        lambda exclusion: re.compile(exclusion).search(key),
                        allExclusions,
                    )
                )
            ) <= 0 :
                if type(value) == dict:
                    value = CRUDCleanFinalDatas(value, exclusion = exclusion, singleid = singleid)
                res[key] = value
        return res
    elif type(data) in (list, tuple):
        res: list = list(
            map(
                lambda value: CRUDCleanFinalDatas(value, exclusion = exclusion, singleid = singleid),
                data,
            )
        )
        return res
    return data
def CRUDCleanFinalDatas2(data: any, exclusion: 'list | tuple' = None, singleid: bool = False):
    singleid = deepcopy(singleid) if type(singleid) == bool else False
    allExclusions: list = ['id'] if singleid == True else ['id', 'objectid']
    allExclusions = deepcopy(allExclusions) + (
        exclusion if type(exclusion) in (list, tuple) else []
    )
    # data = data
    if type(data) == str and strIsJsonType(data):
        data = strToJsonType(data)

    if type(data) == dict :
        res: dict = {}
        for key, value in data.items():
            if not(key in allExclusions):
                res[key] = value
        return res
    elif type(data) in (list, tuple):
        res: list = list(
            map(
                lambda value: CRUDCleanFinalDatas2(value, exclusion = exclusion, singleid = singleid),
                data,
            )
        )
        return res
    return data



def getInternalUrl(path: str, params = {}):
    try:
        path = path if type(path) == str and len(path) > 0 else None
        params = params if type(params) == dict else {}
        structConf = Manager().getStructConfig()
        primaryUrl: str = urljoin(structConf['baseUrl'], path)
        strParams = urlencode(params, doseq=True)
        finalUrl: str = primaryUrl + (
            "?" + strParams if (type(params) == dict and len(params.keys()) > 0) else ""
        )
        return finalUrl
    except: 
        stack = str(traceback.format_exc())
        log.error(stack)

        return None

def getClientVisitorDatas(request: LocalProxy):
    geo = pygeoip.GeoIP(createStaticMediaPath('geolocation','GeoLiteCity.dat'), pygeoip.MEMORY_CACHE)
    res = dict({
        'ipaddress': request.remote_addr,
        'browser': request.user_agent.browser,
        'version': request.user_agent.version and int(request.user_agent.version.split('.')[0]),
        'platform': request.user_agent.platform,
        'uas': request.user_agent.string,
        'geo_data': geo.record_by_addr(request.remote_addr),
    })
    return res

def LoopList(data, loop, typeLoop = 'filter'):
    data = list(data[:]).copy() if type(data) in (list, tuple) else []
    loop = loop if callable(loop) else lambda x: x
    typeLoop = typeLoop if typeLoop in ['filter', 'map'] else 'filter'
    res = []
    if(typeLoop == 'map'):
        for index, value in enumerate(data):
            element = data[index]
            res.append(loop(copy.deepcopy(element)))
            if(index > 2):
                break
    elif(typeLoop == 'filter'):
        for index, value in enumerate(data):
            element = data[index]
            if(loop(copy.deepcopy(element))):
                res.append(copy.deepcopy(element))
            if(index > 2):
                break

    return res

def TranslateTextWithTranslations(texte, translations):
    texte = texte if (
        type(texte) == str
        and len(texte) > 0
    ) else ''
    translations = translations if (
        type(translations) in (list, tuple)
        and len(translations) > 0
    ) else []
    res = {'en': texte, 'fr': texte}
    # print("> TranslateTextWithTranslations - translations:: ", translations)
    if len(translations) > 0:
        for content in translations[0]['contents']:
            res[content['lang']] = texte
            
    for translation in translations:
        translationCode = translation['code'] if (
            type(translation) == dict
            and 'code' in translation
            and type(translation['code']) == str
            and len(translation['code']) > 0
        ) else None
        translationContents = translation['contents'] if (
            type(translation) == dict
            and 'contents' in translation
            and type(translation['contents']) in (list, tuple)
            and len(translation['contents']) > 0
        ) else []
        if translationCode and len(translationContents) > 0:
            for content in translationContents:
                # print("> TranslateTextWithTranslations - res:: ", res)
                res[content['lang']] = str(res[content['lang']]).replace(
                    '$translate{{' + translationCode + '}}'
                    , content['content']
                )  
    return res
def GetTree(
    datas
    , labelCode = 'code'
    , labelParentCode = 'parent_code'
    , parentValue = None
    , labelChildrenCode = 'children'
    , labelChildrenLengthCode = 'children_length'
):
    datas = datas if type(datas) in (list, tuple) else []
    labelCode = labelCode if type(labelCode) == str and len(labelCode) > 0 else 'code'
    labelParentCode = labelParentCode if type(labelParentCode) == str and len(labelParentCode) > 0 else 'parent_code'
    labelChildrenCode = labelChildrenCode if type(labelChildrenCode) == str and len(labelChildrenCode) > 0 else 'children'
    labelChildrenLengthCode = labelChildrenLengthCode if type(labelChildrenLengthCode) == str and len(labelChildrenLengthCode) > 0 else 'children_length'

    def GetTreeChildren(value, parentValue):
        res_gtc = list(
            filter(
                lambda x: x[labelParentCode] == value[labelCode],
                datas,
            )
        )
        # value[labelChildrenCode] = res_gtc
        value[labelChildrenCode] = res_gtc
        value[labelChildrenCode] = list(
            map(
                lambda x: GetTreeChildren(x, value[labelCode]),
                value[labelChildrenCode]
            )
        )
        value[labelChildrenLengthCode] = len(value[labelChildrenCode])
        return value


    res = list(
        filter(
            lambda x: x[labelParentCode] == parentValue,
            datas,
        )
    )
    if type(res) in (list, tuple) :
        res = list(
            map(
                lambda x: GetTreeChildren(x, parentValue),
                res 
            )
        )
    else: 
        res = []
    return res

def ConvertToBool(value, default = False):
    default = default if type(default) == bool else False
    value = value.lower() if type(value) == str and len(value) > 0 else value
    if (value in [True, 'true', 't', 'vrai', 'v', 1]):
        result = True
    elif (value in [False, 'false', 'f', 'faux', 0]):
        result = False
    else:
        result = default

    return result


def ConvertMediasValue(media):
    media['value'] = ConvertForBase64File(media['value'])
    return media

def ConvertForBase64File(file):
    result = None
    if(
        type(file) in (list, tuple)
        and len(file) > 0
    ) :
        result = str(''.join(file))
    elif(
        type(file) == str
        and len(file) > 0
    ) :
        result = str(file)
    return result
def RetroConvertForBase64File(file):
    # len_max = 256
    len_max = 100000
    result = []
    if(
        type(file) == str
        and len(file) > 0
    ) :
        result = tuple(
            map(
                lambda x: file[x['e1']:x['e2']],
                tuple(
                    map(
                        lambda x: {'e1': x, 'e2': x+len_max},
                        tuple(range(0, len(file), len_max))
                    )
                )
            )
        )
    elif (
        type(file) in (list, tuple)
    ):
        result = file
    return result


def InitListObjectsFile(data):
    data = data if (
        type(data) == dict
        and 'value' in data.keys()
        and 'type' in data.keys()
        and type(data['type']) == str
    ) else {
        'value': None,
        'type': 'img',
    }
    data['value'] = RetroConvertForBase64File(data['value'])
    return data

def GetStaticFile(fileUrl):
    manager = Manager()
    structConf = manager.getStructConfig()
    return createDir(structConf['staticFolder'], fileUrl)

def GetIterableWithIndex(dataArray):
    result = []
    if type(dataArray) in [list, tuple] :
        for key, value in enumerate(dataArray):
            if type(value) in [list, tuple] :
                result.append([key+1] + value)

    return result

def DateDiffInSeconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def CleanAlert(alert):
    if not(
        type(alert) == dict and
        'type' in alert.keys() and
        type(alert['type']) == str and
        len(alert['type']) > 0 and
        'message' in alert.keys() and
        type(alert['message']) == str and
        len(alert['message']) > 0
    ) :
        alert = {
            'visible': False
        }
    else :
        alert['visible'] = True
    return alert

def PagesSelects(lengthElements, page, pages = 25):
    lengthElements = lengthElements if type(lengthElements)==int else 0
    page = page if type(page)==int else 0
    pages = pages if pages in pagesPossibles else pagesPossibles[0]
    pagesForPS = pages if pages != pagesPossibles[0] else lengthElements
    lengthPage = math.floor( lengthElements / pagesForPS )
    lengthPage = lengthPage if lengthPage >= 1 else 1
    lengthPageSelects = 3
    lps = lengthPageSelects
    pagesSelects = []

    if not(lengthElements > 0):
        pagesSelects = []
    elif page == 1:
        lps = lps + 1
        lps = lps if lps >= 1 else 1
        pagesSelects = list(range(1, lps, 1))
    elif page >= lengthPage:
        lps = lps - 1
        lps = lps if lps >= 1 else 1
        pagesSelects = list(range(lengthPage - lps, lengthPage + 1, 1))
    else:
        lps = math.floor( (lps-1) / 2 )
        lps = lps if lps >= 1 else 1
        pagesSelects = list(range(page - lps, page + lps + 1, 1))
        ## print('> lps::', lps)
        ## print('> page::', page)
    pagesSelects = list(
        filter(
            lambda x: x > 0 and x <= lengthPage,
            pagesSelects
        )
    )
    ## print('> utils | PagesSelects | lengthElements:: ', lengthElements)
    ## print('> utils | PagesSelects | page:: ', page)
    ## print('> utils | PagesSelects | pages:: ', pages)
    ## print('> utils | PagesSelects | lengthPage:: ', lengthPage)
    ## print('> utils | PagesSelects | lengthPageSelects:: ', lengthPageSelects)
    ## print('> utils | PagesSelects | pagesSelects:: ', pagesSelects)
    return {
        'ps':pagesSelects,
        'max': lengthPage
    }

def CleanName(
    nameValue,
    supCharacterAuthorised = ['_', '.'],
    changeBy = '',
    join = True
):
    result = None
    if type(nameValue) == str or type(nameValue) == int or type(nameValue) == float:
        nameValue = str(nameValue)
        tabAuth = tabAlphanumerique[:]
        for data in supCharacterAuthorised:
            tabAuth.append(data)
        result = list(nameValue)
        result = list(
            map(
                lambda x: x if x in tabAuth else changeBy,
                result
            )
        )
        if join == True:
            for data in supCharacterAuthorised:
                result = changeBy.join(result)
                result = result.split(data)
                result = result[0] + changeBy.join(
                    list(
                        map(
                            lambda x: x.capitalize(),
                            result[1:]
                        )
                    )
                )
        else:
            result = ''.join(result)
            result = result.split(changeBy)
            result = list(
                filter(
                    lambda x: len(x) > 0,
                    result
                )
            )
    return result

def getLang(lang):
    result = lang
    result = result if result in langs else 'fr'
    return result
def getLangCode(lang):
    return langCodes[getLang(lang)]
def cleanBody(body: any, files = None, encoder = "UTF-8"):
    if(type(body) in (str, bytes)):
        body = json.loads( body.decode(encoder) )
    elif(type(body) == dict):
        body = body if type(body) == dict else {}
    else :
        body = {}
    files = files if type(files) == dict else {}

    resCB = body
    resCB.update(files)

    return resCB
def cleanBodies(bodies: any, files = None, encoder = "UTF-8"):
    if(type(bodies) in (str, bytes)):
        bodies = json.loads( bodies.decode(encoder) )
    elif(type(bodies) in (list, tuple)):
        bodies = list(
            filter(
                lambda body: type(body) == dict,
                bodies,
            )
        ) if type(bodies) in (list, tuple) else []
    else :
        bodies = []
    files = files if type(files) == dict else {}

    clonedBodies = []
    for index, val in enumerate(bodies):
        val.update(files)
        clonedBodies.append(val)

    resCB = clonedBodies

    return resCB


def convertToOtherType(element, typeElement = None):
    result = None
    typeElement = typeElement if typeElement in [int, float, bool, str, list, tuple, dict, datetime] else None
    if typeElement :
        try:
            if element != None:
                if typeElement == datetime :
                    result = parse(element)
                if (
                    typeElement == bool
                    and (
                        (
                            type(element) == str
                            and element.lower() in ['true', 't', '1', 'false', 'f', '0']
                        ) or (
                            type(element) == bool
                        ) or (
                            element in [0,1]
                        )
                    )
                ) :
                    result = True if (
                        element in ['true', 't', '1', 1, True]
                    ) else False
                else:
                    result = typeElement(element)
            """if(typeElement == int):
                result = int(element)
            elif(typeElement == float):
                result = float(element)
            elif(typeElement == bool):
                result = bool(element)
            elif(typeElement == list):
                result = list(element)
            elif(typeElement == tuple):
                result = tuple(element)
            elif(typeElement == dict):
                result = dict(element)
            else:
                result = None"""
        except Exception as e:
            #raise
            result = None
    return 

def ElementForUpdate(
    oldElement: any,
    newElement: any,
    nullableAttributes: list = [],
    strictColumns: bool = True,
):
    try:
        strictColumns = strictColumns if type(strictColumns) == bool else True
        nullableAttributes = list(
            filter(
                lambda x: type(x) == str and len(x) > 0,
                nullableAttributes,
            ),
        ) if type(nullableAttributes) in (list, tuple) else []
        oldElement = oldElement if type(oldElement) == dict else {}
        newElement = newElement if type(newElement) == dict else {}

        newElementClone = {}
        for index, key in enumerate(newElement):
            value = newElement[key]
            if(value is None and key in nullableAttributes):
                newElementClone[key] = None
            elif(value is not None):
                newElementClone[key] = value
        newElement = newElementClone
        oldElementClone = {}
        for index, key in enumerate(oldElement):
            value = oldElement[key]
            if(value is None and key in nullableAttributes):
                oldElementClone[key] = None
            elif(value is not None):
                oldElementClone[key] = value
        oldElement = oldElementClone

        if(strictColumns == True):
            oldElementClone = {}
            for index, key in enumerate(oldElement):
                value = oldElement[key]
                if(key in newElement.keys()):
                    oldElementClone[key] = value
            oldElement = oldElementClone

        allKeysElement = list(dict.fromkeys(
            list(oldElement.keys()) + list(newElement.keys())
        ))
        # print('---> allKeysElement:: ', allKeysElement)
        res = {}
        for index, key in enumerate(allKeysElement):
            value = oldElement[key] if key in oldElement.keys() else None
            newValue = newElement[key] if key in newElement.keys() else None
            finalValue = None

            if(
                (
                    # not(key in nullableAttributes) and
                    (
                        value or
                        type(value) == bool or
                        value is None
                    )
                )
            ):
                if(
                    type(newValue) in (int, float, str, bool) or
                    type(newValue) is FileStorage or
                    type(newValue) is datetime or
                    type(newValue) is date
                ):
                    finalValue = newValue
                elif(
                    type(newValue) == dict and
                    len(newValue.keys()) <= 0 and
                    type(value) == dict
                ):
                    finalValue = value
                elif(
                    type(newValue) == dict and
                    type(value) == dict
                ):
                    finalValue = ElementForUpdate(
                        oldElement=value,
                        newElement=newValue,
                        nullableAttributes=nullableAttributes,
                        strictColumns=strictColumns,
                    )
                elif(
                    type(newValue) in (list, tuple) and
                    type(value) in (list, tuple)
                ):
                    finalValue = newValue
                else:
                    finalValue = newValue
            elif(
                key in nullableAttributes and
                value is None and
                newElement[key] is None
            ):
                finalValue = newElement[key]
            else:
                finalValue = value
            
            res[key] = finalValue
        """
        res = {}
        for index, key in enumerate(oldElement):
            value = oldElement[key]
            finalValue = None
            if(
                (
                    # not(key in nullableAttributes) and
                    (
                        value or
                        type(value) == bool or
                        value is None
                    ) and
                    (
                        key in newElement.keys() and (
                            newElement[key] or
                            type(newElement[key]) == bool or
                            newElement[key] is None
                        )
                    )
                )
            ):
                if(
                    type(newElement[key]) in (int, float, str, bool) or
                    type(newElement[key]) is FileStorage or
                    type(newElement[key]) is datetime or
                    type(newElement[key]) is date
                ):
                    finalValue = newElement[key]
                elif(
                    type(newElement[key]) == dict and
                    type(value) == dict
                ):
                    finalValue = ElementForUpdate(
                        oldElement=value,
                        newElement=newElement[key],
                        nullableAttributes=nullableAttributes,
                        strictColumns=strictColumns,
                    )
                elif(
                    type(newElement[key]) in (list, tuple) and
                    type(value) in (list, tuple)
                ):
                    finalValue = newElement[key]
                else:
                    finalValue = newElement[key]
            elif(
                key in nullableAttributes and
                value is None and
                newElement[key] is None
            ):
                finalValue = newElement[key]
            else:
                finalValue = value
            res[key] = finalValue
        """
        
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None


def ElementFindByParents(element, parents: list):
    try:
        parents = list(
            filter(
                lambda parent: type(parent) == str and len(parent) > 0,
                parents,
            )
        )
        res = deepcopy(element)
        if type(element) == dict :
            haveErr: bool = False
            element2 = deepcopy(element)
            for key, parent in enumerate(parents):
                if parent in element2.keys():
                    element2 = deepcopy(element2[parent])
                else:
                    haveErr = True
                    break
            if haveErr == False:
                res = deepcopy(element2)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None
def ElementForUpdateV2(
    oldElement: any,
    newElement: any,
    nullableAttributes: list = [],
    columns: list = [],
):
    try:
        columns = deepcopy(columns) if type(columns) in (list, tuple) else []
        columns = list(
            filter(
                lambda column: (
                    type(column) == dict and (
                        (
                            'parent' in column.keys() and (
                                (
                                    type(column['parent']) == str and
                                    len(column['parent']) > 0
                                ) or
                                column['parent'] is None
                            )
                        ) or not('parent' in column.keys())
                    ) and
                    'children' in column.keys() and
                    (
                        type(column['children']) in (list, tuple) or
                        column['children'] is None
                    )
                ),
                columns,
            )
        )
        def CleanColumn(data):
            if data['children'] is None:
                data['children'] = []
            if (
                not('parent' in data.keys()) or (
                    'parent' in data.keys() and 
                    data['parent'] is None
                )
            ):
                data['parent'] = None
            return data
        columns = list(
            map(
                lambda column: CleanColumn(column),
                columns,
            )
        )
        nullableAttributes = list(
            filter(
                lambda x: type(x) == str and len(x) > 0,
                nullableAttributes,
            ),
        ) if type(nullableAttributes) in (list, tuple) else []
        oldElement = oldElement if type(oldElement) == dict else {}
        newElement = newElement if type(newElement) == dict else {}

        def structAction(
            columnParentName: str = None,
            oldData = oldElement,
            newData = newElement,
            parents = []
        ):
                oldData = deepcopy(oldData) if type(oldData) == dict else {}
                newData = deepcopy(newData) if type(newData) == dict else {}
                parents = list(
                    filter(
                        lambda parent: type(parent) == str and len(parent) > 0,
                        deepcopy(parents),
                    )
                ) if type(parents) in (list, tuple) else []
                structElement = {}
                columnsTarget = list(
                    filter(
                        lambda column: (
                            (
                                columnParentName is None and
                                column['parent'] is None
                            ) or column['parent'] == columnParentName
                        ),
                        deepcopy(columns),
                    )
                )
                # print('--> ElementForUpdateV2 - structAction | columnsTarget:: ', columnsTarget)
                # print('--> ElementForUpdateV2 - structAction | columns:: ', columns)
                for key, columnT in enumerate(columnsTarget):
                    for keyChild, child in enumerate(columnT['children']):
                        structElement[child] = None
                        newParents = deepcopy(parents) + [deepcopy(child)]

                        if child in oldData.keys():
                            structElement[child] = oldData[child]
                        if child in newData.keys():
                            if newData[child] is not None:
                                structElement[child] = newData[child]
                            elif child in nullableAttributes and newData[child] is None:
                                structElement[child] = None
                        
                        columnsTargetChildren = list(
                            filter(
                                lambda column: (
                                    (
                                        child is None and
                                        column['parent'] is None
                                    ) or column['parent'] == child
                                ),
                                deepcopy(columns),
                            )
                        )
                        # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] newParents:: ', newParents)
                        # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] columnsTargetChildren:: ', columnsTargetChildren)
                        # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] (len(columnsTargetChildren) > 0):: ', (len(columnsTargetChildren) > 0))
                        if len(columnsTargetChildren) > 0:
                            # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] ElementFindByParents(oldData, newParents):: ', ElementFindByParents(oldData, newParents))
                            # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] ElementFindByParents(newData, newParents):: ', ElementFindByParents(newData, newParents))
                            structElementChild = structAction(
                                columnParentName=deepcopy(child),
                                oldData=ElementFindByParents(oldData, newParents),
                                newData=ElementFindByParents(newData, newParents),
                            )
                            structElement[child] = structElementChild
                            # print('--> ElementForUpdateV2 - structAction | [key = ', key,'][keyChild = ', keyChild,'] structElementChild:: ', structElementChild)
                
                        if structElement[child] is None and not(child in nullableAttributes):
                            del structElement[child]
                return deepcopy(structElement)

        # print('--> ElementForUpdateV2 | columns:: ', columns)
        
        # for indexOld, (keyOld, valueOld) in enumerate(oldElement.items()):
        #     pass
        # res = loopObjectV2(data = oldElement, map = loopAction)

        return structAction(
            columnParentName = None,
            oldData = oldElement,
            newData = newElement,
            parents = [],
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None