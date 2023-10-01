from typing import *
import asyncio
import logging
import traceback
import sys
import copy

from .hivi_init import Manager
from .sql import engine as SQLEngine, client as SQLClient
from .nosql import engine as NoSQLEngine, client as NoSQLClient

manager = Manager()
DBCONFIG = manager.getDatabaseConfig()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)

def NoSql_SQL_MemoryDBAction(
    sqlAction = lambda dialect, dbType: None,
    noSqlAction = lambda dialect, dbType: None,
    memoryDBAction = lambda dialect, dbType: None,
    returnException: bool = True,
) -> any:
    returnException = copy.deepcopy(returnException) if type(returnException) == bool else True
    try:
        dialect = DBCONFIG['dialect']
        dbType = DBCONFIG['dbtype']
        sqlAction = sqlAction if callable(sqlAction) else (lambda dialect, dbType: None)
        noSqlAction = noSqlAction if callable(noSqlAction) else (lambda dialect, dbType: None)
        memoryDBAction = memoryDBAction if callable(memoryDBAction) else (lambda dialect, dbType: None)

        if dbType == 'sql' :
            return sqlAction(dialect=dialect, dbType=dbType)
        elif dbType == 'nosql' :
            return noSqlAction(dialect=dialect, dbType=dbType)
        elif dbType == 'memorydb' :
            return memoryDBAction(dialect=dialect, dbType=dbType)
        return None
    except Exception as err:
        if returnException == True:
            raise err
        else:
            code = str(type(err))
            msg = str(err)
            stack = str(traceback.format_exc())
            trace = sys.exc_info()[2]
            
            if DEBUG == True:
                log.error(stack)

            return None

engine = NoSql_SQL_MemoryDBAction(
    sqlAction = lambda dialect, dbType: SQLEngine,
    noSqlAction = lambda dialect, dbType: NoSQLEngine,
    memoryDBAction = lambda dialect, dbType: None,
)
client = NoSql_SQL_MemoryDBAction(
    sqlAction = lambda dialect, dbType: SQLClient,
    noSqlAction = lambda dialect, dbType: NoSQLClient,
    memoryDBAction = lambda dialect, dbType: None,
)
dialect = DBCONFIG['dialect']
dbType = DBCONFIG['dbtype']