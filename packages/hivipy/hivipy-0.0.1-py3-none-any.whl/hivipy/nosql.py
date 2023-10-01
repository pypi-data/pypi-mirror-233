from socket import timeout
from typing import *
import asyncio
import logging
import traceback
import sys
from copy import deepcopy
from pymongo import MongoClient

from .hivi_init import Manager


manager = Manager()
DBCONFIG = manager.getDatabaseConfig()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)

def createEngine(config: dict):
    config = deepcopy(config)

    engineStr = None
    authDatas = tuple(
        filter(
            lambda data: (type(data) == str and len(data) > 0) or type(data) == int,
            (config["user"], config["password"])
        )
    )
    authStr = ':'.join(authDatas) + '@' if (
        type(authDatas) in (list, tuple)
        and len(authDatas) == 2
    ) else ''
    hostDatas = tuple(
        filter(
            lambda data: (type(data) == str and len(data) > 0) or type(data) == int,
            (config["host"], str(config["port"]))
        )
    )
    hostStr = ':'.join(hostDatas) if (
        type(hostDatas) in (list, tuple)
        and len(hostDatas) == 2
    ) else ''
    if(config['dialect'] == 'mongodb'):
        engineStr = "mongodb://{authStr}{hostStr}/".format(
            authStr = authStr,
            hostStr = hostStr,
            db = config["name"],
        )
        # if DEBUG :
            # print("> hvscript - nosql | createEngine - engineStr:: ", engineStr)
        client = MongoClient(engineStr)
        return client[config["name"]]


def NOSQL_Action(
    mongodbAction = lambda dialect, dbType: None,
    elseAction = lambda dialect, dbType: None,
):
    config = deepcopy(config)
    elseAction = deepcopy(elseAction)

    try:
        dialect = DBCONFIG['dialect']
        dbType = DBCONFIG['dbtype']

        # if DEBUG :
            # print("---> hivipy - nosql | NOSQL_Action - dialect:: ", dialect)
        
        mongodbAction = mongodbAction if callable(mongodbAction) else (lambda dialect, dbType: None)
        elseAction = elseAction if callable(elseAction) else (lambda dialect, dbType: None)

        if(dialect == 'mongodb'):
            return mongodbAction(dialect=dialect, dbType=dbType)
        return elseAction(dialect=dialect, dbType=dbType)
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None

engine = createEngine(config=DBCONFIG)
client = engine