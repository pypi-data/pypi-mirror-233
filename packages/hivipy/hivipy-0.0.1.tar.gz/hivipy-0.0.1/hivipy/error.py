from typing import *
import asyncio
import logging
import traceback
import sys
# from django.conf import settings
from .hivi_init import Manager

from .utils import getLang
from .config import pagesPossibles, responsesPossibles

manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)


def getErrorResponse(typeResp: str = 'unknown_error', lang: str = 'fr'):
    lang = getLang(lang)
    if typeResp in responsesPossibles.keys():
        res = responsesPossibles[typeResp]
        return {
            'datas': None,
            'meta': {
                'pagination': {
                    'page': 1,
                    'pageSize': pagesPossibles[0],
                    'pageCount': 1,
                    'pageLength': 0,
                    'total': 0,
                },
            },
            'data': None,
            'exists': False,
            'notif': {
                "code": res['code'],
                "message": res['message'][lang],
                "status": res['status'],
                "type": res['type'],
            }
        }, res['status']
    return {
        'datas': None,
        'meta': {
            'pagination': {
                'page': 1,
                'pageSize': pagesPossibles[0],
                'pageCount': 1,
                'pageLength': 0,
                'total': 0,
            },
        },
        'data': None,
        'exists': False,
        'notif': {
            "code": responsesPossibles['unknown_error']['code'],
            "message": responsesPossibles['unknown_error']['message'][lang],
            "status": responsesPossibles['unknown_error']['status'],
            "type": responsesPossibles['unknown_error']['type'],
        }
    }, responsesPossibles['unknown_error']['status']

def ifInvalidUnknownErrorSync(lang, src, initialAttr = 'data'):
    initialAttr = initialAttr if type(initialAttr) == str else 'data'
    lang = getLang(lang)
    try:
        if callable(src):
            res = src()
        else:
            res = src
        if type(res) == dict:
            return res
        else:
            # return {
            #     initialAttr: res
            # }
            return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
async def ifInvalidUnknownError(lang, src, initialAttr = 'data'):
    initialAttr = initialAttr if type(initialAttr) == str else 'data'
    lang = getLang(lang)
    try:
        if callable(src):
            res = await src()
        else:
            res = src
        if type(res) == dict:
            return res
        else:
            # return {
            #     initialAttr: res
            # }
            return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
async def ifInvalidUnknownErrorForExport(lang, src):
    lang = getLang(lang)
    try:
        if callable(src):
            res = await src()
        else:
            res = src
        return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return {
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message' : {
                    'fr': 'Echec lors de l\'exportation du file',
                    'en': 'Failed to export file',
                }[lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
async def ifInvalidUnknownErrorForFindAll(lang, src, initialAttr = 'datas'):
    initialAttr = initialAttr if type(initialAttr) == str else 'datas'
    lang = getLang(lang)
    try:
        if callable(src):
            res = await src()
        else:
            res = src
        if type(res) == dict:
            return res
        else:
            # return {
            #     initialAttr: res
            # }
            return res
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
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
async def ifInvalidUnknownErrorForFindOne(lang, src, initialAttr = 'data'):
    initialAttr = initialAttr if type(initialAttr) == str else 'data'
    lang = getLang(lang)
    try:
        if callable(src):
            res = await src()
        else:
            res = src
        if type(res) == dict:
            return res
        else:
            # return {
            #     initialAttr: res
            # }
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
            'exists': False,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }
async def ifInvalidUnknownErrorForExists(lang, src, initialAttr = 'exists'):
    initialAttr = initialAttr if type(initialAttr) == str else 'exists'
    lang = getLang(lang)
    try:
        if callable(src):
            res = await src()
        else:
            res = src
        if type(res) == dict:
            return res
        else:
            # return {
            #     initialAttr: res
            # }
            return res
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        log.error(stack)

        return {
            'exists': False,
            'notif': {
                'type': responsesPossibles['unknown_error']['type'],
                'code': responsesPossibles['unknown_error']['code'],
                'status': responsesPossibles['unknown_error']['status'],
                'message': responsesPossibles['unknown_error']['message'][lang],
                'stack': stack if DEBUG else None,
                # 'trace': sys.exc_info()[2],
            },
        }