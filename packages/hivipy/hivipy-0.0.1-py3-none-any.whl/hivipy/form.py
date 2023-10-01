from typing import *
import asyncio
import logging
import traceback
import sys
import re
import json
from copy import deepcopy
from werkzeug.local import LocalProxy
from .objects import mergeObjects
from .utils import getLang
from .config import pagesPossibles, responsesPossibles
from .hivi_init import Manager

manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)

def getRequestBody(request: LocalProxy):
    try:
        finalBody = {}
        body = None
        contentType = request.headers.get('Content-Type')
        # if contentType == 'application/json':
        if contentType is not None and 'multipart/form-data' in contentType:
            body = dict(request.form)
            # if DEBUG :
            # print("--> getRequestBody - body:: ", body)
        
            # print("--> getRequestBody - request.form:: ", request.form)
            # print("--> getRequestBody - type(request.form):: ", type(request.form))
        else:
            body = dict(request.get_json(force=True))
            arrayElements = {}
            if type(body) == dict:
                newBody = {}
                for index, (key, value) in enumerate(body.items()):
                    checkArray = re.search(r'(\w{1,})\[\d{0,}\]', key)
                    if checkArray:
                        cleanedKey = checkArray.groups()[0]
                        if (
                            cleanedKey in arrayElements.keys() and
                            type(arrayElements[cleanedKey]) in (list, tuple)
                        ):
                            arrayElements[cleanedKey].append(value)
                        else:
                            arrayElements[cleanedKey] = [value]
                    else:
                        newBody[key] = deepcopy(value) if type(value) in (str, int, float, bool) else value
                newBody = {
                    **newBody,
                    **arrayElements,
                }
                body = newBody
        # if DEBUG :
            # print("--> getRequestBody - body - final:: ", body)
        files = dict(request.files)
        # if DEBUG :
            # print("--> getRequestBody - files - final:: ", files)
        if 'covers[primary]' in files.keys():
            pass
            # if DEBUG :
                # print("--> getRequestBody - type(files['covers[primary]']) - final:: ", type(files['covers[primary]']))

        finalBody = mergeObjects(body, files)
        # if DEBUG :
            # print("--> getRequestBody - finalBody - final:: ", finalBody)

        return finalBody
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None

def getRequestBodies(request: LocalProxy):
    try:
        finalBody = []
        body = None
        contentType = request.headers.get('Content-Type')
        body = request.get_json(force=True)
        body = list(body) if type(body) in (list, tuple) else []

        finalBody = body

        return finalBody
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None