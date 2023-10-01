from typing import *
from functools import reduce
import re
import math
from logging import Logger
from operator import and_, or_, not_
import logging
import pandas as pd

from .sql import DBCONFIG
from .SQLAUtil import cleanForExtractCompositeType, extractCompositeType
from .config import pagesPossibles
from .hivi_init import Manager


log = logging.getLogger(__name__)
manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']

def __eq_exec(column, data):
    return (column == data)
def __ne_exec(column, data):
    return (column != data)
def __in_exec(column, data):
    return column in data
def __gt_exec(column, data):
    return (column > data)
def __lt_exec(column, data):
    return (column > data)
def __gte_exec(column, data):
    return (column >= data)
def __lte_exec(column, data):
    return (column >= data)
def __between_exec(column, data):
    return (column >= data & column <= data)
def __is_exec(column, data):
    if data is not None:
        return (column.isin(data))
    else:
        return (column == data)
def __not_exec(column, data):
    if data is not None:
        return (~column.isin(data))
    else:
        return (column != data)
def __like_exec(column, data):
    data = str(data)
    val = "".join(data.split("%"))
    # if DEBUG :
        # print("> __like_exec - column:: ", column)
        # print("> __like_exec - data:: ", data)
        # print("> __like_exec - val:: ", val)
        # print("> __like_exec - bool(re.match(r'^\%(\w|\s){1,}\%$', data)):: ", bool(re.match(r'^\%(\w|\s){1,}\%$', data)))
        # print("> __like_exec - bool(re.match(r'^\%(\w|\s){1,}', data)):: ", bool(re.match(r'^\%(\w|\s){1,}', data)))
        # print("> __like_exec - bool(re.match(r'(\w|\s){1,}\%$', data)):: ", bool(re.match(r'(\w|\s){1,}\%$', data)))
    
    if(bool(re.match(r'^\%(\w|\s){1,}\%$', data))):
        return (column.str.contains(val, na=False))
    elif(bool(re.match(r'^\%(\w|\s){1,}', data))):
        # if DEBUG :
            # print("^\%(\w|\s){1,}")
        return (column.str.startswith(val))
    elif(bool(re.match(r'(\w|\s){1,}\%$', data))):
        # if DEBUG :
            # print("(\w|\s){1,}\%$")
        return (column.str.endswith(val))
    else:
        # if DEBUG :
            # print("%(\w\n){1,0}%$")
        return (column.str.contains(val, na=False))
def __notlike_exec(column, data):
    data = str(data)
    val = "".join(data.split("%"))
    if(bool(re.match(r'^\%(\w|\s){1,}\%$', data))):
        return (~column.str.contains(val, na=False))
    elif(bool(re.match(r'^\%(\w|\s){1,}', data))):
        return (~column.str.startswith(val))
    elif(bool(re.match(r'(\w|\s){1,}\%$', data))):
        return (~column.str.endswith(val))
    else:
        return (~column.str.contains(val, na=False))
def __starts_with_exec(column, data):
    return (column.str.startswith(data))
def __ends_with_exec(column, data):
    return (column.str.endswith(data))
def __contains_exec(column, data):
    return (column.str.contains(data))
def __icontains_exec(column, data):
    return (column.str.contains(data, case=True))
def __match_exec(column, data):
    return (column.str.match(data))
def __imatch_exec(column, data):
    return (column.str.match(data, case=True))
allLogicalOperator = {
    '$eq': __eq_exec,
    '$ne': __ne_exec,
    '$in': __in_exec,
    '$gt': __gt_exec,
    '$lt': __lt_exec,
    '$gte': __gte_exec,
    '$lte': __lte_exec,
    '$between': __between_exec,
    '$is': __is_exec,
    '$not': __not_exec,
    # '$isdistinct': __is_distinct_exec,
    # '$notDistinct': __not_distinct_exec,
    '$like': __like_exec,
    '$notLike': __notlike_exec,
    # '$ilike': __ilike_exec,
    # '$notIlike': __notilike_exec,
    '$startsWith': __starts_with_exec,
    '$endsWith': __ends_with_exec,
    '$contains': __contains_exec,
    '$icontains': __icontains_exec,
    '$match': __match_exec,
    '$imatch': __imatch_exec,
}

def __and_exec(data):
    res = data
    if(type(data) in (list, tuple)):
        for index, value in enumerate(data):
            dataElement = data[index]
            if(index == 0):
                res = dataElement
            else:
                res = res & dataElement
    return res
def __or_exec(data):
    res = data
    if(type(data) in (list, tuple)):
        for index, value in enumerate(data):
            dataElement = data[index]
            if(index == 0):
                res = dataElement
            else:
                res = res | dataElement
            dataElement = dataElement
    return res
def __not_exec(data):
    res = data
    if(type(data) in (list, tuple)):
        for index, value in enumerate(data):
            dataElement = data[index]
            if(index == 0):
                res = dataElement
            else:
                res = res & dataElement
    return ~(res)
allComparisonOperator = {
    '_and': __and_exec,
    '_or': __or_exec,
    '_not': __not_exec,
}


allCond = {}
allCond.update(allLogicalOperator)
allCond.update(allComparisonOperator)


def PD_querySessionPagination(
    dataframe: pd.DataFrame,
    progressive = False,
    page: int = 1,
    pageSize: int = 10,
):
    try:
        if(type(page) in (str, int, float)):
            page = int(page)
        if(type(pageSize) in (str, int, float)):
            pageSize = int(pageSize)
        progressive = progressive if type(progressive) == bool else False
        page = page if (
            type(page) == int
        ) else 1
        pageSize = pageSize if (
            pageSize in pagesPossibles
        ) else pagesPossibles[0]
        
        total: int = len(dataframe.index)
        total = total if type(total) == int else 0
        exists: bool = (total > 0)
        
        takeAllDatas: bool = (pageSize == -1)
        pageSize = total if (pageSize == -1) else pageSize
        pageCount = math.ceil(total/pageSize) if type(total) in (float, int) and total > 0 else 0
        page = page if(
            page >= 1 and
            page <= pageCount
        ) else 1

        offset = 0 if (progressive) else ((page * pageSize) - pageSize)
        limit = (page * pageSize) if (progressive) else pageSize

        dataframePaginated = dataframe.iloc[offset:(limit + offset)].reset_index(drop = True)

        # if DEBUG :
            # print("> PD_querySessionPagination - takeAllDatas:: ", takeAllDatas)
            # print("> PD_querySessionPagination - pageSize:: ", pageSize)

        pagination = {
            'page': page,
            'pageSize': pageSize if takeAllDatas is False else -1,
            'pageCount': pageCount,
            'pageLength': len(dataframePaginated.index),
            'total': total,
        }

        return dataframePaginated, pagination
    except Exception as err:
        MSG: str = 'Failure while paging over data'
        log.error(MSG)
        raise Exception("{msg} || {err}".format(
            msg = MSG,
            err = str(err),
        ))

def PD_querySessionSort(
    dataframe: pd.DataFrame,
    options: list,
):
    try:
        optionsPossibles = ('asc', 'desc')
        if(
            not(options == 'random')
        ):
            options = options if type(options) in (list, tuple) else []
            options = list(
                filter(
                    lambda option: (
                        type(option) in (list, tuple) and
                        len(option) > 0 and
                        len(option) <= 2
                    ),
                    options,
                )
            )
            options = list(
                map(
                    lambda option: (
                        [option[0].lower(), 'asc'] if not(len(option) == 2) else [option[0].lower(), option[1].lower()]
                    ),
                    options,
                )
            )
            options = list(
                filter(
                    lambda option: (
                        option[1] in optionsPossibles
                    ),
                    options,
                )
            )
            if(len(options) > 0):
                options = {
                    'columns': list(
                        map(
                            lambda x: x[0],
                            options,
                        )
                    ),
                    'ascending': list(
                        map(
                            lambda x: True if x[1] == 'asc' else False,
                            options,
                        )
                    )
                }
                dataframe = dataframe.sort_values(options['columns'], ascending = options['ascending']).reset_index(drop = True)
        else:
            dataframe = dataframe.sample(frac = 1)

        # if DEBUG :
            # print("> PD_querySessionSort - dataframe:: ", dataframe)

        return dataframe
    except Exception as err:
        MSG: str = 'Failure while sorting on data'
        log.error(MSG)
        raise Exception("{msg} || {err}".format(
            msg = MSG,
            err = str(err),
        ))

def PD_queryFilter(query: dict, Dataframe: pd.DataFrame):
    try:
        return PD_applyComparisonOperators(
            data = query,
            co = allComparisonOperator,
            lo = allLogicalOperator,
            op = allCond,
            Dataframe = Dataframe,
        )
    except Exception as err:
        MSG: str = 'Failure while creating sql filter query'
        log.error(MSG)
        raise Exception("{msg} || {err}".format(
            msg = MSG,
            err = str(err),
        ))
   
def PD_getColumnLO_names(columnStr: str, Dataframe: pd.DataFrame):
    var2 = re.sub(
        re.compile(r'\s', re.IGNORECASE | re.DOTALL),
        '', columnStr
    )
    names = var2.split(".")

    return names
def PD_getColumnLO(columnStr: str, Dataframe: pd.DataFrame):
    names = PD_getColumnLO_names(columnStr, Dataframe=Dataframe)

    res = None
    for index, value in enumerate(names):
        if(index == 0):
            res = Dataframe[value]
        else:
            res = res.map(lambda x: x[value])

    # if DEBUG :
        # print("> PD_getColumnLO - columnStr:: ", columnStr)
        # print("> PD_getColumnLO - config:: ", config)
        # print("> PD_getColumnLO - res:: ", res)

    return res

def PD_applyLogicalOperators(
    data: any,
    cond: any,
    Dataframe: pd.DataFrame = None,
    parent: any = None,
):
    parent = parent if type(parent) == str else None
    data = data if type(data) in (list, tuple, dict) else (
        [] if type(data) in (list, tuple) else {}
    )

    # if DEBUG :
        # print("> PD_applyLogicalOperators - Dataframe:: ", Dataframe)
        # print("> PD_applyLogicalOperators - parent:: ", parent)

    if(type(data) == dict):
        subData = {}
        compositeParentIds = []
        for index, key in enumerate(data):
            element = data[key]
            parentElement = key

            # if DEBUG :
                # print("> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - key:: ", key)
                # print("> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - data:: ", data)
                # print("> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - data[", key, "]:: ", element)
            
            if(type(element) == dict):
                finalValue = {}
                for indexSub, keySub in enumerate(element):
                    elementSub = element[keySub]
                    constraint = (
                        parentElement is not None and
                        keySub in cond.keys()
                    )
                    newkeySub = "{parent}.{child}".format(
                        parent = parentElement,
                        child = keySub,
                    )

                    # if DEBUG :
                        # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - elementSub:: ", elementSub)
                        # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - keySub:: ", keySub)
                        # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - newkeySub:: ", newkeySub)
                        # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - constraint:: ", constraint)
                        # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - cond.keys():: ", cond.keys())

                    if(constraint):
                        names = PD_getColumnLO_names(parentElement, Dataframe = Dataframe)
                        # column = PD_getColumnLO(newkeySub, Dataframe = Dataframe)
                        column = PD_getColumnLO(parentElement, Dataframe = Dataframe)
                        if(len(names) > 1):
                            try:
                                finalValue[newkeySub] = column.map(lambda x: cond[keySub](x, elementSub))
                            except Exception as errr:
                                finalValue[newkeySub] = cond[keySub](
                                    column,
                                    elementSub,
                                )
                        else:
                            finalValue[newkeySub] = cond[keySub](
                                column,
                                elementSub,
                            )
                        compositeParentIds.append(parentElement)
                        # if DEBUG :
                            # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - finalValue:: ", finalValue)
                            # print("\t> PD_applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - data:: ", data)
                        # data[newkeySub] = elementSub
                    element[keySub] = elementSub
                # if DEBUG :
                    # print("> PD_applyLogicalOperators | subData:: ", subData)
                subData.update(finalValue)
            data[key] = element
        
        # if DEBUG :
            # print("> PD_applyLogicalOperators | subData.items():: ", subData.items())
            # print("> PD_applyLogicalOperators | len(subData.keys()):: ", len(subData.keys()))
        if(
            len(subData.keys()) > 0
        ):
            data.update(subData)
            # if DEBUG :
                # print("> PD_applyLogicalOperators | subData:: ", subData)
                # print("> PD_applyLogicalOperators | compositeParentIds:: ", compositeParentIds)

            for index, key in enumerate(compositeParentIds):
                if(key in data.keys()):
                    del data[key]
        finaldata = [] if type(data) in (list, tuple) else {}
        for index, keyOrValue in enumerate(data):
            key = index if type(data) in (list, tuple) else keyOrValue
            element = data[key]
            element = PD_applyLogicalOperators(element, cond = cond, parent = key, Dataframe = Dataframe)
            if(
                type(element) in (str, int, float) or (
                    type(element) in (list, tuple, dict) and
                    len(element.keys()) > 0
                )
            ):
                finaldata[key] = element
        # if DEBUG :
            # print("> PD_applyLogicalOperators | finaldata(old):: ", finaldata)

        finaldata = list(finaldata) if type(data) in (list, tuple) else dict(finaldata.values())
        # if DEBUG :
            # print("> PD_applyLogicalOperators | finaldata:: ", finaldata)
        """if(len(finaldata) > 0):
            data = finaldata"""
    else:
        data = None

    if(parent == None):
        if(type(data) in (list, tuple, dict)):
            data = list(data.values())

    return data
def PD_applyComparisonOperators(
    data: any,
    co: any,
    lo: any,
    op: any,
    Dataframe: pd.DataFrame = None,
    parent: any = None,
):
    parent = parent if type(parent) in [str, int, float] else None

    # if DEBUG :
        # print("> PD_applyComparisonOperators - data:: ", data)
        # print("> PD_applyComparisonOperators - co.keys():: ", co.keys())
        # print("> PD_applyComparisonOperators - lo.keys():: ", lo.keys())
    if(type(data) in (list, tuple, dict)):
        finalData = [] if type(data) in (list, tuple) else {}
        otherData = [] if type(data) in (list, tuple) else {}
        primaryData = [] if type(data) in (list, tuple) else {}
        for index, keyOrValue in enumerate(data):
            key = index if type(data) in (list, tuple) else keyOrValue
            element = data[key]
            cond = not(key in co.keys())

            if(cond):
                if(type(data) in (list, tuple)):
                    otherData.append(element)
                elif(type(data) == dict):
                    otherData[key] = element
            else:
                if(type(data) in (list, tuple)):
                    primaryData.append(element)
                elif(type(data) == dict):
                    primaryData[key] = element
            # if DEBUG :
                # print("\t> PD_applyComparisonOperators | index:: ", index, " - key:: ", key)
                # print("\t> PD_applyComparisonOperators | index:: ", index, " - cond:: ", cond)

        # - primaryData
        for index, keyOrValue in enumerate(primaryData):
            key = index if type(primaryData) in (list, tuple) else keyOrValue
            element = primaryData[key]

            # if DEBUG :
                # print("\t\t\t---> PD_applyComparisonOperators | index:: ", index, " - key:: ", key)
            if(
                type(element) in (list, tuple)
            ):
                # if DEBUG :
                    # print("\t\t\t---> PD_applyComparisonOperators | index:: ", index, " - element(old):: ", element)
                for indexSub, valueSub in enumerate(element):
                    keySub = indexSub
                    elementSub = element[keySub]

                    # if DEBUG :
                        # print("\t\t\t\t\t---> PD_applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - keySub:: ", keySub)
                        # print("\t\t\t\t\t---> PD_applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - element[", keySub, "] [BEFORE]:: ", element[keySub])
                    if(
                        type(elementSub) == dict and
                        len(
                            list(
                                filter(
                                    lambda x: (x in co.keys()),
                                    elementSub.keys()
                                )
                            )
                        ) <= 0
                    ):
                        elementSub = cleanForExtractCompositeType(
                            elementSub,
                            cond = op,
                        )
                        elementSub = extractCompositeType(
                            elementSub,
                            cond = op,
                        )
                        elementSub = PD_applyLogicalOperators(
                            data = elementSub,
                            cond = lo,
                            Dataframe = Dataframe,
                        )
                        elementSub = co['_and'](elementSub)
                    else:
                        elementSub = PD_applyComparisonOperators(elementSub, co = co, lo = lo, op = op, Dataframe = Dataframe, parent = keySub)
                    element[keySub] = elementSub
                    # if DEBUG :
                        # print("\t\t\t\t\t---> PD_applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - element[", keySub, "]:: ", element[keySub])
                # if DEBUG :
                    # print("\t\t\t---> PD_applyComparisonOperators | index:: ", index, " - element:: ", element)

            # --

            # element = PD_applyComparisonOperators(element, co = co, lo = lo, op = op, Dataframe = Dataframe, parent = parent)
            # if DEBUG :
                # print("\t\t\t---> PD_applyComparisonOperators | index:: ", index, " - element  [BEFORE]:: ", element)
            primaryData[key] = co[key](element)
        # - otherData
        otherData = cleanForExtractCompositeType(
            data = otherData,
            cond = op,
        )
        otherData = extractCompositeType(
            data = otherData,
            cond = op,
        )
        otherData = PD_applyLogicalOperators(
            data = otherData,
            cond = lo,
            Dataframe = Dataframe,
        )
        # - primaryData
        primaryData = list(primaryData.values())

        # if DEBUG :
            # print("> PD_applyComparisonOperators - otherData:: ", otherData)
            # print("> PD_applyComparisonOperators - primaryData:: ", primaryData)
            
        """if(type(data) in (list, tuple)):
            finalData = otherData + primaryData
        elif(type(data) == dict):
            finalData.update(otherData)
            finalData.update(primaryData)"""
        if(
            (
                type(primaryData) in (list, tuple) and
                len(primaryData) > 0
            ) and (
                type(otherData) in (list, tuple) and
                len(otherData) > 0
            )
        ):
            # if DEBUG :
                # print("> PD_applyComparisonOperators - co['_and'](otherData):: ", co['_and'](otherData))
                # print("> PD_applyComparisonOperators - co['_and'](primaryData):: ", co['_and'](primaryData))
                # print("> PD_applyComparisonOperators - data [BEFORE]:: ", data)
            data = co['_and']([
                co['_and'](otherData),
                co['_and'](primaryData),
            ])
        elif(
            type(primaryData) in (list, tuple) and
            len(primaryData) > 0
        ):
            data = co['_and'](primaryData)
        elif(
            type(otherData) in (list, tuple) and
            len(otherData) > 0
        ):
            data = co['_and'](otherData)
    # if DEBUG :
        # print("> PD_applyComparisonOperators - data:: ", data)
                
    return data