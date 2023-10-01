from typing import *
import asyncio
import logging
import traceback
import sys
from copy import deepcopy
import pandas as pd
from sqlalchemy.orm import load_only
from sqlalchemy.orm.query import Query
from sqlalchemy import func, select

from .objects import loopObject, removeAttributesOfObject
from .SQLAUtil import queryFilter, querySessionPagination, querySessionSort
from .file import Export, Import
from .sql import session
from .config import pagesPossibles, responsesPossibles
from .utils import ElementForUpdate, getLang, getIdBody, CRUDCleanFinalDatas
from .hivi_init import Manager
from sqlalchemy.orm import aliased


manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)
sessionF = session


def _SQL__PKQuery(query: dict, model, mapFunct = lambda data: {
    'slug': {
        '$eq': data['slug'],
    },
}):
    query = deepcopy(query)
    model = deepcopy(model)
    mapFunct = deepcopy(mapFunct)

    try:
        mapFunct = mapFunct if callable(mapFunct) else (lambda data: {
            'slug': {
                '$eq': data['slug'],
            },
        })
        query = query if type(query) == dict else {}
        query.update({
            '_pageSize': -1,
        })
        res = _SQL_findAll(query, _kit = {
            'readModel': model,
        })
        allDatas = res['datas']
        # print("> main.scripts._SQL__PKQuery | query:: ", query)
        # print("> main.scripts._SQL__PKQuery | model:: ", model)
        # print("> main.scripts._SQL__PKQuery | res:: ", res)
        # print("> main.scripts._SQL__PKQuery | allDatas:: ", allDatas)
        res = {
            '_or': list(
                map(
                    lambda elmt: {
                        'id': {
                            '$eq': elmt['id'],
                        },
                    },
                    allDatas,
                ),
            )
        }
        # print("> main.scripts._SQL__PKQuery | res:: ", res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None


def _SQL_findAll(
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
        Table: any = readModel
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
        attributes = deepcopy(query['_attributes']) if (
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

        # print("> Scripts - crud | findAll - sort:: ", sort)
        # print("> Scripts - crud | findAll - attributes:: ", attributes)

        # filter
        QF, TableF = queryFilter(
            query,
            Table = Table,
        )
        Table = TableF
        # print("> Scripts - crud | findAll - Table:: ", Table)
        # print("> Scripts - crud | findAll - query:: ", query)
        # print("> Scripts - crud | findAll - QF:: ", QF)
        # print("> Scripts - crud | findAll - type(QF):: ", type(QF))
        # print("> Scripts - crud | findAll - QF:: ", QF)
        
        """preSessionQuery = sessionF.query(TableF).options(load_only(*list(
            map(
                lambda attribute: getattr(TableF, attribute),
                deepcopy(attributes),
            )
        ))) if len(attributes) > 0 else sessionF.query(TableF)"""
        sessionQuery = sessionF.query(Table).filter(QF) if(len(query.keys()) > 0) else sessionF.query(Table).filter()
        # print("> Scripts - crud | findAll - sessionQuery:: ", sessionQuery)
        # sort
        sessionQuery = querySessionSort(sessionQuery, sort, Table = Table)
        # pagination
        queryPagination, pagination = querySessionPagination(sessionQuery, page = page, pageSize = pageSize, progressive = progressive)

        result = [q.__dict__ for q in queryPagination.all()]

        result = deepcopy(result) if type(result) in (list, tuple) else []
        for index, value in enumerate(result):
            if(type(result[index]) == dict and '_sa_instance_state' in result[index].keys()):
                del result[index]['_sa_instance_state']


        # map
        result = list(
            map(
                cleanData,
                result,
            )
        )
        
        # print("> Scripts - crud | findAll - result:: ", result)

        return {
            'datas': result,
            'meta': {
                'pagination': pagination,
            },
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message']['fr'],
            },
        }
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)
            
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
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message']['fr'],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            }
            
        }
def _SQL_findOne(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
    _clean: dict = {
        'cleanData': lambda x: x,
    },
    attributes: 'list|tuple' = [],
):
    # print("> main.scripts._SQL_findOne | query - old:: ", query)
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _clean = deepcopy(_clean)
    attributes = deepcopy(attributes)
    
    try:
        _kit = _kit if type(_kit) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Table: any = readModel
        _clean = _clean if type(_clean) == dict else {
            'cleanData': lambda x: x,
        }
        cleanData = _clean['cleanData'] if (
            'cleanData' in _clean and
            callable(_clean['cleanData'])
        ) else (lambda x: x)
        query = query if type(query) == dict else {}
        attributes = list(attributes) if (
            type(attributes) in (list, tuple)
        )  else []
        attributes = list(
            filter(
                lambda x: type(x) == str,
                attributes,
            )
        )
        # print("> main.scripts._SQL_findOne | attributes:: ", attributes)

        # filter
        QF, TableF = queryFilter(
            query,
            Table = Table,
        )
        Table = TableF
        count = 0
        exists = False
        row = None

        # print("> main.scripts._SQL_findOne | query:: ", query)
        if(len(query.keys()) > 0):
            """cleanAttributes = list(
                map(
                    lambda attribute: getattr(Table, attribute),
                    deepcopy(attributes),
                )
            )"""
            """sessionQuery = sessionF.query(Table).filter(QF).options(
                load_only(*cleanAttributes)
            ) if len(attributes) > 0 else sessionF.query(Table).filter(QF)"""
            sessionQuery = sessionF.query(Table).filter(QF)
            # print("> main.scripts._SQL_findOne | query:: ", query)
            # print("> main.scripts._SQL_findOne | QF:: ", QF)
            # print("> main.scripts._SQL_findOne | sessionQuery:: ", sessionQuery)
            # print("> main.scripts._SQL_findOne | sessionQuery.one():: ", sessionQuery.one())
            count = sessionQuery.count()
            count = count if type(count) in (int, float) else 0
            exists = (count > 0)
            # print("> main.scripts._SQL_findOne | cleanAttributes:: ", cleanAttributes)
            # print("> main.scripts._SQL_findOne | count:: ", count)
            # print("> main.scripts._SQL_findOne | exists:: ", exists)
            # print("> main.scripts._SQL_findOne | sessionQuery:: ", sessionQuery)
            if(exists):
                _row = None
                if count > 1:
                    _row = sessionQuery.limit(1).all()[0]
                    if(type(_row) == dict and '_sa_instance_state' in _row.keys()):
                        del _row['_sa_instance_state']
                else:
                    _row = sessionQuery.one()

                row = {}
                for column in _row.__table__.columns:
                    row[column.name] = getattr(_row, column.name)
                row = cleanData(row)

        return {
            'data': row,
            'exists': exists,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message']['fr'],
            },
        }
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)
            
        return {
            'data': None,
            'exists': False,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message']['fr'],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            }
        }
def _SQL_exists(
    query: any,
    _kit: dict = {
        'readModel': None,
    },
):
    query = deepcopy(query)
    _kit = deepcopy(_kit)
    # sessionF = deepcopy(sessionF)
    
    res = None
    try:
        _kit = _kit if type(_kit) == dict else {}
        readModel = deepcopy(_kit['readModel'] if (
            'readModel' in _kit
        ) else None)
        Table: any = deepcopy(readModel)
        query = query if type(query) == dict else {}

        # filter
        QF, TableF = queryFilter(
            query,
            Table = Table,
        )
        Table = TableF
        count = 0
        exists = False

        # print("> main.scripts._SQL_exists | Table:: ", Table)
        # print("> main.scripts._SQL_exists | query:: ", query)
        # print("> main.scripts._SQL_exists | QF:: ", QF)

        if(len(query.keys()) > 0):
            sessionQuery = sessionF.query(Table).filter(QF)
            count = sessionQuery.count()
            # print("> main.scripts._SQL_exists | sessionQuery:: ", sessionQuery)
            # print("> main.scripts._SQL_exists | count:: ", count)
            count = deepcopy(count) if type(count) in (int, float) else 0
            exists = (count > 0)
        # print("> main.scripts._SQL_exists | exists:: ", exists)

        res = {
            'exists': exists,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message']['fr'],
            },
        }
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)
            
        res = {
            'exists': False,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message']['fr'],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            }
        }
    # print("> main.scripts._SQL_exists | res:: ", res)
    sessionF.flush()
    return res

def _SQL_add(
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
        Table = readModel
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

        body = cleanBody(body)
        validatedata = form.validate(body)
        # print("> main.scripts._SQL_add | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            exists = _SQL_exists(
                query = query,
                _kit = { 'readModel': Table },
            )['exists']
            # print("> main.scripts._SQL_add | exists:: ", exists)
            if(exists == True):
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['data_exists']['type'],
                        'code': responsesPossibles['data_exists']['code'],
                        'status': responsesPossibles['data_exists']['status'],
                        'message': responsesPossibles['data_exists']['message'][lang],
                    }
                }
            else:
                cleanedData = cleanData(data = validatedata['data'], exists=exists, lang=lang)
                # print("> main.scripts._SQL_add | cleanedData:: ", cleanedData)
                sessionF.add(writeModel(**cleanedData))
                sessionF.commit()

                res = {
                    'data': cleanedData,
                    'notif': {
                        'type': responsesPossibles['good_action']['type'],
                        'code': responsesPossibles['good_action']['code'],
                        'status': responsesPossibles['good_action']['status'],
                        'message': responsesPossibles['good_action']['message'][lang],
                    },
                }

                res = _supAction(data = validatedata['data'], body = body, exists = exists, lang = lang, res = res)
        else:
            return {
                'data': None,
                'notif': {
                    'type': responsesPossibles['invalid_form']['type'],
                    'code': responsesPossibles['invalid_form']['code'],
                    'status': responsesPossibles['invalid_form']['status'],
                    'message': str(validatedata['error']),
                }
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            }
        }
def _SQL_update(
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
        'slug': {
            '$eq': data['slug'],
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
            'slug': {
                '$eq': data['slug'],
            },
        })
        nullableAttributes = list(
            filter(
                lambda x: x in (int, float, str),
                nullableAttributes,
            )
        ) if type(nullableAttributes) in (list, tuple) else []
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
        Table = readModel
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

        body = cleanBody(body)
        validatedata = form.validate(body)
        # print("> main.scripts._SQL_add | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            exists = _SQL_exists(
                query = query,
                _kit = { 'readModel': Table },
            )['exists']
            oldElementAction = _SQL_findOne(
                query = query,
                _kit = { 'readModel': Table },
            )
            oldElement = oldElementAction['data'] if oldElementAction['data'] is not None else validatedata['data']
            if(exists == True):
                cleanedData = cleanData(
                    oldData = oldElement,
                    newData = validatedata['data'],
                    nullableAttributes = nullableAttributes,
                    exists=exists,
                    lang=lang,
                )
                # print("> main.scripts._SQL_add | cleanedData:: ", cleanedData)
                
                cleanedQueryForTable = _SQL__PKQuery(
                    query,
                    model = readModel,
                    mapFunct = _mapActionPK
                )
                SQLAQF, TableF = queryFilter(
                    cleanedQueryForTable,
                    Table = writeModel,
                )
                Table = TableF
                sessionF.query(writeModel).filter(SQLAQF).update(cleanedData)
                sessionF.commit()

                res = {
                    'data': cleanedData,
                    'notif': {
                        'type': responsesPossibles['good_action']['type'],
                        'code': responsesPossibles['good_action']['code'],
                        'status': responsesPossibles['good_action']['status'],
                        'message': responsesPossibles['good_action']['message'][lang],
                    },
                }

                res = _supAction(data = validatedata['data'], body = body, exists = exists, lang = lang, res = res)
            else:
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['data_doesnt_exists']['type'],
                        'code': responsesPossibles['data_doesnt_exists']['code'],
                        'status': responsesPossibles['data_doesnt_exists']['status'],
                        'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                    },
                }
        else:
            return {
                'data': None,
                'notif': {
                    'type': responsesPossibles['invalid_form']['type'],
                    'code': responsesPossibles['invalid_form']['code'],
                    'status': responsesPossibles['invalid_form']['status'],
                    'message': str(validatedata['error']),
                },
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            }
        }
def _SQL_edit(
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
        'slug': {
            '$eq': data['slug'],
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
            'slug': {
                '$eq': data['slug'],
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

        exists = _SQL_exists(
            query = queryExists,
            _kit = { 'readModel': readModel },
        )['exists']
        
        # print("> main.scripts._SQL_edit | body:: ", body)
        # print("> main.scripts._SQL_edit | query:: ", query)
        # print("> main.scripts._SQL_edit | exists:: ", exists)

        body = cleanBody(body)
        body = removeAttributesOfObject(body)
        validatedata = None
        if(exists == True):
            # print("> main.scripts._SQL_edit - UPDATE <")
            exist = True
            validatedata = formUpdate.validate(body)
            # print("> main.scripts._SQL_edit | formUpdate:: ", formUpdate)
        else:
            # print("> main.scripts._SQL_edit - ADD <")
            validatedata = formAdd.validate(body)
            # print("> main.scripts._SQL_edit | formAdd:: ", formAdd)
        
        # print("> main.scripts._SQL_edit | validatedata:: ", validatedata)
        if(validatedata['valid'] == True):
            cleanedData = None
            if(exists == True):
                SQLAQF, TableF = queryFilter(
                    _SQL__PKQuery(
                        queryReadWrite,
                        model = readModel,
                        mapFunct = _mapActionPK
                    ),
                    Table = writeModel,
                )
                writeModel = TableF
                oldElement = _SQL_findOne(
                    query = queryReadWrite2,
                    _kit = { 'readModel': readModel },
                )['data']
                cleanedData = cleanDataUpdate(
                    oldData=oldElement,
                    newData=validatedata['data'],
                    nullableAttributes=nullableAttributes,
                    exists=exists,
                    lang=lang,
                )
                sessionF.query(writeModel).filter(SQLAQF).update(cleanedData)
            else:
                cleanedData = cleanDataAdd(data = validatedata['data'], exists=exists, lang=lang)
                sessionF.add(writeModel(**cleanedData))
            sessionF.commit()
            # print("> main.scripts._SQL_edit | cleanedData:: ", cleanedData)

            res = {
                'data': cleanedData,
                'notif': {
                    'type': responsesPossibles['good_action']['type'],
                    'code': responsesPossibles['good_action']['code'],
                    'status': responsesPossibles['good_action']['status'],
                    'message': responsesPossibles['good_action']['message'][lang],
                },
            }
            res = _supAction(data = validatedata['data'], body = body, exists = exists, lang = lang, res = res)

            return res
        else:
            return {                
                'data': None,
                'notif': {
                    'type': responsesPossibles['invalid_form']['type'],
                    'code': responsesPossibles['invalid_form']['code'],
                    'status': responsesPossibles['invalid_form']['status'],
                    'message': str(validatedata['error']),
                },
            }
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }

def _SQL_delete(
    query: dict,
    lang: str,
    _kit: dict = {
        'readModel': None,
        'writeModel': None,
    },
    _supAction = lambda data, exists, lang, res : res,
    _mapActionPK = lambda data : {
        'slug': {
            '$eq': data['slug'],
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
            'slug': {
                '$eq': data['slug'],
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
        Table = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None

        queryExists = query
        queryReadWrite = query
        exists = _SQL_exists(
            query = queryExists,
            _kit = { 'readModel': Table },
        )['exists']
        if(exists == True):
            cleanedData = _SQL_findOne(
                query = queryReadWrite,
                _kit = {
                    'readModel': Table,
                },
            )['data']
            # print("> main.scripts._SQL_add | query:: ", query)
            
            SQLAQF, TableF = queryFilter(
                _SQL__PKQuery(
                    query,
                    model = Table,
                    mapFunct = _mapActionPK
                ),
                Table = writeModel,
            )
            writeModel = TableF
            sessionF.query(writeModel).filter(SQLAQF).delete()
            sessionF.commit()

            res = {
                'data': cleanedData,
                'notif': {
                    'type': responsesPossibles['good_action']['type'],
                    'code': responsesPossibles['good_action']['code'],
                    'status': responsesPossibles['good_action']['status'],
                    'message': responsesPossibles['good_action']['message'][lang],
                },
            }

            res = _supAction(data = validatedata['data'], exists = exists, lang = lang, res = res)
        else:
            return {
                'data': None,
                'notif': {
                    'type': responsesPossibles['data_doesnt_exists']['type'],
                    'code': responsesPossibles['data_doesnt_exists']['code'],
                    'status': responsesPossibles['invalid_form']['status'],
                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                },
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_archiveOrRestore(
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
        'slug': {
            '$eq': data['slug'],
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
        # print("> _SQL_archiveOrRestore - body:: ", body)
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
        return _SQL_update(
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_archive(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _SQL_restore(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_archiveOrRestore(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )
def _SQL_blockOrUnblock(
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
        'slug': {
            '$eq': data['slug'],
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
        return _SQL_update(
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_block(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _SQL_unblock(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_blockOrUnblock(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )
def _SQL_publishOrUnpublish(
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
        'slug': {
            '$eq': data['slug'],
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
        return _SQL_update(
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
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_publish(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "primary",
    )
def _SQL_unpublish(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    query = deepcopy(query)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)

    return _SQL_publishOrUnpublish(
        query = query,
        lang = lang,
        nullableAttributes = nullableAttributes,
        _kit = _kit,
        _supAction = _supAction,
        _mapActionPK = _mapActionPK,
        _actionStrict = "reverse",
    )

def _SQL_add_multiple(
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
        Table = readModel
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
            lambda body: getIdBody(body)
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
        
        cleanedDatas = []

        sessionF.close_all()
        with sessionF.begin():
            exist = False
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForAdd = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None

            validatedata: dict = deepcopy(form.validate(bodiesClone))
            isValid = validatedata['valid']
            # print("> main.scripts._SQL_add_multiple | form:: ", form)
            # print("> main.scripts._SQL_add_multiple | exceptInvalidElement:: ", exceptInvalidElement)
            if(isValid):
                allDataIsValid = True
                
                for index, body in enumerate(bodiesClone):
                    # body = deepcopy(body)
                    queryBody = deepcopy(initQueryBody(body))
                    reqSUB = deepcopy(_SQL_findOne(
                        query = queryBody,
                        _kit = { 'readModel': Table },
                    ))
                    exists = deepcopy(reqSUB['exists'])
                    isValid = False
                    if exists == True:
                        return {
                            'notif': {
                                'type': responsesPossibles['data_exists']['type'],
                                'code': responsesPossibles['data_exists']['code'],
                                'status': responsesPossibles['data_exists']['status'],
                                'message': responsesPossibles['data_exists']['message'][lang],
                            },
                        }
                    else:
                        validatedata['data'][index] = cleanData(data = validatedata['data'][index], exists = exists, lang = lang) if isValid else validatedata['data'][index]
                        validatedata['data'][index] = validatedata['data'][index] if validatedata['data'][index] is not None else {}
                        allElementForAdd.append(writeModel(**validatedata['data'][index]))
                    allCheck.append(exists)
            else:
                # print("> main.scripts._SQL_add_multiple | form:: ", form)
                # print("> main.scripts._SQL_add_multiple | exceptInvalidElement:: ", exceptInvalidElement)
                allDataIsValid = False
                return {
                    'notif': {
                        'type': responsesPossibles['invalid_form']['type'],
                        'code': responsesPossibles['invalid_form']['code'],
                        'status': responsesPossibles['invalid_form']['status'],
                        'message': str(validatedata['error']),
                    },
                }

            # print("> main.scripts._SQL_add_multiple | writeModel:: ", writeModel)
            # print("> main.scripts._SQL_add_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_add_multiple | allElementForAdd:: ", allElementForAdd)
            # print("> main.scripts._SQL_add_multiple | allDataIsValid:: ", allDataIsValid)

            # -> FOR ADD
            if len(allElementForAdd) > 0 :
                sessionF.add_all(allElementForAdd)
                sessionF.flush()
                cleanedDatas = deepcopy(cleanedDatas) + validatedata['data']

        sessionF.commit()
        sessionF.close_all()
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = True, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        sessionF.rollback()
        sessionF.close_all()

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_update_multiple(
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
        'slug': {
            '$eq': data['slug'],
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
            'slug': {
                '$eq': data['slug'],
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
        Table = readModel
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
            lambda body: getIdBody(body)
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

        cleanedDatas = []
        exist: bool = False

        sessionF.close_all()
        with sessionF.begin():
            exist = _SQL_exists(
                query = {
                    '_or': list(
                        map(
                            lambda body: deepcopy(initQueryBody(body)),
                            deepcopy(bodies),
                        )
                    )
                },
                _kit = {
                    'readModel': Table,
                },
            )['exists']
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForUpdate = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None

            validatedata: dict = deepcopy(form.validate(bodiesClone))
            isValid = validatedata['valid']
            # print("> main.scripts._SQL_update_multiple | form:: ", form)
            # print("> main.scripts._SQL_update_multiple | exceptInvalidElement:: ", exceptInvalidElement)
            if(isValid):
                allDataIsValid = True
                if exist == True :
                    for index, body in enumerate(bodiesClone):
                        # body = deepcopy(body)
                        queryBody = deepcopy(initQueryBody(body))
                        reqSUB = deepcopy(_SQL_findOne(
                            query = queryBody,
                            _kit = { 'readModel': Table },
                        ))
                        exists = deepcopy(reqSUB['exists'])
                        isValid = False
                        if exists == True:
                            validatedata['data'][index] = cleanData(
                                oldData= reqSUB['data'],
                                newData = validatedata['data'][index],
                                nullableAttributes = nullableAttributes,
                                exists = exists,
                                lang = lang,
                            )
                            allElementForUpdate.append({
                                'data': validatedata['data'][index],
                                'query': _mapActionPK(reqSUB['data']),
                            })
                        else:
                            return {
                                'data': None,
                                'notif': {
                                    'type': responsesPossibles['data_doesnt_exists']['type'],
                                    'code': responsesPossibles['data_doesnt_exists']['code'],
                                    'status': responsesPossibles['data_doesnt_exists']['status'],
                                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                                },
                            }
                        allCheck.append(exists)
                else:
                    return {
                        'data': None,
                        'notif': {
                            'type': responsesPossibles['data_doesnt_exists']['type'],
                            'code': responsesPossibles['data_doesnt_exists']['code'],
                            'status': responsesPossibles['data_doesnt_exists']['status'],
                            'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                        },
                    }
            else:
                # print("> main.scripts._SQL_update_multiple | form:: ", form)
                # print("> main.scripts._SQL_update_multiple | exceptInvalidElement:: ", exceptInvalidElement)
                allDataIsValid = False
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['invalid_form']['type'],
                        'code': responsesPossibles['invalid_form']['code'],
                        'status': responsesPossibles['invalid_form']['status'],
                        'message': str(validatedata['error']),
                    },
                }
                
            # print("> main.scripts._SQL_update_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_update_multiple | allElementForUpdate:: ", allElementForUpdate)
            # print("> main.scripts._SQL_update_multiple | allDataIsValid:: ", allDataIsValid)
            

            if len(allElementForUpdate) > 0 :
                for indexAEFU, elementAEFU in enumerate(allElementForUpdate):
                    SQLAQF, TableF = queryFilter(
                        elementAEFU['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).update(elementAEFU['data'])
                    sessionF.flush()
                    cleanedDatas.append(elementAEFU['data'])

            sessionF.commit()
            sessionF.close_all()
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        sessionF.rollback()
        sessionF.close_all()

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_edit_multiple(
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
        'slug': {
            '$eq': data['slug'],
        },
    },
):
    # sessionF = deepcopy(sessionF)
    bodies = deepcopy(bodies)
    lang = deepcopy(lang)
    nullableAttributes = deepcopy(nullableAttributes)
    _kit = deepcopy(_kit)
    _clean = deepcopy(_clean)
    _supAction = deepcopy(_supAction)
    _mapActionPK = deepcopy(_mapActionPK)
    
    # print("> main.scripts._SQL_edit_multiple | bodies:: ", bodies)

    res = None
    try:
        sessionF.close_all()
        with sessionF.begin():
            _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
                'slug': {
                    '$eq': data['slug'],
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
            Table = readModel
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
                lambda body: getIdBody(body)
            )
            
            """query = {
                '_or': list(
                    map(
                        lambda body: initQueryBody(body),
                        bodies,
                    ),
                ),
            }"""

            bodies = list(
                map(
                    lambda body: cleanBody(body),
                    bodies,
                ),
            )
            bodies = removeAttributesOfObject(bodies)

            cleanedDatas = []
            exist = False
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForAddValid = []
            allElementForAdd = []
            allElementForUpdate = []
            allDataIsValid: bool = True
            invalidElement: dict = None
            for index, body in enumerate(bodiesClone):
                # body = deepcopy(body)
                queryBody = deepcopy(initQueryBody(body))
                reqSUB = deepcopy(_SQL_findOne(
                    query = queryBody,
                    _kit = { 'readModel': Table },
                ))
                # print("> main.scripts._SQL_edit_multiple | [", index, "] - queryBody :: ", queryBody)
                exists = deepcopy(reqSUB['exists'])
                isValid = False
                if exists == True:
                    validatedata: dict = deepcopy(formUpdate.validate(body))
                    isValid = validatedata['valid']
                    validatedata['data'] = cleanDataUpdate(
                        oldData= reqSUB['data'],
                        newData = validatedata['data'],
                        nullableAttributes = nullableAttributes,
                        exists = exists,
                        lang = lang,
                    )
                    allElementForUpdate.append({
                        'data': validatedata['data'],
                        'query': _mapActionPK(reqSUB['data']),
                    })
                    if not(isValid == True):
                        invalidElement = {
                            **validatedata,
                            **{
                                'body': body,
                            }
                        }
                    exist = True
                else:
                    validatedata: dict = deepcopy(formAdd.validate(body))
                    isValid = validatedata['valid']
                    # print("> main.scripts._SQL_edit_multiple | invalidElement:: ", invalidElement)
                    # print("> main.scripts._SQL_edit_multiple | ", index, " - old - validatedata['data']:: ", validatedata['data'])
                    validatedata['data'] = cleanDataAdd(data = validatedata['data'], exists = exists, lang = lang) if isValid else validatedata['data']
                    validatedata['data'] = validatedata['data'] if validatedata['data'] is not None else {}
                    # print("> main.scripts._SQL_edit_multiple | ", index, " - validatedata:: ", validatedata)
                    # print("> main.scripts._SQL_edit_multiple | ", index, " - body:: ", body)
                    allElementForAddValid.append(validatedata['data'])
                    allElementForAdd.append(writeModel(**validatedata['data']))
                if not(isValid == True) :
                    # print("> main.scripts._SQL_edit_multiple | invalidElement:: ", invalidElement)
                    allDataIsValid = False
                    return {
                        'data': None,
                        'notif': {
                            'type': responsesPossibles['invalid_form']['type'],
                            'code': responsesPossibles['invalid_form']['code'],
                            'status': responsesPossibles['invalid_form']['status'],
                            'message': str(validatedata['error']),
                        },
                    }
                else:
                    allDataIsValid = True
                allCheck.append(exists)
            # print("> main.scripts._SQL_edit_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_edit_multiple | allElementForAddValid:: ", allElementForAddValid)
            # print("> main.scripts._SQL_edit_multiple | allElementForAdd:: ", allElementForAdd)
            # print("> main.scripts._SQL_edit_multiple | allElementForUpdate:: ", allElementForUpdate)
            # print("> main.scripts._SQL_edit_multiple | allDataIsValid:: ", allDataIsValid)

            # -> FOR ADD
            if len(allElementForAdd) > 0 :
                sessionF.add_all(allElementForAdd)
                sessionF.flush()
                cleanedDatas = deepcopy(cleanedDatas) + allElementForAddValid
            # -> FOR UPDATE
            if len(allElementForUpdate) > 0 :
                for indexAEFU, elementAEFU in enumerate(allElementForUpdate):
                    SQLAQF, TableF = queryFilter(
                        elementAEFU['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).update(elementAEFU['data'])
                    sessionF.flush()
                    cleanedDatas.append(elementAEFU['data'])

            res = {
                'data': cleanedDatas,
                'notif': {
                    'type': responsesPossibles['good_action']['type'],
                    'code': responsesPossibles['good_action']['code'],
                    'status': responsesPossibles['good_action']['status'],
                    'message': responsesPossibles['good_action']['message'][lang],
                },
            }

            res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
            # print("> main.scripts._SQL_edit_multiple | res:: ", res)

            
            sessionF.commit()
            sessionF.close_all()

            return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        sessionF.rollback()
        sessionF.close_all()

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }

def _SQL_delete_multiple(
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
        'slug': {
            '$eq': data['slug'],
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
            'slug': {
                '$eq': data['slug'],
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
            lambda body: getIdBody(body)
        )
        Table = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None

        cleanedDatas = []
        exist: bool = False

        sessionF.close_all()
        with sessionF.begin():
            exist = _SQL_exists(
                query = {
                    '_or': list(
                        map(
                            lambda body: deepcopy(initQueryBody(body)),
                            deepcopy(params),
                        )
                    )
                },
                _kit = {
                    'readModel': Table,
                },
            )['exists']
            bodiesClone = deepcopy(params)

            allCheck = []
            allElementForDelete = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None
            
            if(exist == True):
                for index, body in enumerate(bodiesClone):
                    # body = deepcopy(body)
                    queryBody = deepcopy(initQueryBody(body))
                    reqSUB = deepcopy(_SQL_findOne(
                        query = queryBody,
                        _kit = { 'readModel': Table },
                    ))
                    exists = deepcopy(reqSUB['exists'])
                    isValid = False
                    if exists == True:
                        allElementForDelete.append({
                            'data': body,
                            'query': _mapActionPK(reqSUB['data']),
                        })
                    else:
                        return {
                            'data': None,
                            'notif': {
                                'type': responsesPossibles['data_doesnt_exists']['type'],
                                'code': responsesPossibles['data_doesnt_exists']['code'],
                                'status': responsesPossibles['data_doesnt_exists']['status'],
                                'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                            },
                        }
                    allCheck.append(exists)
            else:
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['data_doesnt_exists']['type'],
                        'code': responsesPossibles['data_doesnt_exists']['code'],
                        'status': responsesPossibles['data_doesnt_exists']['status'],
                        'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                    },
                }
                
            # print("> main.scripts._SQL_delete_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_delete_multiple | allElementForDelete:: ", allElementForDelete)
            # print("> main.scripts._SQL_delete_multiple | allDataIsValid:: ", allDataIsValid)
        
            if len(allElementForDelete) > 0 :
                for indexAEFU, elementAEFD in enumerate(allElementForDelete):
                    SQLAQF, TableF = queryFilter(
                        elementAEFD['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).delete()
                    sessionF.flush()
                    cleanedDatas.append(elementAEFD['data'])
                        
            sessionF.commit()
            sessionF.close_all()
        # print("> main.scripts._SQL_delete_multiple | cleanedDatas:: ", cleanedDatas)
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(data = cleanedDatas, exists = exist, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_archiveOrRestore_multiple(
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
        'slug': {
            '$eq': data['slug'],
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
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'slug': {
                '$eq': data['slug'],
            },
        })
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        lang = getLang(lang)
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Table = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        def cleanData(oldData, newData, nullableAttributes, exists, lang):
            newData['status'] = 'visible' if (oldData['status'] == 'archived') else 'archived'
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        cleanBody = (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: getIdBody(body)
        )
        _supAction = _supAction if callable(_supAction) else (lambda datas, bodies, exist, lang, res : res)
        
        
        cleanedDatas = []
        bodies = deepcopy(params)
        bodies = list(
            map(
                lambda body: cleanBody(body),
                bodies,
            ),
        )
        bodies = removeAttributesOfObject(bodies)
        exist: bool = False


        sessionF.close_all()
        with sessionF.begin():
            exist = _SQL_exists(
                query = {
                    '_or': list(
                        map(
                            lambda body: deepcopy(initQueryBody(body)),
                            deepcopy(bodies),
                        )
                    )
                },
                _kit = {
                    'readModel': Table,
                },
            )['exists']
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForArchiveOrRestoreMultiple = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None

            validatedata: dict = deepcopy(form.validate(bodiesClone))
            isValid = validatedata['valid']
            # print("> main.scripts._SQL_archiveOrRestore_multiple | form:: ", form)
            # print("> main.scripts._SQL_archiveOrRestore_multiple | exceptInvalidElement:: ", exceptInvalidElement)
            if(isValid):
                allDataIsValid = True
                if exist == True :
                    for index, body in enumerate(bodiesClone):
                        # body = deepcopy(body)
                        queryBody = deepcopy(initQueryBody(body))
                        reqSUB = deepcopy(_SQL_findOne(
                            query = queryBody,
                            _kit = { 'readModel': Table },
                        ))
                        exists = deepcopy(reqSUB['exists'])
                        isValid = False
                        if exists == True:
                            validatedata['data'][index] = cleanData(
                                oldData= reqSUB['data'],
                                newData = validatedata['data'][index],
                                nullableAttributes = nullableAttributes,
                                exists = exists,
                                lang = lang,
                            )
                            allElementForArchiveOrRestoreMultiple.append({
                                'data': validatedata['data'][index],
                                'query': _mapActionPK(reqSUB['data']),
                            })
                        else:
                            return {
                                'data': None,
                                'notif': {
                                    'type': responsesPossibles['data_doesnt_exists']['type'],
                                    'code': responsesPossibles['data_doesnt_exists']['code'],
                                    'status': responsesPossibles['data_doesnt_exists']['status'],
                                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                                },
                            }
                        allCheck.append(exists)
                else:
                    return {
                        'data': None,
                        'notif': {
                            'type': responsesPossibles['data_doesnt_exists']['type'],
                            'code': responsesPossibles['data_doesnt_exists']['code'],
                            'status': responsesPossibles['data_doesnt_exists']['status'],
                            'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                        },
                    }
            else:
                # print("> main.scripts._SQL_archiveOrRestore_multiple | form:: ", form)
                # print("> main.scripts._SQL_archiveOrRestore_multiple | exceptInvalidElement:: ", exceptInvalidElement)
                allDataIsValid = False
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['invalid_form']['type'],
                        'code': responsesPossibles['invalid_form']['code'],
                        'status': responsesPossibles['invalid_form']['status'],
                        'message': str(validatedata['error']),
                    },
                }

            if len(allElementForArchiveOrRestoreMultiple) > 0 :
                for indexAORM, elementAORM in enumerate(allElementForArchiveOrRestoreMultiple):
                    SQLAQF, TableF = queryFilter(
                        elementAORM['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).update(elementAORM['data'])
                    sessionF.flush()
                    cleanedDatas.append(elementAORM['data'])
            sessionF.commit()
            sessionF.close_all()

            # print("> main.scripts._SQL_archiveOrRestore_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_archiveOrRestore_multiple | allElementForArchiveOrRestoreMultiple:: ", allElementForArchiveOrRestoreMultiple)
            # print("> main.scripts._SQL_archiveOrRestore_multiple | allDataIsValid:: ", allDataIsValid)
            
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = exist, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_blockOrUnblock_multiple(
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
        'slug': {
            '$eq': data['slug'],
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
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'slug': {
                '$eq': data['slug'],
            },
        })
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        lang = getLang(lang)
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Table = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        def cleanData(oldData, newData, nullableAttributes, exists, lang):
            newData['blocked'] = False if (oldData['blocked'] == True) else True
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        cleanBody = (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: getIdBody(body)
        )
        _supAction = _supAction if callable(_supAction) else (lambda datas, bodies, exist, lang, res : res)
        
        
        cleanedDatas = []
        bodies = deepcopy(params)
        bodies = list(
            map(
                lambda body: cleanBody(body),
                bodies,
            ),
        )
        bodies = removeAttributesOfObject(bodies)


        sessionF.close_all()
        with sessionF.begin():
            exist = _SQL_exists(
                query = {
                    '_or': list(
                        map(
                            lambda body: deepcopy(initQueryBody(body)),
                            deepcopy(bodies),
                        )
                    )
                },
                _kit = {
                    'readModel': Table,
                },
            )['exists']
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForBlockOrUnblockMultiple = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None

            validatedata: dict = deepcopy(form.validate(bodiesClone))
            isValid = validatedata['valid']
            # print("> main.scripts._SQL_blockOrUnblock_multiple | form:: ", form)
            # print("> main.scripts._SQL_blockOrUnblock_multiple | exceptInvalidElement:: ", exceptInvalidElement)
            if(isValid):
                allDataIsValid = True
                if exist == True :
                    for index, body in enumerate(bodiesClone):
                        # body = deepcopy(body)
                        queryBody = deepcopy(initQueryBody(body))
                        reqSUB = deepcopy(_SQL_findOne(
                            query = queryBody,
                            _kit = { 'readModel': Table },
                        ))
                        exists = deepcopy(reqSUB['exists'])
                        isValid = False
                        if exists == True:
                            validatedata['data'][index] = cleanData(
                                oldData= reqSUB['data'],
                                newData = validatedata['data'][index],
                                nullableAttributes = nullableAttributes,
                                exists = exists,
                                lang = lang,
                            )
                            allElementForBlockOrUnblockMultiple.append({
                                'data': validatedata['data'][index],
                                'query': _mapActionPK(reqSUB['data']),
                            })
                        else:
                            return {
                                'data': None,
                                'notif': {
                                    'type': responsesPossibles['data_doesnt_exists']['type'],
                                    'code': responsesPossibles['data_doesnt_exists']['code'],
                                    'status': responsesPossibles['data_doesnt_exists']['status'],
                                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                                },
                            }
                        allCheck.append(exists)
                else:
                    return {
                        'data': None,
                        'notif': {
                            'type': responsesPossibles['data_doesnt_exists']['type'],
                            'code': responsesPossibles['data_doesnt_exists']['code'],
                            'status': responsesPossibles['data_doesnt_exists']['status'],
                            'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                        },
                    }
            else:
                # print("> main.scripts._SQL_blockOrUnblock_multiple | form:: ", form)
                # print("> main.scripts._SQL_blockOrUnblock_multiple | exceptInvalidElement:: ", exceptInvalidElement)
                allDataIsValid = False
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['invalid_form']['type'],
                        'code': responsesPossibles['invalid_form']['code'],
                        'status': responsesPossibles['invalid_form']['status'],
                        'message': str(validatedata['error']),
                    },
                }

            if len(allElementForBlockOrUnblockMultiple) > 0 :
                for indexAORM, elementAORM in enumerate(allElementForBlockOrUnblockMultiple):
                    SQLAQF, TableF = queryFilter(
                        elementAORM['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).update(elementAORM['data'])
                    sessionF.flush()
                    cleanedDatas.append(elementAORM['data'])

            # print("> main.scripts._SQL_blockOrUnblock_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_blockOrUnblock_multiple | allElementForArchiveOrRestoreMultiple:: ", allElementForArchiveOrRestoreMultiple)
            # print("> main.scripts._SQL_blockOrUnblock_multiple | allDataIsValid:: ", allDataIsValid)

            sessionF.commit()
            sessionF.close_all()
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = True, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
def _SQL_publishOrUnpublish_multiple(
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
        'slug': {
            '$eq': data['slug'],
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
        _mapActionPK = _mapActionPK if callable(_mapActionPK) else (lambda data: {
            'slug': {
                '$eq': data['slug'],
            },
        })
        params = list(
            filter(
                lambda param: type(param) == dict,
                params,
            )
        ) if type(params) in (list, tuple) else []
        lang = getLang(lang)
        _kit = _kit if type(_kit) == dict else {}
        _clean = _clean if type(_clean) == dict else {}
        readModel = _kit['readModel'] if (
            'readModel' in _kit
        ) else None
        Table = readModel
        writeModel = _kit['writeModel'] if (
            'writeModel' in _kit
        ) else None
        form = _kit['form'] if (
            'form' in _kit
        ) else None
        def cleanData(oldData, newData, nullableAttributes, exists, lang):
            newData['published'] = False if (oldData['published'] == True) else True
            return ElementForUpdate(
                oldElement=oldData,
                newElement=newData,
                nullableAttributes=nullableAttributes,
            )
        cleanBody = (lambda x: x)
        initQueryBody = _clean['initQueryBody'] if (
            'initQueryBody' in _clean and
            callable(_clean['initQueryBody'])
        ) else (
            lambda body: getIdBody(body)
        )
        _supAction = _supAction if callable(_supAction) else (lambda datas, bodies, exist, lang, res : res)
        
        
        cleanedDatas = []
        bodies = deepcopy(params)

        sessionF.close_all()
        with sessionF.begin():
            exist = _SQL_exists(
                query = {
                    '_or': list(
                        map(
                            lambda body: deepcopy(initQueryBody(body)),
                            deepcopy(bodies),
                        )
                    )
                },
                _kit = {
                    'readModel': Table,
                },
            )['exists']
            bodiesClone = deepcopy(bodies)

            allCheck = []
            allElementForPublishOrUnpublishMultiple = []
            allDataIsValid: bool = True
            exceptInvalidElement: dict = None

            validatedata: dict = deepcopy(form.validate(bodiesClone))
            isValid = validatedata['valid']
            # print("> main.scripts._SQL_publishOrUnpublish_multiple | form:: ", form)
            # print("> main.scripts._SQL_publishOrUnpublish_multiple | exceptInvalidElement:: ", exceptInvalidElement)
            if(isValid):
                allDataIsValid = True
                if exist == True :
                    for index, body in enumerate(bodiesClone):
                        # body = deepcopy(body)
                        queryBody = deepcopy(initQueryBody(body))
                        reqSUB = deepcopy(_SQL_findOne(
                            query = queryBody,
                            _kit = { 'readModel': Table },
                        ))
                        exists = deepcopy(reqSUB['exists'])
                        isValid = False
                        if exists == True:
                            validatedata['data'][index] = cleanData(
                                oldData= reqSUB['data'],
                                newData = validatedata['data'][index],
                                nullableAttributes = nullableAttributes,
                                exists = exists,
                                lang = lang,
                            )
                            allElementForPublishOrUnpublishMultiple.append({
                                'data': validatedata['data'][index],
                                'query': _mapActionPK(reqSUB['data']),
                            })
                        else:
                            return {
                                'data': None,
                                'notif': {
                                    'type': responsesPossibles['data_doesnt_exists']['type'],
                                    'code': responsesPossibles['data_doesnt_exists']['code'],
                                    'status': responsesPossibles['data_doesnt_exists']['status'],
                                    'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                                },
                            }
                        allCheck.append(exists)
                else:
                    return {
                        'data': None,
                        'notif': {
                            'type': responsesPossibles['data_doesnt_exists']['type'],
                            'code': responsesPossibles['data_doesnt_exists']['code'],
                            'status': responsesPossibles['data_doesnt_exists']['status'],
                            'message': responsesPossibles['data_doesnt_exists']['message'][lang],
                        },
                    }
            else:
                # print("> main.scripts._SQL_publishOrUnpublish_multiple | form:: ", form)
                # print("> main.scripts._SQL_publishOrUnpublish_multiple | exceptInvalidElement:: ", exceptInvalidElement)
                allDataIsValid = False
                return {
                    'data': None,
                    'notif': {
                        'type': responsesPossibles['invalid_form']['type'],
                        'code': responsesPossibles['invalid_form']['code'],
                        'status': responsesPossibles['invalid_form']['status'],
                        'message': str(validatedata['error']),
                    },
                }

            if len(allElementForPublishOrUnpublishMultiple) > 0 :
                for indexAORM, elementAORM in enumerate(allElementForPublishOrUnpublishMultiple):
                    SQLAQF, TableF = queryFilter(
                        elementAORM['query'],
                        Table = writeModel,
                    )
                    sessionF.query(TableF).filter(SQLAQF).update(elementAORM['data'])
                    sessionF.flush()
                    cleanedDatas.append(elementAORM['data'])

            # print("> main.scripts._SQL_publishOrUnpublish_multiple | allCheck:: ", allCheck)
            # print("> main.scripts._SQL_publishOrUnpublish_multiple | allElementForArchiveOrRestoreMultiple:: ", allElementForArchiveOrRestoreMultiple)
            # print("> main.scripts._SQL_publishOrUnpublish_multiple | allDataIsValid:: ", allDataIsValid)
            

            sessionF.commit()
            sessionF.close_all()
        res = {
            'data': cleanedDatas,
            'notif': {
                'type': responsesPossibles['good_action']['type'],
                'code': responsesPossibles['good_action']['code'],
                'status': responsesPossibles['good_action']['status'],
                'message': responsesPossibles['good_action']['message'][lang],
            },
        }
        res = _supAction(datas = cleanedDatas, bodies = bodies, exist = True, lang = lang, res = res)
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'data': None,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }

def _SQL_export(
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

    elemntForFindAll = _SQL_findAll(
        query = query,
        _kit = _kit,
        progressive = progressive,
        _clean = _clean,
    )
    datas = elemntForFindAll["datas"]
    # export_type = "csv"
    # print("> pd_crud - _SQL_export | query:: ", query)
    # print("> pd_crud - _SQL_export | _kit:: ", _kit)
    # print("> pd_crud - _SQL_export | progressive:: ", progressive)
    # print("> pd_crud - _SQL_export | _clean:: ", _clean)
    # print("> pd_crud - _SQL_export | elemntForFindAll:: ", elemntForFindAll)
    # print("> pd_crud - _SQL_export | datas:: ", datas)
    # print("> pd_crud - _SQL_export | export_type:: ", export_type)

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

def _SQL_extract(
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