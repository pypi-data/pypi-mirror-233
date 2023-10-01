from typing import *
import asyncio
import logging
import traceback
import sys
from copy import deepcopy
import pandas as pd

from .objects import loopObject, pdDataframeToObject, removeAttributesOfObject

from .PDUtil import PD_queryFilter, PD_querySessionPagination, PD_querySessionSort
from .SQLAUtil import queryFilter, querySessionPagination, querySessionSort
from .file import Export, Import
from .sql import session
from .config import pagesPossibles, responsesPossibles
from .utils import ElementForUpdate, getLang
from .hivi_init import Manager


manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)

def __PKQuery(query: dict, model, mapFunct = lambda data: {
    'id': {
        '$eq': data['id'],
    },
}):
    query = deepcopy(query)
    model = deepcopy(model)
    mapFunct = deepcopy(mapFunct)

    try:
        mapFunct = mapFunct if callable(mapFunct) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        query = query if type(query) == dict else {}
        query.update({
            '_pageSize': -1,
        })
        allDatas = _PD_findAll(query, _kit = {
            'readModel': model,
        })['datas']
        res = {
            '_or': list(
                map(
                    mapFunct,
                    allDatas,
                ),
            )
        }
        # if DEBUG :
            # print("> main.scripts.__PKQuery | res:: ", res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None

def _PD_findAll(
    query: dict,
    _kit: dict = {
        'readModel': None,
    },
    progressive: bool = False,
    _clean: dict = {
        'cleanData': lambda x: x,
    },
):
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    progressive = deepcopy(progressive)
    _clean = deepcopy(_clean)

    try:
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe: pd.DataFrame = readModel
        _clean = _clean if type(_clean) == dict else {
            'cleanData': lambda x: x,
        }
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda x: x)
        progressive = progressive if type(progressive) == bool else False
        query = query if type(query) == dict else {}
        # parameters
        # -> sort
        sort = query['_sort'] if '_sort' in query.keys() else None
        if '_sort' in query.keys():
            del query['_sort']
        # -> pagination
        page = query['_page'] if '_page' in query.keys() else None
        if '_page' in query.keys():
            del query['_page']
        pageSize = query['_pageSize'] if (
            '_pageSize' in query.keys()
        ) else None
        if '_pageSize' in query.keys():
            del query['_pageSize']
        # -> attributes
        attributes = query['_attributes'] if (
            '_attributes' in query.keys() and
            type(query['_attributes']) in (list, tuple)
        )  else []
        attributes = list(
            filter(
                lambda x: type(x) == str,
                attributes,
            )
        )
        if '_attributes' in query.keys():
            del query['_attributes']

        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - sort:: ", sort)
            # print("> Scripts - crud | PD_findAll - attributes:: ", attributes)

        # filter
        QF = None
        if(len(query.keys()) > 0):
            queryF = deepcopy(query)
            QF = PD_queryFilter(
                queryF,
                Dataframe = Dataframe,
            )
        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - QF:: ", QF)
        if(QF is not None and len(QF) > 0):
            Dataframe = Dataframe[QF]
        Dataframe = PD_querySessionSort(Dataframe, sort)
        # pagination
        dataframePaginated, pagination = PD_querySessionPagination(Dataframe, page = page, pageSize = pageSize, progressive = progressive)

        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - dataframePaginated:: ", dataframePaginated)
        result = pdDataframeToObject(dataframePaginated, isArray=True)
        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - result:: ", result)

        result = result if type(result) in (list, tuple) else []
        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - cleanData:: ", cleanData)


        # map
        result = list(
            map(
                lambda data: cleanData(data),
                result,
            )
        )
        
        # if DEBUG :
            # print("> Scripts - crud | PD_findAll - result:: ", result)

        return {
            'datas': result,
            'meta': {
                'pagination': pagination,
            },
        }
    except Exception as err:
        log.error(str(err))
        return {
            'datas': [],
            'meta': {
                'pagination': {
                    'page': 1,
                    'pageSize': pagesPossibles[0],
                    'pageCount': 1,
                    'pageLength': 0,
                    'total': 0,
                },
            },
        }
def _PD_findOne(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
    _clean: dict = {
        'cleanData': lambda x: x,
    },
):
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    
    try:
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe: pd.DataFrame = readModel
        _clean = _clean if type(_clean) == dict else {
            'cleanData': lambda x: x,
        }
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda x: x)
        query = query if type(query) == dict else {}
        # parameters
        # -> sort
        if '_sort' in query.keys():
            del query['_sort']
        # -> pagination
        if '_page' in query.keys():
            del query['_page']
        if '_pageSize' in query.keys():
            del query['_pageSize']
        # -> attributes
        if '_attributes' in query.keys():
            del query['_attributes']

        # filter
        QF = None
        if(len(query.keys()) > 0):
            queryF = deepcopy(query)
            QF = PD_queryFilter(
                queryF,
                Dataframe = Dataframe,
            )
        # if DEBUG :
            # print("> Scripts - crud | PD_findOne - QF:: ", QF)
        if(QF is not None and len(QF) > 0):
            Dataframe = Dataframe[QF]

        result = pdDataframeToObject(Dataframe, isArray=False)

        row = cleanData(result)
        exists = True if result else False

        return {
            'data': row,
            'exists': exists,
        }
    except Exception as err:
        log.error(str(err))
        return {
            'data': None,
            'exists': False,
        }
def _PD_exists(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
):
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    
    try:
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe: pd.DataFrame = readModel
        query = query if type(query) == dict else {}
        # parameters
        # -> sort
        if '_sort' in query.keys():
            del query['_sort']
        # -> pagination
        if '_page' in query.keys():
            del query['_page']
        if '_pageSize' in query.keys():
            del query['_pageSize']
        # -> attributes
        if '_attributes' in query.keys():
            del query['_attributes']

        # filter
        QF = None
        if(len(query.keys()) > 0):
            queryF = deepcopy(query)
            QF = PD_queryFilter(
                queryF,
                Dataframe = Dataframe,
            )
        # if DEBUG :
            # print("> Scripts - crud | PD_findOne - QF:: ", QF)
        if(QF is not None and len(QF) > 0):
            Dataframe = Dataframe[QF]

        result = pdDataframeToObject(Dataframe, isArray=False)
        
        exists = True if result else False

        return {
            'exists': exists,
        }
    except Exception as err:
        log.error(str(err))
        return {
            'exists': False,
        }

def _PD_add(
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
):
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    
    try:
        query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            del query['lang']
        body = body if type(body) == dict else {}
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda data, exists, lang: data)
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)
        queryExists = query

        body = cleanBody(body)
        body = removeAttributesOfObject(body)
        validatedata = form.validate(body)
        # if DEBUG :
            # print("> main.scripts._add | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            exists = _PD_exists(
                query = queryExists,
                _kit = { 'readModel': Dataframe },
            )['exists']
            # if DEBUG :
                # print("> main.scripts._add | exists:: ", exists)
            if(exists == True):
                return {
                    'type': responsesPossibles['data_exists']['type'],
                    'code': responsesPossibles['data_exists']['code'],
                    'message': responsesPossibles['data_exists']['message'][lang],
                }
            else:
                cleanedData = cleanData(data = validatedata['data'], exists=exists, lang=lang)
                # if DEBUG :
                    # print("> main.scripts._add | cleanedData:: ", cleanedData)
                session.add(writeModel(**cleanedData))
                session.commit()

                res = {
                    'data': cleanedData,
                    'type': 'success',
                }

                res = _supAction(data = cleanedData, body = body, exists = exists, lang = lang, res = res)
        else:
            return {
                'type': responsesPossibles['invalid_form']['type'],
                'code': responsesPossibles['invalid_form']['code'],
                'message': str(validatedata['error']),
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_update(
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
):
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            lang = query['lang']
            del query['lang']
        body = body if type(body) == dict else {}
        lang = getLang(lang)
        queryExists = query
        queryReadWrite = query
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(oldData, newData, nullableAttributes))
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)

        body = cleanBody(body)
        body = removeAttributesOfObject(body)
        validatedata = form.validate(body)
        # if DEBUG :
            # print("> main.scripts._add | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            exists = _PD_exists(
                query = queryExists,
                _kit = { 'readModel': Dataframe },
            )['exists']
            # if DEBUG :
                # print("> main.scripts._add | exists:: ", exists)
            if(exists == True):
                oldElement = _PD_findOne(
                    query = queryReadWrite,
                    _kit = { 'readModel': Dataframe },
                )['data']
                cleanedData = cleanData(
                    oldData=oldElement,
                    newData=validatedata['data'],
                    nullableAttributes=nullableAttributes,
                    exists=exists,
                    lang=lang,
                )
                # if DEBUG :
                    # print("> main.scripts._update | oldElement:: ", oldElement)
                    # print("> main.scripts._update | validatedata['data']:: ", validatedata['data'])
                    # print("> main.scripts._update | cleanedData:: ", cleanedData)
                
                cleanedQueryForTable = __PKQuery(
                    query,
                    model = Dataframe,
                    mapFunct = _mapActionPK
                )
                # if DEBUG :
                    # print("> main.scripts._update | cleanedQueryForTable:: ", cleanedQueryForTable)
                    # print("> main.scripts._update | writeModel:: ", writeModel)
                SQLAQF = queryFilter(
                    cleanedQueryForTable,
                    Table = writeModel,
                )
                session.query(writeModel).filter(SQLAQF).update(cleanedData)
                session.commit()

                res = {
                    'data': cleanedData,
                    'type': 'success',
                }

                res = _supAction(data = cleanedData, body = body, exists = exists, lang = lang, res = res)
            else:
                return {
                    'type': responsesPossibles['data_doesnt_exists']['type'],
                    'code': responsesPossibles['data_doesnt_exists']['code'],
                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                }
        else:
            return {
                'type': responsesPossibles['invalid_form']['type'],
                'code': responsesPossibles['invalid_form']['code'],
                'message': str(validatedata['error']),
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_edit(
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
):
    query = deepcopy(query)
    # body = deepcopy(body)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            lang = query['lang']
            del query['lang']
        body = body if type(body) == dict else {}
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        formAdd = _kit['formAdd'] if (
            'formAdd' in _kit
        ) else None
        formUpdate = _kit['formUpdate'] if (
            'formUpdate' in _kit
        ) else None
        cleanDataAdd = _clean['cleanDataAdd'] if (
            'cleanDataAdd' in _clean and
            callable(_clean['cleanDataAdd'])
        ) else (lambda data, exists, lang: data)
        cleanDataUpdate = _clean['cleanDataUpdate'] if (
            'cleanDataUpdate' in _clean and
            callable(_clean['cleanDataUpdate'])
        ) else (lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(oldData, newData, nullableAttributes))
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)
        queryExists = query
        queryReadWrite = query
        queryReadWrite2 = query

        exists = _PD_exists(
            query = queryExists,
            _kit = { 'readModel': Dataframe },
        )['exists']
        
        # if DEBUG :
            # print("> main.scripts._PD_edit | body:: ", body)
            # print("> main.scripts._PD_edit | query:: ", query)
            # print("> main.scripts._PD_edit | exists:: ", exists)

        body = cleanBody(body)
        body = removeAttributesOfObject(body)
        validatedata = None
        if(exists == True):
            # if DEBUG :
                # print("> main.scripts._PD_edit - UPDATE <")
            exist = True
            validatedata = formUpdate.validate(body)
            # if DEBUG :
                # print("> main.scripts._PD_edit | formUpdate:: ", formUpdate)
        else:
            # if DEBUG :
                # print("> main.scripts._PD_edit - ADD <")
            validatedata = formAdd.validate(body)
            # if DEBUG :
                # print("> main.scripts._PD_edit | formAdd:: ", formAdd)
        
                # print("> main.scripts._PD_edit | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            cleanedData = None
            if(exists == True):
                SQLAQF = queryFilter(
                    __PKQuery(
                        queryReadWrite,
                        model = Dataframe,
                        mapFunct = _mapActionPK
                    ),
                    Table = writeModel,
                )
                oldElement = _PD_findOne(
                    query = queryReadWrite2,
                    _kit = { 'readModel': Dataframe },
                )['data']
                cleanedData = cleanDataUpdate(
                    oldData=oldElement,
                    newData=validatedata['data'],
                    nullableAttributes=nullableAttributes,
                    exists=exists,
                    lang=lang,
                )
                session.query(writeModel).filter(SQLAQF).update(cleanedData)
            else:
                cleanedData = cleanDataAdd(data = validatedata['data'], exists=exists, lang=lang)
                session.add(writeModel(**cleanedData))
            session.commit()
            # if DEBUG :
                # print("> main.scripts._PD_edit | cleanedData:: ", cleanedData)

            res = {
                'data': cleanedData,
                'type': 'success',
            }
            res = _supAction(data = cleanedData, body = body, exists = exists, lang = lang, res = res)

            return res
        else:
            return {
                'type': responsesPossibles['invalid_form']['type'],
                'code': responsesPossibles['invalid_form']['code'],
                'message': str(validatedata['error']),
            }
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }

def _PD_delete(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            del query['lang']
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None

        queryExists = query
        queryReadWrite = query
        exists = _PD_exists(
            query = queryExists,
            _kit = { 'readModel': Dataframe },
        )['exists']
        if(exists == True):
            cleanedData = _PD_findOne(
                query = queryReadWrite,
                _kit = {
                    'readModel': Dataframe,
                },
            )['data']
            
            SQLAQF = queryFilter(
                __PKQuery(
                    query,
                    model = Dataframe,
                    mapFunct = _mapActionPK
                ),
                Table = writeModel,
            )
            session.query(writeModel).filter(SQLAQF).delete()
            session.commit()

            res = {
                'data': cleanedData,
                'type': 'success',
            }

            res = _supAction(data = cleanedData, exists = exists, lang = lang, res = res)
        else:
            return {
                'type': responsesPossibles['data_doesnt_exists']['type'],
                'code': responsesPossibles['data_doesnt_exists']['code'],
                'message': responsesPossibles['data_doesnt_exists']['message'][lang],
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_archiveOrRestore(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    try:
        _actionStrict = _actionStrict if _actionStrict in ('primary', 'reverse') else None
        query = query if type(query) == dict else {}
        body = {
            'status': 'archived',
        }
        # if DEBUG :
            # print("> _PD_archiveOrRestore - body:: ", body)
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['status'] = 'visible' if (oldData['status'] == 'archived') else 'archived'
            if _actionStrict == 'primary':
                newData['status'] = 'archived'
            elif _actionStrict == 'reverse':
                newData['status'] = 'visible'
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        queryReadWrite = query
        return _PD_update(
            query = queryReadWrite,
            body = body,
            lang = lang,
            nullableAttributes = nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': lambda x: x,
                'cleanData': cleanDataFunct,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_archive(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _PD_restore(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )
def _PD_blockOrUnblock(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    try:
        _actionStrict = _actionStrict if _actionStrict in ('primary', 'reverse') else None
        query = query if type(query) == dict else {}
        body = {
            'blocked': True,
        }
        queryReadWrite = query
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['blocked'] = False if (oldData['blocked'] == True) else True
            if _actionStrict == 'primary':
                newData['blocked'] = True
            elif _actionStrict == 'reverse':
                newData['blocked'] = False
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        return _PD_update(
            query = queryReadWrite,
            body = body,
            lang = lang,
            nullableAttributes = nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': lambda x: x,
                'cleanData': cleanDataFunct,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_block(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _PD_unblock(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )
def _PD_publishOrUnpublish(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    _actionStrict = deepcopy(_actionStrict)

    try:
        _actionStrict = _actionStrict if _actionStrict in ('primary', 'reverse') else None
        query = query if type(query) == dict else {}
        body = {
            'published': True,
        }
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['published'] = False if (oldData['published'] == True) else True
            if _actionStrict == 'primary':
                newData['published'] = True
            elif _actionStrict == 'reverse':
                newData['published'] = False
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        queryReadWrite = query
        return _PD_update(
            query = queryReadWrite,
            body = body,
            lang = lang,
            nullableAttributes = nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': lambda x: x,
                'cleanData': cleanDataFunct,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_publish(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _PD_unpublish(
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
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _PD_publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )

def _PD_add_multiple(
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
        'cleanData': lambda data, exist, lang: data,
        'initQueryBody': lambda body: {
            'id': {
                '$eq': body['id'] if type(body) == dict and 'id' in body.keys() else None
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
):
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)

    try:
        """query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            del query['lang']"""
        bodies = list(
            filter(
                lambda body: type(body) == dict,
                bodies,
            )
        ) if type(bodies) in (list, tuple) else []
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda data, exists, lang: data)
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        
        query = {
            '_or': list(
                map(
                    initQueryBody,
                    bodies,
                ),
            ),
        }

        bodies = list(
            map(
                lambda body: cleanBody(body),
                bodies,
            ),
        )
        bodies = removeAttributesOfObject(bodies)
        queryReadWrite = query
        validatedata = form.validate(bodies)
        if(validatedata['valid'] == True):
            exist = _PD_exists(
                query = queryReadWrite,
                _kit = { 'readModel': Dataframe },
            )['exists']
            if(exist == True):
                return {
                    'type': responsesPossibles['data_exists']['type'],
                    'code': responsesPossibles['data_exists']['code'],
                    'message': responsesPossibles['data_exists']['message'][lang],
                }
            else:
                cleanedDatas = list(
                    map(
                        lambda data: cleanData(data = data, exist=exist, lang=lang),
                        validatedata['data'],
                    )
                )

                # if DEBUG :
                    # print("> main.scripts._add_multiple | cleanedDatas:: ", cleanedDatas)
                session.add_all(
                    list(
                        map(
                            lambda data: writeModel(**data),
                            cleanedDatas,
                        )
                    )
                )
                session.commit()

                res = {
                    'data': cleanedDatas,
                    'type': 'success',
                }

                res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
        else:
            return {
                'type': responsesPossibles['invalid_form']['type'],
                'code': responsesPossibles['invalid_form']['code'],
                'message': str(validatedata['error']),
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        session.rollback()

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_update_multiple(
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
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        """query = query if type(query) == dict else {}
        if 'lang' in query.keys():
            del query['lang']"""
        bodies = list(
            filter(
                lambda body: type(body) == dict,
                bodies,
            )
        ) if type(bodies) in (list, tuple) else []
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (
            lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        )
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        _supAction = _supAction if callable(_supAction) else (lambda datas, bodies, exist, lang, res : res)
        
        query = {
            '_or': list(
                map(
                    initQueryBody,
                    bodies,
                ),
            ),
        }

        bodies = list(
            map(
                lambda body: cleanBody(body),
                bodies,
            ),
        )
        bodies = removeAttributesOfObject(bodies)
        validatedata = form.validate(bodies)
        # if DEBUG :
            # print("> main.scripts._update_multiple | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            invalidBodies = list(
                filter(
                    lambda body: not(
                        _PD_exists(
                            query = initQueryBody(body),
                            _kit = { 'readModel': Dataframe },
                        )['exists'] == True
                    ),
                    bodies,
                )
            )
            exist = (len(invalidBodies) <= 0)
            # if DEBUG :
                # print("> main.scripts._update_multiple | invalidBodies:: ", invalidBodies)
                # print("> main.scripts._update_multiple | exist:: ", exist)
            if(exist == True):
                cleanedDatas = []
                session.begin()
                for index, body in enumerate(bodies):
                    query = initQueryBody(body)
                    queryExists = query
                    queryReadWrite = query
                    oldElement = _PD_findOne(
                        query = queryExists,
                        _kit = { 'readModel': Dataframe },
                    )['data']
                    cleanedData = cleanData(
                        oldData=oldElement,
                        newData=validatedata['data'][index],
                        nullableAttributes=nullableAttributes,
                        exists=exist,
                        lang=lang,
                    )
                    SQLAQF = queryFilter(
                        __PKQuery(
                            queryReadWrite,
                            model = Dataframe,
                            mapFunct = _mapActionPK
                        ),
                        Table = writeModel,
                    )
                    session.query(writeModel).filter(SQLAQF).update(cleanedData)
                    cleanedDatas.append(cleanedData)

                # if DEBUG :
                    # print("> main.scripts._update_multiple | cleanedDatas:: ", cleanedDatas)

                session.commit()

                res = {
                    'data': cleanedDatas,
                    'type': 'success',
                }

                res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
            else:
                return {
                    'type': responsesPossibles['data_doesnt_exists']['type'],
                    'code': responsesPossibles['data_doesnt_exists']['code'],
                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                }
        else:
            return {
                'type': responsesPossibles['invalid_form']['type'],
                'code': responsesPossibles['invalid_form']['code'],
                'message': str(validatedata['error']),
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        session.rollback()

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_edit_multiple(
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
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        bodies = list(
            filter(
                lambda body: type(body) == dict,
                bodies,
            )
        ) if type(bodies) in (list, tuple) else []
        lang = getLang(lang)
        
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        formAdd = _kit['formAdd'] if (
            'formAdd' in _kit
        ) else None
        formUpdate = _kit['formUpdate'] if (
            'formUpdate' in _kit
        ) else None
        cleanDataAdd = _clean['cleanDataAdd'] if (
            'cleanDataAdd' in _clean and
            callable(_clean['cleanDataAdd'])
        ) else (lambda data, exists, lang: data)
        cleanDataUpdate = _clean['cleanDataUpdate'] if (
            'cleanDataUpdate' in _clean and
            callable(_clean['cleanDataUpdate'])
        ) else (lambda oldData, newData, nullableAttributes, exists, lang: ElementForUpdate(oldData, newData, nullableAttributes))
        cleanBody = _clean['cleanBody'] if (
            'cleanBody' in _clean and
            callable(_clean['cleanBody'])
        ) else (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        
        query = {
            '_or': list(
                map(
                    lambda body: initQueryBody(body),
                    bodies,
                ),
            ),
        }

        bodies = list(
            map(
                lambda body: cleanBody(body),
                bodies,
            ),
        )
        bodies = removeAttributesOfObject(bodies)

        session.begin()
        cleanedDatas = []
        exist = False
        bodiesClone = deepcopy(bodies)
        for index, body in enumerate(bodiesClone):
            query = initQueryBody(body)
            exists = _PD_exists(
                query = query,
                _kit = { 'readModel': Dataframe },
            )['exists']
            
            # if DEBUG :
                # print("> main.scripts._edit_multiple | index:: ", index)
                # print("> main.scripts._edit_multiple | body:: ", body)
                # print("> main.scripts._edit_multiple | query:: ", query)
                # print("> main.scripts._edit_multiple | exists:: ", exists)

            validatedata = None
            if(exists == True):
                # if DEBUG :
                    # print("> main.scripts._edit_multiple - UPDATE <")
                exist = True
                validatedata = formUpdate.validate(body)
                # if DEBUG :
                    # print("> main.scripts._edit_multiple | formUpdate:: ", formUpdate)
            else:
                # if DEBUG :
                    # print("> main.scripts._edit_multiple - ADD <")
                validatedata = formAdd.validate(body)
                # if DEBUG :
                    # print("> main.scripts._edit_multiple | formAdd:: ", formAdd)
                # if DEBUG :
                    # print("> main.scripts._edit_multiple | validatedata:: ", validatedata)
            if(validatedata['valid'] == True):
                cleanedData = None
                # if DEBUG :
                    # print("> main.scripts._PD_edit | exists:: ", exists)
                if(exists == True):
                    queryExists = query
                    queryReadWrite = query
                    oldElement = _PD_findOne(
                        query = queryExists,
                        _kit = { 'readModel': Dataframe },
                    )['data']
                    cleanedData = cleanDataUpdate(
                        oldData=oldElement,
                        newData=validatedata['data'],
                        nullableAttributes=nullableAttributes,
                        exists=exists,
                        lang=lang,
                    )
                    SQLAQF = queryFilter(
                        __PKQuery(
                            queryReadWrite,
                            model = Dataframe,
                            mapFunct = _mapActionPK
                        ),
                        Table = writeModel,
                    )
                    session.query(writeModel).filter(SQLAQF).update(cleanedData)
                else:
                    cleanedData = cleanDataAdd(data = validatedata['data'], exist=exist, lang=lang)
                    session.add(writeModel(**cleanedData))
                # if DEBUG :
                    # print("> main.scripts._PD_edit | cleanedData:: ", cleanedData)
                cleanedDatas.append(cleanedData)
            else:
                return {
                    'type': responsesPossibles['invalid_form']['type'],
                    'code': responsesPossibles['invalid_form']['code'],
                    'message': str(validatedata['error']),
                }
                
        res = {
            'data': cleanedDatas,
            'type': 'success',
        }

        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
        # if DEBUG :
            # print("> main.scripts._edit_multiple | res:: ", res)

        session.commit()

        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        session.rollback()

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }

def _PD_delete_multiple(
    params: dict,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda data, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    params = deepcopy(params)
    lang = deepcopy(lang)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'id': {
                '$eq': data['id'],
            },
        })
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        _clean = _clean if type(_clean) == dict else {}
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        Dataframe = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None

        paramsClone = []
        for index, param in enumerate(params):
            paramVal = initQueryBody(params[index])
            paramsClone.append(paramVal)
        # if DEBUG :
            # print("> main.scripts._PD_delete_multiple | params:: ", params)
            # print("> main.scripts._PD_delete_multiple | paramsClone:: ", paramsClone)
        
        query = {
            '_or': paramsClone
        }

        if 'lang' in query.keys():
            del query['lang']
        lang = getLang(lang)
        queryExists = query
        queryFinal = deepcopy(query)

        # if DEBUG :
            # print("> main.scripts._PD_delete_multiple | queryExists:: ", queryExists)
            # print("> main.scripts._PD_delete_multiple | queryFinal:: ", queryFinal)
        exists = _PD_exists(
            query = queryExists,
            _kit = { 'readModel': Dataframe },
        )['exists']
        # if DEBUG :
            # print("> main.scripts._PD_delete_multiple | query:: ", query)
            # print("> main.scripts._PD_delete_multiple | exists:: ", exists)
        if(exists == True):
            SQLAQF = queryFilter(
                query = __PKQuery(
                    queryFinal,
                    model = Dataframe,
                    mapFunct = _mapActionPK
                ),
                Table = writeModel,
            )
            session.query(writeModel).filter(SQLAQF).delete()
            session.commit()

            res = {
                'data': params,
                'type': 'success',
            }

            res = _supAction(data = params, exists = exists, lang = lang, res = res)
        else:
            return {
                'type': responsesPossibles['data_doesnt_exists']['type'],
                'code': responsesPossibles['data_doesnt_exists']['code'],
                'message': responsesPossibles['data_doesnt_exists']['message'][lang],
            }


        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_archiveOrRestore_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        _clean = _clean if type(_clean) == dict else {}
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        
        query = {
            '_or': list(
                map(
                    lambda param: initQueryBody(param),
                    params,
                )
            )
        }

        bodies = []
        for index, param in enumerate(params):
            val = deepcopy(param)
            val['status'] = 'visible'
            bodies.append(val)
        # if DEBUG :
            # print("> _PD_archiveOrRestore_multiple - bodies:: ", bodies)
            # print("> _PD_archiveOrRestore_multiple - query:: ", query)
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['status'] = 'visible' if (oldData['status'] == 'archived') else 'archived'
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        return _PD_update_multiple(
            # query = query,
            bodies = bodies,
            lang = lang,
            nullableAttributes=nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': None,
                'cleanData': cleanDataFunct,
                'initQueryBody': initQueryBody,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_blockOrUnblock_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        _clean = _clean if type(_clean) == dict else {}
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        
        query = {
            '_or': list(
                map(
                    lambda param: initQueryBody(param),
                    params,
                )
            )
        }

        bodies = []
        for index, param in enumerate(params):
            val = deepcopy(param)
            val['blocked'] = False
            bodies.append(val)
        # if DEBUG :
            # print("> _PD_archiveOrRestore_multiple - bodies:: ", bodies)
            # print("> _PD_archiveOrRestore_multiple - query:: ", query)
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['blocked'] = False if (oldData['blocked'] == True) else True
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        return _PD_update_multiple(
            # query = query,
            bodies = bodies,
            lang = lang,
            nullableAttributes=nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': None,
                'cleanData': cleanDataFunct,
                'initQueryBody': initQueryBody,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }
def _PD_publishOrUnpublish_multiple(
    params: dict,
    lang: str,
    nullableAttributes: list = [],
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
        'form': None,
    },
    _clean: dict = {
        'initQueryBody': lambda body: {
            'id': {
                '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
            }
        },
    },
    _supAction = lambda datas, bodies, exist, lang, res : res,
    _mapActionPK = lambda data : {
        'id': {
            '$eq': data['id'],
        },
    },
):
    params = deepcopy(params)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    try:
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        _clean = _clean if type(_clean) == dict else {}
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: {
                'id': {
                    '$eq': (body['_id'] if type(body) == dict and '_id' in body.keys() else None) if (body['_id'] if type(body) == dict and '_id' in body.keys() else None) else (body['id'] if type(body) == dict and 'id' in body.keys() else None)
                }
            }
        )
        
        query = {
            '_or': list(
                map(
                    lambda param: initQueryBody(param),
                    params,
                )
            )
        }

        bodies = []
        for index, param in enumerate(params):
            val = deepcopy(param)
            val['published'] = False
            bodies.append(val)
        # if DEBUG :
            # print("> _PD_archiveOrRestore_multiple - bodies:: ", bodies)
            # print("> _PD_archiveOrRestore_multiple - query:: ", query)
        def cleanDataFunct(oldData: dict, newData: dict, nullableAttributes: list, exists: bool, lang: str):
            newData['published'] = False if (oldData['published'] == True) else True
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        return _PD_update_multiple(
            # query = query,
            bodies = bodies,
            lang = lang,
            nullableAttributes=nullableAttributes,
            _kit = _kit,
            _clean = {
                'cleanBody': None,
                'cleanData': cleanDataFunct,
                'initQueryBody': initQueryBody,
            },
            _supAction = _supAction,
            _mapActionPK = _mapActionPK,
        )
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'type': 'danger',
            'code': '0001__unknown_error',
            'message': msg,
            'stack': stack if DEBUG else None,
            # 'trace': sys.exc_info()[2],
        }

def _PD_export(
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
):
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    progressive = deepcopy(progressive)
    _clean = deepcopy(_clean)
    export_type = deepcopy(export_type)
    title = deepcopy(title)
    filename = deepcopy(filename)
    columns = deepcopy(columns)
    lang = deepcopy(lang)

    elemntForFindAll = _PD_findAll(
        query = query,
        _kit = _kit,
        progressive = progressive,
        _clean = _clean,
    )
    datas = elemntForFindAll["datas"]
    # export_type = "csv"
    # if DEBUG :
        # print("> pd_crud - _PD_export | query:: ", query)
        # print("> pd_crud - _PD_export | _kit:: ", _kit)
        # print("> pd_crud - _PD_export | progressive:: ", progressive)
        # print("> pd_crud - _PD_export | _clean:: ", _clean)
        # print("> pd_crud - _PD_export | elemntForFindAll:: ", elemntForFindAll)
        # print("> pd_crud - _PD_export | datas:: ", datas)
        # print("> pd_crud - _PD_export | export_type:: ", export_type)

    return Export(
        filename,
        export_type = export_type,
        datas = {
            'rows': datas,
            'columnsConf': columns,
            'title': title,
            'lang': lang,
        },
    )

def _PD_extract(
    file,
    rows = {},
    columns = {},
    cleanData = (lambda x: x),
    schemas = {},
):
    # file = deepcopy(file)
    rows = deepcopy(rows)
    columns = deepcopy(columns)
    cleanData = deepcopy(cleanData)
    schemas = deepcopy(schemas)

    return Import(
        file = file,
        rows = rows,
        columns = columns,
        cleanData = cleanData,
        schemas = schemas,
    )