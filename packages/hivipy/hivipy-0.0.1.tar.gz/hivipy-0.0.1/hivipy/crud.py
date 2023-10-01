from typing import *
import asyncio
import logging
import traceback
import sys
import copy
import re
import pandas as pd
from flask.wrappers import Response
from sqlalchemy.orm.query import Query
from copy import deepcopy
from .utils import getIdBody

from .objects import loopObject, removeAttributesOfObject, strIsJsonType, strToJsonType
from .db import NoSql_SQL_MemoryDBAction
from .utils import ElementForUpdate, CRUDCleanFinalDatas
from .sqlcrud import _SQL_findAll, _SQL_countAll, _SQL_findOne, _SQL_exists, _SQL_add, _SQL_update, _SQL_edit, _SQL_deleteAll, _SQL_delete, _SQL_archiveOrRestore, _SQL_blockOrUnblock, _SQL_publishOrUnpublish, _SQL_add_multiple, _SQL_update_multiple, _SQL_edit_multiple, _SQL_delete_multiple, _SQL_archiveOrRestore_multiple, _SQL_archive_multiple, _SQL_restore_multiple, _SQL_blockOrUnblock_multiple, _SQL_block_multiple, _SQL_unblock_multiple, _SQL_publishOrUnpublish_multiple, _SQL_publish_multiple, _SQL_unpublish_multiple, _SQL_export, _SQL_extract
from .interfaces import CRUDFindAllDict, CRUDOptionDict, CRUDCountAllDict, CRUDFindDict, CRUDExistsDict, CRUDExecSingleDict, CRUDExecAllDict, CRUDExtractDatasDict


def loopObjectAction(index, key, element, data):
    if type(element) == str and strIsJsonType(element):
        element = strToJsonType(element)
    # element = CRUDCleanFinalDatas(
    #     data = element,
    #     singleid = False,
    # )
    return element

def _findAll(
    query: dict,
    _kit: dict = {
        'readModel': None,
    },
    progressive: bool = False,
    _clean: dict = {
        'cleanData': lambda x: x,
    },
    returnException: bool = True,
) -> CRUDFindAllDict:
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    progressive = deepcopy(progressive)
    _clean = deepcopy(_clean)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_findAll(
            query=query,
            _kit=_kit,
            progressive=progressive,
            _clean=_clean,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'datas' in result.keys():
        result['datas'] = loopObject(data = result['datas'], map = loopObjectAction)

    return result
def _countAll(
    query: dict,
    _kit: dict = {
        'readModel': None,
    },
    progressive: bool = False,
    _clean: dict = {
        'cleanData': lambda x: x,
    },
    returnException: bool = True,
) -> CRUDCountAllDict:
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    progressive = deepcopy(progressive)
    _clean = deepcopy(_clean)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_countAll(
            query=query,
            _kit=_kit,
            progressive=progressive,
            _clean=_clean,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'datas' in result.keys():
        result['datas'] = loopObject(data = result['datas'], map = loopObjectAction)

    return result
def _findOne(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
    _clean: dict = {
        'cleanData': lambda x: x,
    },
    attributes: 'list|tuple' = [],
    returnException: bool = True,
) -> CRUDFindDict:
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    # _clean = deepcopy(_clean)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_findOne(
            query=query,
            _kit=_kit,
            _clean=_clean,
            attributes=attributes,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _exists(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
    returnException: bool = True,
) -> CRUDExistsDict:
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    
    return NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_exists(
            query=query,
            _kit=_kit,
            returnException = returnException,
        )),
        returnException = returnException,
    )

def _add(
    query: dict,
    body: dict,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'cleanData': lambda data, exists, lang: data,
        'cleanBody': lambda x: x,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_add(
            query=query,
            body=body,
            lang=lang,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _update(
    query: dict,
    body: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'cleanBody': lambda x: x,
        'cleanData': lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(
            oldElement=oldData,
            newElement=newData,
            nullableAttributes=nullableAttributes,
        ),
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_update(
            query=query,
            body=body,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _edit(
    query: dict,
    body: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'formAdd': None,
        'formUpdate': None,
    },
    _clean: dict = {
        'cleanBody': lambda x: x,
        'cleanDataAdd': lambda data, exists, lang: data,
        'cleanDataUpdate': lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(
            oldElement=oldData,
            newElement=newData,
            nullableAttributes=nullableAttributes,
        ),
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_edit(
            query=query,
            body=body,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result

def _deleteAll(
    lang: str,
    _kit: dict = {
        'writeModel': None,
    },
    _supAction = lambda data, lang, res : res,
    returnException: bool = True,
) -> CRUDExecSingleDict:
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_deleteAll(
            lang=lang,
            _kit=_kit,
            _supAction=_supAction,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result

def _delete(
    query: dict,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
    },
    _supAction = lambda data, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_delete(
            query=query,
            lang=lang,
            _kit=_kit,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _archiveOrRestore(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    _actionStrict = None,
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_archiveOrRestore(
            query=query,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            _actionStrict=_actionStrict,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _archive(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _restore(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _blockOrUnblock(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    _actionStrict = None,
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_blockOrUnblock(
            query=query,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            _actionStrict=_actionStrict,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _block(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _unblock(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _publishOrUnpublish(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    _actionStrict = None,
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_publishOrUnpublish(
            query=query,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            _actionStrict=_actionStrict,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _publish(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _unpublish(
    query: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _supAction = lambda data, body, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecSingleDict:
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = _publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result

def _add_multiple(
    # query: dict,
    bodies: list,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'cleanBody': lambda x: x,
        'cleanData': lambda data, exists, lang: data,
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    returnException: bool = True,
) -> CRUDExecAllDict:
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_add_multiple(
            bodies=bodies,
            lang=lang,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _update_multiple(
    # query: dict,
    bodies: list,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'cleanBody': lambda x: x,
        'cleanData': lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(
            oldElement=oldData,
            newElement=newData,
            nullableAttributes=nullableAttributes,
        ),
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_update_multiple(
            bodies=bodies,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _edit_multiple(
    bodies: list,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'formAdd': None,
        'formUpdate': None,
    },
    _clean: dict = {
        'cleanBody': lambda x: x,
        'cleanDataAdd': lambda data, exists, lang: data,
        'cleanDataUpdate': lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(
            oldElement=oldData,
            newElement=newData,
            nullableAttributes=nullableAttributes,
        ),
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_edit_multiple(
            bodies=bodies,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result

def _delete_multiple(
    params: dict,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda data, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_delete_multiple(
            params=params,
            lang=lang,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _archiveOrRestore_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
    _actionStrict = None,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_archiveOrRestore_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
            _actionStrict=_actionStrict,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _archive_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_archive_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _restore_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_restore_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _blockOrUnblock_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
    _actionStrict = None,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_blockOrUnblock_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
            _actionStrict=_actionStrict,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _block_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_block_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _unblock_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_unblock_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _publishOrUnpublish_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
    _actionStrict = None,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_publishOrUnpublish_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
            _actionStrict=_actionStrict,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _publish_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_publish_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result
def _unpublish_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: getIdBody(body),
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
    returnException: bool = True,
) -> CRUDExecAllDict:
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_unpublish_multiple(
            params=params,
            lang=lang,
            nullableAttributes=nullableAttributes,
            _kit=_kit,
            _clean=_clean,
            _supAction=_supAction,
            _mapActionPK=_mapActionPK,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'data' in result.keys():
        result['data'] = loopObject(data = result['data'], map = loopObjectAction)

    return result

def _export(
    query: dict,
    _kit: dict = {
        'readModel': None,
    },
    progressive: bool = False,
    _clean: dict = {
        'cleanData': lambda x: x,
    },
    export_type = 'csv',
    title = None,
    filename = None,
    columns = [],
    lang = None,
    returnException: bool = True,
) -> 'CRUDExecSingleDict | Response':
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    progressive = deepcopy(progressive)
    _clean = deepcopy(_clean)
    export_type = deepcopy(export_type)
    title = deepcopy(title)
    filename = deepcopy(filename)
    columns = deepcopy(columns)
    lang = deepcopy(lang)

    return NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_export(
            query=query,
            _kit=_kit,
            progressive=progressive,
            _clean=_clean,
            export_type=export_type,
            title=title,
            filename=filename,
            columns=columns,
            lang=lang,
            returnException = returnException,
        )),
        returnException = returnException,
    )

def _extract(
    file,
    rows = {},
    columns = {},
    cleanData = (lambda x: x),
    schemas = {},
    returnException: bool = True,
) -> CRUDExtractDatasDict:
    # file = deepcopy(file)
    rows = deepcopy(rows)
    columns = deepcopy(columns)
    cleanData = deepcopy(cleanData)
    schemas = deepcopy(schemas)

    result = NoSql_SQL_MemoryDBAction(
        sqlAction=(lambda dialect, dbType : _SQL_extract(
            file=file,
            rows=rows,
            columns=columns,
            cleanData=cleanData,
            schemas=schemas,
            returnException = returnException,
        )),
        returnException = returnException,
    )
    if type(result) == dict and 'datas' in result.keys():
        result['datas'] = loopObject(data = result['datas'], map = loopObjectAction)

    return result