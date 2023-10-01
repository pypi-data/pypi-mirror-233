from socket import timeout
from typing import *
import asyncio
import logging
import traceback
import sys
import warnings
from copy import deepcopy
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import exc as sa_exc

from .hivi_init import Manager


manager = Manager()
DBCONFIG = manager.getDatabaseConfig()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
log = logging.getLogger(__name__)

# print('--> hivipy - sql | DBCONFIG:: ', DBCONFIG)
dialect = DBCONFIG['dialect']
dbtype = DBCONFIG['dbtype']
def createEngine(config: dict):
    config = deepcopy(config)

    engineStr = None
    if(config['dialect'] == 'sqlite'):
        engineStr = "sqlite:///{name}?check_same_thread=False&charset=utf8mb4".format(
            name = config["name"],
        )
    elif(config['dialect'] == 'postgres'):
        engineStr = "postgresql+pg8000://{user}:{pwd}@{host}:{port}/{dbname}".format(
            user = config["user"],
            pwd = config["password"],
            host = config["host"],
            port = config["port"],
            dbname = config["name"],
        )
    elif(config['dialect'] == 'oracle'):
        engineStr = "oracle://{user}:{pwd}@{host}:{port}/{dbname}".format(
            user = config["user"],
            pwd = config["password"],
            host = config["host"],
            port = config["port"],
            dbname = config["name"],
        )
    elif(config['dialect'] == 'mysql'):
        engineStr = "mysql+pymysql://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8mb4".format(
            user = config["user"],
            pwd = config["password"],
            host = config["host"],
            port = config["port"],
            dbname = config["name"],
        )
    elif(config['dialect'] == 'mssql'):
        engineStr = "mssql+pyodbc://{user}:{pwd}@{host}:{port}/{dbname}?charset=utf8".format(
            user = config["user"],
            pwd = config["password"],
            host = config["host"],
            port = config["port"],
            dbname = config["name"],
        )
    return create_engine(
        engineStr,
        # future=True,
        echo = False,
    ).connect()


def SQL_Action(
    sqliteAction = lambda dialect, dbType: None,
    postgresAction = lambda dialect, dbType: None,
    oracleAction = lambda dialect, dbType: None,
    mysqlAction = lambda dialect, dbType: None,
    mssqlAction = lambda dialect, dbType: None,
    elseAction = lambda dialect, dbType: None,
):
    sqliteAction = deepcopy(sqliteAction)
    postgresAction = deepcopy(postgresAction)
    oracleAction = deepcopy(oracleAction)
    mysqlAction = deepcopy(mysqlAction)
    mssqlAction = deepcopy(mssqlAction)
    elseAction = deepcopy(elseAction)

    try:
        dialect = DBCONFIG['dialect']
        dbType = DBCONFIG['dbtype']

        # print("---> hivipy - sql | SQL_Action - dialect:: ", dialect)
        
        sqliteAction = sqliteAction if callable(sqliteAction) else (lambda dialect, dbType: None)
        postgresAction = postgresAction if callable(postgresAction) else (lambda dialect, dbType: None)
        oracleAction = oracleAction if callable(oracleAction) else (lambda dialect, dbType: None)
        mysqlAction = mysqlAction if callable(mysqlAction) else (lambda dialect, dbType: None)
        mssqlAction = mssqlAction if callable(mssqlAction) else (lambda dialect, dbType: None)
        elseAction = elseAction if callable(elseAction) else (lambda dialect, dbType: None)

        if(dialect == 'sqlite'):
            return sqliteAction(dialect=dialect, dbType=dbType)
        elif(dialect == 'postgres'):
            return postgresAction(dialect=dialect, dbType=dbType)
        elif(dialect == 'oracle'):
            return oracleAction(dialect=dialect, dbType=dbType)
        elif(dialect == 'mysql'):
            return mysqlAction(dialect=dialect, dbType=dbType)
        elif(dialect == 'mssql'):
            return mssqlAction(dialect=dialect, dbType=dbType)
        return mssqlAction(dialect=dialect, dbType=dbType)
    except Exception as err:
        code = str(type(err))
        msg = str(err)
        stack = str(traceback.format_exc())
        trace = sys.exc_info()[2]
        
        if DEBUG == True:
            log.error(stack)

        return None

engine = createEngine(DBCONFIG) if dbtype == 'sql' else None
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine, metadata=metadata)
client = automap_base()
SessionMaker = sessionmaker(
    bind = engine,
    expire_on_commit=False,
)
session = SessionMaker()
# session = Session(engine, expire_on_commit=False)
# session.close_all()


warnings.filterwarnings('ignore', category=sa_exc.SAWarning)
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=sa_exc.SAWarning)