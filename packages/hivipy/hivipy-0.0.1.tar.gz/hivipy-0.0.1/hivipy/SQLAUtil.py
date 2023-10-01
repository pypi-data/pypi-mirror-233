from copy import deepcopy, copy
from typing import *
from functools import reduce
import re
import math
import json
import traceback
import sys
from logging import Logger
import logging
import sqlalchemy as SQLAType
from sqlalchemy.dialects.postgresql import array as PGarray, ARRAY as PGARRAY
from sqlalchemy import MetaData, Column, String, Table, JSON, ARRAY, and_, or_, not_, asc, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql, mysql
from sqlalchemy.sql.expression import cast, func
from sqlalchemy.orm import aliased
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.automap import automap_base
from sqlalchemy_utils import create_view
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .hivi_init import Manager
from .config import pagesPossibles
from .sql import DBCONFIG, SQL_Action, engine, dialect
from .string import RandomStr


manager = Manager()
structConf = manager.getStructConfig()
# print('--> structConf:: ', structConf)
DEBUG = structConf['debug']
log = logging.getLogger(__name__)


def createSQLView(Base: declarative_base, stmt, viewName: str):
    # Base = deepcopy(Base)
    # stmt = deepcopy(stmt)
    viewName = deepcopy(viewName)

    dropSQLView(viewName=viewName)
    view: DeclarativeMeta = create_view(viewName, stmt, metadata=Base.metadata)
    class VIEW(Base):
        __table__ = view

    return VIEW, Base
def dropSQLView(viewName: str):
    viewName = deepcopy(viewName)

    reqDelete  = 'DROP VIEW IF EXISTS {tablename} CASCADE'.format(
        tablename = deepcopy(viewName),
    ) if dialect != 'sqlite' else 'DROP VIEW IF EXISTS {tablename}'.format(
        tablename = deepcopy(viewName),
    )
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(reqDelete)

def str_findAttributeInObject(target, attributname: str):
    target = deepcopy(target)
    attributname = deepcopy(attributname)

    target = deepcopy(target)
    attributname = deepcopy(attributname)
    if DBCONFIG['dialect'] == 'postgres':
        return """{target}->>'{attributname}'""".format(
            target = target,
            attributname = attributname,
        )
    elif DBCONFIG['dialect'] == 'mysql':
        return """JSON_UNQUOTE(JSON_EXTRACT({target},'$.{attributname}'))""".format(
            target = target,
            attributname = attributname,
        )
    elif DBCONFIG['dialect'] == 'sqlite':
        return """JSON_EXTRACT({target}, '$.{attributname}')""".format(
            target = target,
            attributname = attributname,
        )
    return """{target}->>'{attributname}'""".format(
        target = target,
        attributname = attributname,
    )
def strDropSQLView(viewName: str):
    viewName = deepcopy(viewName)

    reqDelete  = 'DROP VIEW IF EXISTS {tablename} CASCADE;'.format(
        tablename = deepcopy(viewName),
    )
    return reqDelete
def strReqWhere(*conds: list, condType: str = 'and', addWhereLabel: bool = False):
    conds = deepcopy(conds)
    condType = deepcopy(condType)
    addWhereLabel = deepcopy(addWhereLabel)

    addWhereLabel = deepcopy(addWhereLabel) if type(addWhereLabel) == bool else False
    condType = deepcopy(condType) if condType in ('or', 'and') else 'and'
    conds = deepcopy(conds) if type(conds) in (tuple, list) else []
    conds = list(
        filter(
            lambda cond: type(cond) == str and len(cond) > 0,
            conds,
        )
    )

    if len(conds) > 0:
        res = (' ' + condType.upper() + ' ').join(conds)
        if addWhereLabel == True:
            res = 'WHERE (' + res + ')'
        return res
    else:
        return ''
#
def strReqOrWhere(*conds: list):
    conds = deepcopy(conds)

    return strReqWhere(conds = deepcopy(conds), condType='or')
def strReqAndWhere(*conds: list):
    conds = deepcopy(conds)

    return strReqWhere(conds = deepcopy(conds), condType='and')
def strReqOrderBy(*datas):
    datas = deepcopy(datas)

    datas = deepcopy(datas) if type(datas) in (list, tuple) else []
    datas = list(
        filter(
            lambda data: (
                (
                    type(data) == dict and
                    'attribut' in data.keys() and
                    type(data['attribut']) == str and
                    len(data['attribut']) > 0 and
                    'order' in data.keys() and
                    data['order'] in ('asc', 'desc')
                ) or data == 'random'
            ),
            datas
        )
    )

    if len(datas) > 0:
        return 'ORDER BY ' + ', '.join(list(
            map(
                lambda data: 'random()' if data == 'random' else (data['attribut'] + ' ' + data['order']),
                datas,
            )
        ))
    else:
        return ''
#
def strReqCase(*datas, elseData: dict):
    datas = deepcopy(datas)
    elseData = deepcopy(elseData)

    datas = deepcopy(datas) if type(datas) in (list, tuple) else []
    datas = list(
        filter(
            lambda data: (
                type(data) == dict and
                'cond' in data.keys() and
                type(data['cond']) == str and
                len(data['cond']) > 0 and
                'return' in data.keys() and
                type(data['return']) == str and
                len(data['return']) > 0
            ),
            datas,
        )
    )
    elseData = deepcopy(elseData) if (
        len(datas) > 0 and
        type(elseData) == dict and
        'cond' in elseData.keys() and
        type(elseData['cond']) == str and
        len(elseData['cond']) > 0 and
        'return' in elseData.keys() and
        type(elseData['return']) == str and
        len(elseData['return']) > 0
    ) else None

    if len(datas) > 0:
        subReq = ' '.join(
            ['WHEN' + ' ' + '(' + (data['cond'] + ')' + ' ' + 'THEN' + ' ' + data['return']) for data in datas]
        )
        if elseData is not None:
            subReq  = subReq + ' ' + (
                'ELSE' + ' ' + '(' + (elseData['cond'] + ')' + ' ' + 'THEN' + ' ' + elseData['return'])
            )
        res = '(' + ' ' + 'CASE' + ' ' + subReq + ' ' + 'END' + ')'

        return res
    return ''

def strReqLimit(limit: int, offset: int = None):
    limit = deepcopy(limit)
    offset = deepcopy(offset)

    limit = deepcopy(limit) if type(limit) in (int, float) else None
    offset = deepcopy(offset) if type(offset) in (int, float) else None

    if limit is not None:
        reqLimit = 'LIMIT ' + limit
        if offset is not None:
            reqLimit = reqLimit + ' ' + 'OFFSET ' + offset
        return ''
    else:
        return ''

def strReqInnerJoin(
    table1: str,
    alias1: str,
    attribut1: str,
    table2: str,
    alias2: str,
    attribut2: str,
    labelJoin: str = 'INNER JOIN',
    aliased1: bool = True,
    aliased2: bool = True,
):
    aliased1 = deepcopy(aliased1) if type(aliased1) == bool else True
    aliased2 = deepcopy(aliased2) if type(aliased2) == bool else True
    labelJoin = deepcopy(labelJoin) if type(labelJoin) == str and len(labelJoin) > 0 else 'INNER JOIN'
    table1 = deepcopy(table1) if type(table1) == str and len(table1) > 0 else None
    alias1 = deepcopy(alias1) if type(alias1) == str and len(alias1) > 0 else None
    attribut1 = deepcopy(attribut1) if type(attribut1) == str and len(attribut1) > 0 else None
    table2 = deepcopy(table2) if type(table2) == str and len(table2) > 0 else None
    alias2 = deepcopy(alias2) if type(alias2) == str and len(alias2) > 0 else None
    attribut2 = deepcopy(attribut2) if type(attribut2) == str and len(attribut2) > 0 else None

    if (
        table1 is not None and
        alias1 is not None and
        attribut1 is not None and
        table2 is not None and
        alias2 is not None and
        attribut2 is not None
    ):
        subReq1 = '{alias1}.{attribut1}'.format(
            alias1 = alias1,
            attribut1 = attribut1,
        ) if aliased1 == True else '{attribut1}'.format(
            attribut1 = attribut1,
        )
        subReq2 = '{alias2}.{attribut2}'.format(
            alias2 = alias2,
            attribut2 = attribut2,
        ) if aliased2 == True else '{attribut2}'.format(
            attribut2 = attribut2,
        )
        return '{labelJoin} {table1} {alias1} ON {subReq1} = {subReq2}'.format(
            labelJoin = labelJoin,
            table1 = table1,
            alias1 = alias1,
            subReq1 = subReq1,
            subReq2 = subReq2,
        )
    else :
        return None
def sqlReqMultipleForm(
    default = None,
    mysql = None,
    sqlite = None,
    postgres = None,
    defaultMap = lambda data: data,
):
    default = deepcopy(default)
    mysql = deepcopy(mysql)
    sqlite = deepcopy(sqlite)
    postgres = deepcopy(postgres)
    defaultMap = deepcopy(defaultMap)

    mapF = defaultMap

    subReq: str = None
    default = default if default is not None and callable(default) else None
    if default is not None:
        subReq = default
    elif DBCONFIG['dialect'] == 'postgres' and postgres is not None:
        postgres = postgres if postgres is not None and callable(postgres) else mapF
        subReq = postgres
    elif DBCONFIG['dialect'] == 'mysql' and mysql is not None:
        mysql = mysql if mysql is not None and callable(mysql) else mapF
        subReq = postgres
    elif DBCONFIG['dialect'] == 'sqlite' and sqlite is not None:
        sqlite = sqlite if sqlite is not None and callable(sqlite) else mapF
        subReq = sqlite

    return subReq
def sqlGetAttributWithAlias(
    tableOrAliasname: str,
    columns: dict,
):
    tableOrAliasname = deepcopy(tableOrAliasname)
    columns = deepcopy(columns)

    tableOrAliasname = tableOrAliasname if type(tableOrAliasname) == str and len(tableOrAliasname) > 0 else None
    columns = columns if type(columns) == dict else {}
    res = {}
    for index, key in enumerate(columns):
        res[key] = tableOrAliasname + '.' + columns[key]
    
    return res
def sqlViewReqMultipleForm(
    tablename: str,
    columns: dict,
    alias = None,
    hasColumnsAlias: bool = True,
    isView: bool = True,
    viewname: str = None,
    default = None,
    mysql = None,
    sqlite = None,
    postgres = None,
):
    columns = deepcopy(columns)
    tablename = deepcopy(tablename)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)
    viewname = deepcopy(viewname)
    default = deepcopy(default)
    mysql = deepcopy(mysql)
    sqlite = deepcopy(sqlite)
    postgres = deepcopy(postgres)

    tablename = deepcopy(tablename) if type(tablename) == str and len(tablename) > 0 else ''
    columns = deepcopy(columns) if type(columns) == dict else {}
    alias = deepcopy(alias) if type(alias) == str and len(alias) else None
    hasColumnsAlias =  deepcopy(hasColumnsAlias) if type(hasColumnsAlias) == bool else True
    columnsF = {}
    for key, column in columns.items():
        if(hasColumnsAlias == True and alias is not None):
            columnsF[key] = alias + '.' + deepcopy(columns[key])
        else:
            columnsF[key] = deepcopy(columns[key])
        if(hasColumnsAlias == True and column != key):
            columnsF[key] = columnsF[key] + ' AS ' + key
        else:
            columnsF[key] = columnsF[key]
    columnsArr = [ value for key, value in columnsF.items() ]
    columnsAndKey = list(
        reduce(
            lambda x, y: x+y,
            [ [key, value] for key, value in columnsF.items() ]
        )
    )
    tablenameF = deepcopy(tablename) + " " + alias if alias is not None else deepcopy(tablename)
    str_columnsArr = ', '.join(columnsArr)
    viewname = viewname if type(viewname) == str and len(viewname) > 0 else 'view_' + deepcopy(tablenameF)
    
    mapF = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: 'SELECT {strcolumn} FROM {tablename}'.format(
        strcolumn = str_columnsArr,
        tablename = tablenameF,
    )

    subReq = sqlReqMultipleForm(
        default=default,
        postgres=postgres,
        mysql=mysql,
        sqlite=sqlite,
        defaultMap=mapF,
    )
        
    if subReq is not None:
        FSebReq = subReq(
            tablename = tablename,
            alias = alias,
            tablenameF = tablenameF,
            columns = columns,
            columnsF = columnsF,
            columnsArr = columnsArr,
            columnsAndKey = columnsAndKey,
            str_columnsArr = str_columnsArr,
        )
        return 'CREATE VIEW {view} AS {req}'.format(
            view = viewname,
            req = FSebReq,
        ) if isView == True else FSebReq
    else:
        return None
# --->
def getReqSelectWithSqlViewReqMultipleForm(
    tablename: str,
    viewname: str,
    columns: dict,
    alias = None,
    other = (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: ''),
    hasColumnsAlias: bool = True,
    isView: bool = True,
):
    tablename = deepcopy(tablename)
    viewname = deepcopy(viewname)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    other = deepcopy(other)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)

    hasColumnsAlias = deepcopy(hasColumnsAlias) if type(hasColumnsAlias) == bool else True
    isView = deepcopy(isView) if type(isView) == bool else True
    other = deepcopy(other) if callable(other) else (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: '')

    return sqlViewReqMultipleForm(
        viewname = viewname,
        tablename = tablename,
        columns = columns,
        alias = alias,
        hasColumnsAlias=hasColumnsAlias,
        isView=isView,
        mysql = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'SELECT {strcolumn} FROM {tablename} {other}'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        sqlite = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'SELECT {strcolumn} FROM {tablename} {other}'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        postgres = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'SELECT {strcolumn} FROM {tablename} {other}'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                alias = alias,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
    )
def getReqSelectArrayObjectWithSqlViewReqMultipleForm(
    tablename: str,
    columns: dict,
    alias = None,
    other = (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: ''),
    hasColumnsAlias: bool = False,
    isView: bool = False,
):
    tablename = deepcopy(tablename)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    other = deepcopy(other)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)

    hasColumnsAlias = deepcopy(hasColumnsAlias) if type(hasColumnsAlias) == bool else False
    isView = deepcopy(isView) if type(isView) == bool else False
    other = deepcopy(other) if callable(other) else (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: '')

    return sqlViewReqMultipleForm(
        tablename = tablename,
        columns = columns,
        alias = alias,
        hasColumnsAlias=hasColumnsAlias,
        isView=isView,
        mysql = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT json_group_array(JSON_OBJECT({strcolumn})) FROM {tablename} {other} )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        sqlite = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT json_arrayagg(JSON_OBJECT({strcolumn})) FROM {tablename} {other} )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        postgres = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( ARRAY( SELECT JSON_BUILD_OBJECT({strcolumn}) FROM {tablename} {other} ) )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                alias = alias,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
    )
def getReqSelectArrayWithSqlViewReqMultipleForm(
    tablename: str,
    columns: dict,
    alias = None,
    other = (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: ''),
    hasColumnsAlias: bool = False,
    isView: bool = False,
):
    tablename = deepcopy(tablename)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    other = deepcopy(other)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)

    hasColumnsAlias = deepcopy(hasColumnsAlias) if type(hasColumnsAlias) == bool else False
    isView = deepcopy(isView) if type(isView) == bool else False
    other = deepcopy(other) if callable(other) else (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: '')

    return sqlViewReqMultipleForm(
        tablename = tablename,
        columns = columns,
        alias = alias,
        hasColumnsAlias=hasColumnsAlias,
        isView=isView,
        mysql = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT json_group_array({strcolumn}) FROM {tablename} {other} )'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        sqlite = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT json_arrayagg({strcolumn}) FROM {tablename} {other} )'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        postgres = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( ARRAY( SELECT {strcolumn} FROM {tablename} {other} ) )'.format(
                strcolumn = str_columnsArr,
                tablename = tablenameF,
                alias = alias,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
    )
def getReqSelectObjectWithSqlViewReqMultipleForm(
    tablename: str,
    columns: dict,
    alias = None,
    other = (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: ''),
    hasColumnsAlias: bool = False,
    isView: bool = False,
):
    tablename = deepcopy(tablename)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    other = deepcopy(other)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)

    hasColumnsAlias = deepcopy(hasColumnsAlias) if type(hasColumnsAlias) == bool else False
    isView = deepcopy(isView) if type(isView) == bool else False
    other = deepcopy(other) if callable(other) else (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: '')

    return sqlViewReqMultipleForm(
        tablename = tablename,
        columns = columns,
        alias = alias,
        hasColumnsAlias=hasColumnsAlias,
        isView=isView,
        mysql = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT JSON_OBJECT({strcolumn}) FROM {tablename} {other} LIMIT 1 )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        sqlite = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT JSON_OBJECT({strcolumn}) FROM {tablename} {other} LIMIT 1 )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        postgres = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            '( SELECT JSON_BUILD_OBJECT({strcolumn}) FROM {tablename} {other} LIMIT 1 )'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                alias = alias,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
    )
def getReqObjectWithSqlViewReqMultipleForm(
    tablename: str,
    columns: dict,
    alias = None,
    other = (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: ''),
    hasColumnsAlias: bool = False,
    isView: bool = False,
):
    tablename = deepcopy(tablename)
    columns = deepcopy(columns)
    alias = deepcopy(alias)
    other = deepcopy(other)
    hasColumnsAlias = deepcopy(hasColumnsAlias)
    isView = deepcopy(isView)

    hasColumnsAlias = hasColumnsAlias if type(hasColumnsAlias) == bool else False
    isView = isView if type(isView) == bool else False
    other = other if callable(other) else (lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: '')

    return sqlViewReqMultipleForm(
        tablename = tablename,
        columns = columns,
        alias = alias,
        hasColumnsAlias=hasColumnsAlias,
        isView=isView,
        mysql = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'JSON_OBJECT({strcolumn}) {other}'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        sqlite = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'JSON_OBJECT({strcolumn}) {other}'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
        postgres = lambda tablename, alias, tablenameF, columns, columnsF, columnsArr, columnsAndKey, str_columnsArr: (
            'JSON_BUILD_OBJECT({strcolumn}) {other}'.format(
                strcolumn = ', '.join(["'" + value + "'" if index % 2 == 0 else value for index, value in enumerate(columnsAndKey)]),
                tablename = tablenameF,
                alias = alias,
                other = other(
                    tablename = tablename,
                    alias = alias,
                    tablenameF = tablenameF,
                    columns = columns,
                    columnsF = columnsF,
                    columnsArr = columnsArr,
                    columnsAndKey = columnsAndKey,
                    str_columnsArr = str_columnsArr,
                ),
            )
        ),
    )
# --->
def strReqGetIntervalTime(
    duration: str,
    typeRes: str,
):
    duration = deepcopy(duration)
    typeRes = deepcopy(typeRes)

    duration =  str(deepcopy(duration)) if type(duration) in (int, float, str) else None
    typeRes =  deepcopy(typeRes) if type(typeRes) in ( 'second', 'minute', 'hour', 'day', 'month', 'year' ) else 'second'

    if duration is not None and typeRes is not None:
        defaultMap = (lambda duration, typeRes : '' )
        def mysqlMap(duration: float, typeRes: str):
            defaultDate = "STR_TO_DATE('01-01-0001 00:00:00', '%d-%m-%Y %H:%i:%s')"
            return """TIMESTAMPDIFF( {type}, {defaultDate}, {defaultDate} + INTERVAL {duration} {type} )""".format(
                type = typeRes,
                defaultDate = defaultDate,
                duration = duration,
            )
        def sqliteMap(duration: float, typeRes: str):
            return """( (datetime('0001-01-01', '+' || {duration} || ' ' || {type})) - datetime('0001-01-01') )""".format(
                type = typeRes,
                duration = duration,
            )
        def postgresMap(duration: float, typeRes: str):
            return """( CONCAT({duration}, ' ', {type})::INTERVAL )""".format(
                type = typeRes,
                duration = duration,
            )
        res = sqlReqMultipleForm(
            mysql= mysqlMap,
            sqlite= sqliteMap,
            postgres= postgresMap,
            defaultMap=defaultMap,
        )

        return res(duration = duration, typeRes = typeRes)
    else:
        return ''
def strReqTimeIsOver(
    thedate1: str,
    thedate2: str,
    duration: str,
    typeRes: str,
):
    thedate1 = deepcopy(thedate1)
    thedate2 = deepcopy(thedate2)
    duration = deepcopy(duration)
    typeRes = deepcopy(typeRes)

    thedate1 =  str(deepcopy(thedate1)) if type(thedate1) == str else None
    thedate2 =  str(deepcopy(thedate2)) if type(thedate2) == str else None
    duration =  str(deepcopy(duration)) if type(duration) in (int, float, str) else None
    typeRes =  deepcopy(typeRes) if type(typeRes) in ( 'second', 'minute', 'hour', 'day', 'month', 'year' ) else 'second'


    if duration is not None and typeRes is not None:
        defaultMap = (lambda duration, typeRes : '' )
        def mysqlMap(thedate1: str, thedate2: str, duration: float, typeRes: str):
            res1 = "( {thedate2} + INTERVAL {duration} {type} )".format(
                type = typeRes,
                duration = duration,
                thedate2 = thedate2,
            )
            res = "( {sub1} >= {thedate1} )".format(
                thedate1 = thedate1,
                sub1 = res1,
            )
            return res
        def sqliteMap(thedate1: str, thedate2: str, duration: float, typeRes: str):
            res = "( (datetime({thedate2}, '+' || {duration} || ' ' || {type}) > {thedate1}) AND ({thedate2} IS NOT NULL AND {thedate1} IS NOT NULL) )".format(
                type = typeRes,
                duration = duration,
                thedate1 = thedate1,
                thedate2 = thedate2,
            )
            return res
        def postgresMap(thedate1: str, thedate2: str, duration: float, typeRes: str):
            if thedate1 is None:
                thedate2 = thedate1
            elif thedate2 is None:
                thedate1 = thedate2
            strIntervale = strReqGetIntervalTime(duration=duration, typeRes=typeRes)
            res1 = """CONCAT( extract( epoch from ( {thedate1} - {thedate2} ) ), ' {type}' )::INTERVAL""".format(
                type = typeRes,
                thedate1 = thedate1,
                thedate2 = thedate2,
            )
            res = """( ( {sub1} > {interval} AND {sub1} >= CONCAT(0, ' {type}')::INTERVAL ) OR {sub1} = CONCAT(0, ' {type}')::INTERVAL )::BOOLEAN""".format(
                type = typeRes,
                interval = strIntervale,
                sub1 = res1,
            )
            return res
        res = sqlReqMultipleForm(
            mysql= mysqlMap,
            sqlite= sqliteMap,
            postgres= postgresMap,
            defaultMap=defaultMap,
        )

        return res(thedate1 = thedate1, thedate2 = thedate2, duration = duration, typeRes = typeRes)
    else:
        return ''
def strReqTimeIsOverUseDatenow(
    thedate2: str,
    duration: str,
    typeRes: str,
):
    thedate2 = deepcopy(thedate2)
    duration = deepcopy(duration)
    typeRes = deepcopy(typeRes)

    thedate1: str = 'CURRENT_TIMESTAMP'
    return strReqTimeIsOver(
        thedate1 = thedate1,
        thedate2 = thedate2,
        duration = duration,
        typeRes = typeRes,
    )

def getSQLValue(data: any):
    # data = data

    if data is not None:
        res = json.dumps(deepcopy(data))
        return res
    return 'null'



def mapF__getSQLObjectForSubquery(data, table, dialect, isArray):
    # data = data
    table = deepcopy(table)
    dialect = deepcopy(dialect)
    isArray = deepcopy(isArray)

    pass
def findAttributeInObject(
    target,
    attributName: str
):
    target = deepcopy(target)
    attributName = deepcopy(attributName)

    if DBCONFIG['dialect'] == 'postgres':
        return target.op('->>')(attributName)
    elif DBCONFIG['dialect'] == 'mysql':
        return SQLAType.func.json_unquote(SQLAType.func.json_extract(target, '$.' + attributName))
    elif DBCONFIG['dialect'] == 'sqlite':
        return SQLAType.func.json_extract(target, '$.' + attributName)
    return SQLAType.func.json_unquote(SQLAType.func.json_extract(target, '$.' + attributName))

toArray = SQL_Action(
    sqliteAction = lambda dialect, dbType: SQLAType.func.json_group_array,
    postgresAction = lambda dialect, dbType: func.array_agg,
    oracleAction = lambda dialect, dbType: None,
    mysqlAction = lambda dialect, dbType: SQLAType.func.array_agg,
    mssqlAction = lambda dialect, dbType: None,
    elseAction = lambda dialect, dbType: SQLAType.func.json_arrayagg,
)
toObject = SQL_Action(
    sqliteAction = lambda dialect, dbType: SQLAType.func.json_object,
    postgresAction = lambda dialect, dbType: SQLAType.func.json_build_object,
    oracleAction = lambda dialect, dbType: None,
    mysqlAction = lambda dialect, dbType: SQLAType.func.json_object,
    mssqlAction = lambda dialect, dbType: None,
    elseAction = lambda dialect, dbType: SQLAType.func.json_object,
)
def getSQLObjectForSubquery(
    columnsAndKey: list,
    table, label: str,
    isArray = True,
    mapF = lambda data, table, dialect, isArray: SQLAType.select(data).select_from(table),
):
    # columnsAndKey = deepcopy(columnsAndKey)
    # table = deepcopy(table)
    # label = deepcopy(label)
    isArray = deepcopy(isArray)
    mapF = deepcopy(mapF)

    mapF = mapF if callable(mapF) else (lambda data, table: SQLAType.select(data).select_from(table))
    label = label if (
        type(label) == str and
        len(label) > 0
    ) else RandomStr(lengthStr=5, mapF=lambda data: "column{0}".format(data))
    isArray = isArray if type(isArray) == bool else True
    """tableF = aliased(
        table,
        name = RandomStr(
            lengthStr=5,
            mapF=lambda data: "sub{0}".format(data)
        )
    )"""
    tableF = table
    """if isArray == True:
        tableF = aliased(
            table,
            name = RandomStr(
                lengthStr=5,
                mapF=lambda data: "sub{0}".format(data)
            )
        )"""
    
    
    return SQL_Action(
        sqliteAction = lambda dialect, dbType: (
            mapF(
                data = (toArray(
                    toObject(*columnsAndKey)
                ) if isArray == True else toObject(*columnsAndKey)).label(label),
                table = tableF,
                dialect = dialect,
                isArray=isArray
            )
        ),
        postgresAction = lambda dialect, dbType: (
            mapF(
                data = (toArray(
                    toObject(*columnsAndKey),
                ) if isArray == True else toObject(*columnsAndKey)).label(label),
                table = tableF,
                dialect = dialect,
                isArray=isArray
            )
        ),
        oracleAction = lambda dialect, dbType: None,
        mysqlAction = lambda dialect, dbType: (
            mapF(
                data = (toArray(
                    toObject(*columnsAndKey)
                ) if isArray == True else toObject(*columnsAndKey)).label(label),
                table = tableF,
                dialect = dialect,
                isArray=isArray
            )
        ),
        mssqlAction = lambda dialect, dbType: None,
        elseAction = lambda dialect, dbType: (
            mapF(
                data = (SQLAType.cast(toArray(
                    toObject(*columnsAndKey)
                ), SQLARRAYType) if isArray == True else SQLAType.cast(toObject(*columnsAndKey), SQLAType.JSON)).label(label),
                table = tableF,
                dialect = DBCONFIG['dialect'],
                isArray=isArray
            )
        ),
    )


def SQLAddOrReductDATETIMEAction(
    column: any,
    time: float = 60,
    timeType: str = 'second',
    actionType: str = 'add'
):
    # column = deepcopy(column)
    timeType = deepcopy(timeType)
    time = deepcopy(time)

    allTimeTypes = ['second', 'minute']
    timeType = deepcopy(timeType) if timeType in allTimeTypes else 'second'
    actionTypes = ['add', 'reduce']
    actionType = deepcopy(actionType) if actionType in actionTypes else 'add'
    time = str(deepcopy(time) if type(time) in (int, float) else 60)
    return SQL_Action(
        sqliteAction = (lambda dialect, dbType: (
            SQLAType.func.DATETIME(
                column,
                SQLConcat(
                    ('+' if actionType == 'add' else '-'),
                    time,
                    ' ',
                    timeType,
                    mapAction = (lambda data: data[0] + data[1] + data[2] + data[3])
                )
            )
        ) ),
        oracleAction = (lambda dialect, dbType: (
            column + SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) if actionType == 'add' else (
            column - SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) ),
        mysqlAction = (lambda dialect, dbType: (
            column + SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) if actionType == 'add' else (
            column - SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) ),
        postgresAction = (lambda dialect, dbType: (
            column + SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) if actionType == 'add' else (
            column - SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        )),
        mssqlAction = (lambda dialect, dbType: (
            column + SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) if actionType == 'add' else (
            column - SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) ),
        elseAction = (lambda dialect, dbType: (
            column + SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) if actionType == 'add' else (
            column - SQLAType.cast(
                SQLConcat(time, ' ' + timeType.upper() + 'S', mapAction = (lambda data: data[0] + data[1])),
            SQLAType.Interval)
        ) ),
    )
    # (datetime(uthsr_u1.dateaddedactivationkey, '+' || CAST('900' AS VARCHAR) || ' ' || CAST(' SECONDS' AS VARCHAR))) AS dateexpiredactivationkey,


SQLARRAYType = SQL_Action(
    sqliteAction = (lambda dialect, dbType: JSON),
    oracleAction = (lambda dialect, dbType: ARRAY ),
    mysqlAction = (lambda dialect, dbType: ARRAY ),
    postgresAction = (lambda dialect, dbType: ARRAY ),
    mssqlAction = (lambda dialect, dbType: ARRAY ),
    elseAction = (lambda dialect, dbType: ARRAY ),
)
def SQLARRAY(dataType = None, dimensions: int = None):
    dataType = deepcopy(dataType)
    dimensions = deepcopy(dimensions)

    dimensions = dimensions if type(dimensions) == int else None
    return SQL_Action(
        sqliteAction = (lambda dialect, dbType: JSON(none_as_null=True)),
        oracleAction = (lambda dialect, dbType: ARRAY(item_type=dataType, dimensions=dimensions) if dataType is not None else ARRAY(dimensions=dimensions) ),
        mysqlAction = (lambda dialect, dbType: ARRAY(item_type=dataType, dimensions=dimensions) if dataType is not None else ARRAY(dimensions=dimensions) ),
        postgresAction = (lambda dialect, dbType: ARRAY(item_type=dataType, dimensions=dimensions) if dataType is not None else ARRAY(dimensions=dimensions) ),
        mssqlAction = (lambda dialect, dbType: ARRAY(item_type=dataType, dimensions=dimensions) if dataType is not None else ARRAY(dimensions=dimensions) ),
        elseAction = (lambda dialect, dbType: ARRAY(item_type=dataType, dimensions=dimensions) if dataType is not None else ARRAY(dimensions=dimensions) ),
    )
def SQLConcat(*elements, mapAction = lambda x: x[0]):
    elements = elements if type(elements) in (list, tuple) else None
    elements = elements if elements is not None and len(elements) > 0 else None
    mapAction = deepcopy(mapAction) if callable(mapAction) else (lambda x: x[0])

    def sqliteSQLConcat(datas):
        if datas is None:
            return None
        res = list(
            map(
                lambda x: SQLAType.cast(x, SQLAType.String),
                datas,
            )
        )
        return res
        

    return SQL_Action(
        sqliteAction = (lambda dialect, dbType: mapAction(sqliteSQLConcat(elements))),
        oracleAction = (lambda dialect, dbType: SQLAType.func.concat(*elements)),
        mysqlAction = (lambda dialect, dbType: SQLAType.func.concat(*elements)),
        postgresAction = (lambda dialect, dbType: SQLAType.func.concat(*elements)),
        mssqlAction = (lambda dialect, dbType: SQLAType.func.concat(*elements)),
        elseAction = (lambda dialect, dbType: SQLAType.func.concat(*elements)),
    ) if elements is not None else None


def __eq_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column == data)
def __ne_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column != data)
def __in_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.in_(data))
def __gt_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column > data)
def __lt_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column > data)
def __gte_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column >= data)
def __lte_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column >= data)
def __between_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.between(*data))
def __is_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.is_(data))
def __is_not_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.is_not(data))
def __is_distinct_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.is_distinct_from(data))
def __not_distinct_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.isnot_distinct_from(data))
def __like_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.like(data))
def __notlike_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.notlike(data))
def __ilike_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.ilike(data))
def __notilike_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.notilike(data))
def __starts_with_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.startswith(data))
def __ends_with_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.endswith(data))
def __contains_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.contains(data))
def __match_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.match(data))
def _regexp_match_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    if(DBCONFIG['dialect'] == 'postgres'):
        return (column.regexp_match(data)).compile(dialect=postgresql.dialect())
    elif(DBCONFIG['dialect'] == 'mysql'):
        return (column.regexp_match(data)).compile(dialect=postgresql.dialect())
    else:
        return (column.match(data))
def __concat_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    return (column.concat(data))
def __regex_replace_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    if(DBCONFIG['dialect'] == 'postgres'):
        return (column.regexp_replace(*data)).compile(dialect=postgresql.dialect())
def __collate_exec(column, data):
    # column = deepcopy(column)
    # dimensions = deepcopy(dimensions)

    if(DBCONFIG['dialect'] == 'mysql'):
        return (column.collate(data)).compile(dialect=mysql.dialect())
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
    '$not': __is_not_exec,
    '$isdistinct': __is_distinct_exec,
    '$notDistinct': __not_distinct_exec,
    '$like': __like_exec,
    '$notLike': __notlike_exec,
    '$ilike': __ilike_exec,
    '$notIlike': __notilike_exec,
    '$startsWith': __starts_with_exec,
    '$endsWith': __ends_with_exec,
    '$contains': __contains_exec,
    '$match': __match_exec,
    '$regexMatch': _regexp_match_exec,
    '$concat': __concat_exec,
    '$regexReplace': __regex_replace_exec,
    '$collate': __collate_exec,
}

def __and_exec(data):
    # data = data

    return and_(*data)
def __or_exec(data):
    # data = data

    return or_(*data)
def __not_exec(data):
    # data = data
    # print('-> hivipy - SQLAUtil | __not_exec - data:: ', data)
    return not_(and_(*data))
def __notOr_exec(data):
    # data = data

    return not_(or_(*data))
allComparisonOperator = {
    '_and': __and_exec,
    '_or': __or_exec,
    '_not': __not_exec,
    '_notOr': __notOr_exec,
}


allCond = {}
allCond.update(allLogicalOperator)
allCond.update(allComparisonOperator)


def querySessionPagination(
    sessionQuery: any,
    progressive = False,
    page: int = 1,
    pageSize: int = 10,
    returnException: bool = True,
):
    returnException = deepcopy(returnException) if type(returnException) == bool else True
    # sessionQuery = deepcopy(sessionQuery)
    progressive = deepcopy(progressive)
    page = deepcopy(page)
    pageSize = deepcopy(pageSize)

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
        
        # print("> querySessionPagination - sessionQuery:: ", sessionQuery)
        total: int = sessionQuery.count()
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

        query = sessionQuery.limit(limit).offset(offset)

        # print("> querySessionPagination - takeAllDatas:: ", takeAllDatas)
        # print("> querySessionPagination - pageSize:: ", pageSize)

        pagination = {
            'page': page,
            'pageSize': pageSize if takeAllDatas is False else -1,
            'pageCount': pageCount,
            'pageLength': query.count(),
            'total': total,
        }

        return query, pagination
    except Exception as err:
        MSG: str = 'Failure while paging over data'
        log.error(MSG)
        if returnException == True:
            raise err
        else:
            code = str(type(err))
            msg = str(err)
            stack = str(traceback.format_exc())
            trace = sys.exc_info()[2]
            
            if DEBUG == True:
                log.error(stack)

def querySessionSort(
    sessionQuery: any,
    options: list,
    Table: any = None,
    returnException: bool = True,
):
    returnException = deepcopy(returnException) if type(returnException) == bool else True
    # sessionQuery = deepcopy(sessionQuery)
    # options = deepcopy(options)
    # Table = deepcopy(Table)

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
            for index, option in enumerate(options):
                if(option[1] == 'asc'):
                    sessionQuery = sessionQuery.order_by(asc(getattr(Table, option[0])))
                elif(option[1] == 'desc'):
                    sessionQuery = sessionQuery.order_by(desc(getattr(Table, option[0])))
        else:
            if(DBCONFIG['dialect'] in ('postgres', 'sqlite')):
                sessionQuery = sessionQuery.order_by(
                    func.random()
                )
            elif(DBCONFIG['dialect'] in ('mysql')):
                sessionQuery = sessionQuery.order_by(
                    func.rand()
                )
            elif(DBCONFIG['dialect'] in ('oracle')):
                sessionQuery = sessionQuery.order_by(
                    func.rand()
                )
            else:
                sessionQuery = sessionQuery.order_by('dbms_random.value')

        # print("> querySessionSort - sessionQuery:: ", sessionQuery)

        return sessionQuery
    except Exception as err:
        MSG: str = 'Failure while sorting on data'
        log.error(MSG)
        if returnException == True:
            raise err
        else:
            code = str(type(err))
            msg = str(err)
            stack = str(traceback.format_exc())
            trace = sys.exc_info()[2]
            
            if DEBUG == True:
                log.error(stack)

def queryFilter(
    query: dict,
    Table: any,
    returnException: bool = True,
):
    returnException = deepcopy(returnException) if type(returnException) == bool else True
    query = deepcopy(query)
    # Table = deepcopy(Table)
    returnException = deepcopy(returnException) if type(returnException) == bool else True

    try:
        return applyComparisonOperators(
            data = query,
            co = allComparisonOperator,
            lo = allLogicalOperator,
            op = allCond,
            Table = Table,
        )
    except Exception as err:
        MSG: str = 'Failure while creating sql filter query'
        log.error(MSG)
        if returnException == True:
            raise err
        else:
            code = str(type(err))
            msg = str(err)
            stack = str(traceback.format_exc())
            trace = sys.exc_info()[2]
            
            if DEBUG == True:
                log.error(stack)
   
def getColumnLO(columnStr, Table):
    # columnStr = deepcopy(columnStr)
    # Table = deepcopy(Table)

    types = ('text', 'char', 'varchar', 'integer', 'decimal', 'numeric', 'real', 'timestamp', 'datetime', 'date', 'time', 'json')
    defaultType = types[0]
    var2 = re.sub(
        re.compile(r'\s', re.IGNORECASE | re.DOTALL),
        '', columnStr
    )
    var2 = var2.split(":")
    names = list(
        filter(
            lambda x: type(x in (str, int, float)),
            var2[0].split("."),
        )
    ) if (
        type(var2) in (list, tuple) and
        0 in range(len(var2))
    ) else []
    typeVar = var2[1].lower() if (
        type(var2) in (list, tuple) and
        1 in range(len(var2)) and
        var2[1] in types
    ) else None
    config = {
        'names': names,
        'type': typeVar,
    }

    res = None
    for index, value in enumerate(config['names']):
        if(index == 0):
            res = getattr(Table, value)
        else:
            res = res[value]
    if(
        len(config['names']) > 1
    ):
        res = res.astext
    if(res is not None):
        if(config['type'] == 'text'):
            res = cast(res, SQLAType.Text)
        elif(config['type'] == 'char'):
            res = cast(res, SQLAType.CHAR)
        elif(config['type'] == 'varchar'):
            res = cast(res, SQLAType.VARCHAR)
        elif(config['type'] == 'integer'):
            res = cast(res, SQLAType.Integer)
        elif(config['type'] == 'numeric'):
            res = cast(res, SQLAType.Numeric)
        elif(config['type'] == 'real'):
            res = cast(res, SQLAType.REAL)
        elif(config['type'] == 'decimal'):
            res = cast(res, SQLAType.DECIMAL)
        elif(config['type'] == 'TIMESTAMP'):
            res = cast(res, SQLAType.TIMESTAMP)
        elif(config['type'] == 'datetime'):
            res = cast(res, SQLAType.DateTime)
        elif(config['type'] == 'date'):
            res = cast(res, SQLAType.Date)
        elif(config['type'] == 'time'):
            res = cast(res, SQLAType.Time)
        elif(config['type'] == 'boolean'):
            res = cast(res, SQLAType.Boolean)
        elif(config['type'] == 'json'):
            res = cast(res, SQLAType.JSON)

    # print("> getColumnLO - columnStr:: ", columnStr)
    # print("> getColumnLO - config:: ", config)
    # print("> getColumnLO - res:: ", res)

    return res

def cleanForExtractCompositeType(
    data: any,
    cond: any,
    parent: bool = None,
):
    # data = data
    # cond = deepcopy(cond)
    # parent = deepcopy(parent)

    parent = parent if type(parent) in (str, int, float) else None
    
    # print("> applyComparisonOperators - list(cond.keys()):: ", list(cond.keys()))
    if(
        type(data) in [list, tuple, dict]
    ):
        # print("> applyComparisonOperators | cond:: ", cond)
        # print("> applyComparisonOperators | data:: ", data)
        for index, keyOrValue in enumerate(data):
            key = index if type(data) in [list, tuple] else keyOrValue
            element = data[key]
            parentElement = parent

            keyIsNotOp = not(key in list(allCond.keys()))
            elementIsValue = (
                type(element) in (str, int, float, bool, list, tuple) or (
                    type(element) == dict and
                    len(
                        list(
                            filter(
                                lambda x: (x in cond.keys()),
                                element.keys()
                            )
                        )
                    ) <= 0 
                )
            )
            # print("> applyComparisonOperators | index:: ", index, " - keyIsNotOp:: ", keyIsNotOp)
            # print("> applyComparisonOperators | index:: ", index, " - key:: ", key)
            check91 = (type(element) == dict and elementIsValue == True and keyIsNotOp == True)
            # print("> applyComparisonOperators | index:: ", index, " - check91:: ", check91)
            if(check91):
                elementValues = list(element.values())
                elementValuesExists = list(
                    map(
                        lambda elementVE: (
                            type(elementVE) in (str, int, float, bool, list, tuple) or (
                                type(elementVE) == dict and
                                len(
                                    list(
                                        filter(
                                            lambda x: (x in cond.keys()),
                                            elementVE.keys()
                                        )
                                    )
                                ) <= 0 
                            )
                        ),
                        elementValues,
                    )
                )
                # print("> applyComparisonOperators | index:: ", index, " - elementValues:: ", elementValues)
                # print("> applyComparisonOperators | index:: ", index, " - elementValuesExists:: ", elementValuesExists)
                elementValuesExistsFalse = (
                    reduce(
                        lambda x, y: (
                            False if(
                                x != True or
                                y != True
                            ) else True
                        ),
                        elementValuesExists,
                    )
                )
                if(elementValuesExistsFalse != True):
                    elementIsValue = False
                # print("> applyComparisonOperators | index:: ", index, " - elementValues:: ", elementValues)
                # print("> applyComparisonOperators | index:: ", index, " - elementValuesExists:: ", elementValuesExists)
                # print("> applyComparisonOperators | index:: ", index, " - elementValuesExistsFalse:: ", elementValuesExistsFalse)
            parentElementNotIsOp = (
                not(parentElement in cond.keys()) or
                parentElement is None
            )
            dataIsValue = (
                # , list, tuple
                type(data) in (str, int, float, bool) or (
                    type(data) == dict and
                    len(
                        list(
                            filter(
                                lambda x: (x in cond.keys()),
                                data.keys()
                            )
                        )
                    ) <= 0 
                )
            )
            isNotCompositeType = not(
                (key in cond.keys()) or (
                    (parentElement in cond.keys())
                )
            )
            # print("> applyComparisonOperators | index:: ", index, " - key:: ", key)
            # print("> applyComparisonOperators | index:: ", index, " - parentElement:: ", parentElement)
            # print("> applyComparisonOperators | index:: ", index, " - element:: ", element)
            # print("> applyComparisonOperators | index:: ", index, " - keyIsNotOp:: ", keyIsNotOp)
            # print("> applyComparisonOperators | index:: ", index, " - parentElementNotIsOp:: ", parentElementNotIsOp)
            # print("> applyComparisonOperators | index:: ", index, " - isNotCompositeType:: ", isNotCompositeType)
            # print("> applyComparisonOperators | index:: ", index, " - elementIsValue:: ", elementIsValue)
            # print("> applyComparisonOperators | index:: ", index, " - dataIsValue:: ", dataIsValue)
            
            # cond 1
            constraint1 = (
                keyIsNotOp and
                parentElementNotIsOp and
                elementIsValue
            )
            """(
                keyIsNotOp and
                isNotCompositeType and
                elementIsValue and
                dataIsValue
            )"""

            # print("> applyComparisonOperators | index:: ", index, " - constraint1:: ", constraint1)

            if(not(constraint1)):
                element = cleanForExtractCompositeType(element, cond = cond, parent = key)
            if(constraint1):
                element = {
                    '$eq': element,
                }
            
            data[key] = element

    return data
def extractCompositeType(
    data: any,
    cond: any,
    parent: bool = None,
    mapKey = (
        lambda parentkey, childKey : "{parent}.{child}".format(
            parent = parentkey,
            child = childKey,
        )
    )
):
    # data = data
    cond = deepcopy(cond)
    parent = deepcopy(parent)
    mapKey = deepcopy(mapKey)

    parent = parent if type(parent) == str else None

    if(type(data) == dict):
        
        subData = {}
        compositeParentIds = []
        start = True

        while len(compositeParentIds) > 0 or start:
            compositeParentIds = []
            subData = {}

            for index, key in enumerate(data):
                element = data[key]
                parentElement = key
                
                if(type(element) == dict):
                    finalValue = {}
                    for indexSub, keySub in enumerate(element):
                        elementSub = element[keySub]
                        constraint = (
                            parentElement is not None and
                            not(keySub in cond.keys()) and
                            not(parentElement in cond.keys())
                        )
                        newkeySub = mapKey(parentElement, keySub) if callable(mapKey) else"{parent}.{child}".format(
                            parent = parentElement,
                            child = keySub,
                        )

                        if(constraint):
                            finalValue[newkeySub] = elementSub
                            compositeParentIds.append(parentElement)
                        element[keySub] = elementSub
                    subData.update(finalValue)
                data[key] = element
                
            if(
                len(subData.keys()) > 0
            ):
                data.update(subData)

                for index, key in enumerate(compositeParentIds):
                    if(key in data.keys()):
                        del data[key]
            start = False
    finaldata = {}
    for index, key in enumerate(data):
        if(type(data[key]) == dict):
            element = extractCompositeType(data[key], cond = cond, parent = key, mapKey = mapKey)
        else:
            element = data[key]
        finaldata[key] = element
    data = finaldata

    # if(parent is None):
        # print("> extractCompositeType - data:: ", data)

    return data
def applyLogicalOperators(
    data: any,
    cond: any,
    Table: any = None,
    parent: any = None,
):
    data = data if type(data) in (list, tuple, dict, bool, int, float) else data
    cond = deepcopy(cond)
    Table = deepcopy(Table)
    parent = deepcopy(parent)

    parent = parent if type(parent) == str else None
    data = data if type(data) in (list, tuple, dict) else (
        [] if type(data) in (list, tuple) else {}
    )

    # print("> applyLogicalOperators - Table:: ", Table)
    # print("> applyLogicalOperators - parent:: ", parent)

    if(
        (
            type(data) in (list, tuple, dict) and
            len(data) > 0
        ) or (
            type(data) == dict and
            len(data.keys()) > 0
        )
    ):
        subData = {}
        compositeParentIds = []
        for index, key in enumerate(data):
            element = data[key]
            parentElement = key

            # print("> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - key:: ", key)
            # print("> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - data:: ", data)
            # print("> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " - data[", key, "]:: ", element)
            
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

                    # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - elementSub:: ", elementSub)
                    # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - keySub:: ", keySub)
                    # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - newkeySub:: ", newkeySub)
                    # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - constraint:: ", constraint)
                    # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - cond.keys():: ", cond.keys())

                    if(constraint):
                        finalValue[newkeySub] = cond[keySub](
                            getColumnLO(parentElement, Table = Table),
                            elementSub,
                        )
                        compositeParentIds.append(parentElement)
                        # print("\t> applyLogicalOperators | finalValue[", newkeySub, "]:: ", finalValue[newkeySub])
                        # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - finalValue:: ", finalValue)
                        # print("\t> applyLogicalOperators | parent:: ", parent, " - index:: ", index, " | parentElement:: ", parentElement, " - indexSub:: ", indexSub, " - data:: ", data)
                        # data[newkeySub] = elementSub
                    element[keySub] = elementSub
                # print("> applyLogicalOperators | subData:: ", subData)
                subData = {
                    **subData,
                    **finalValue,
                }
            data[key] = element
        
        # print("> applyLogicalOperators | subData.items():: ", subData.items())
        # print("> applyLogicalOperators | len(subData.keys()):: ", len(subData.keys()))
        if(
            len(subData.keys()) > 0
        ):
            data = {
                **data,
                **subData,
            }
            # print("> applyLogicalOperators | subData:: ", subData)
            # print("> applyLogicalOperators | compositeParentIds:: ", compositeParentIds)

            for index, key in enumerate(compositeParentIds):
                if(key in data.keys()):
                    del data[key]
        finaldata = [] if type(data) in (list, tuple) else {}
        for index, keyOrValue in enumerate(data):
            key = index if type(data) in (list, tuple) else keyOrValue
            element = data[key]
            dataALO, TableALO = applyLogicalOperators(element, cond = cond, parent = key, Table = Table)
            element = dataALO
            Table = TableALO
            if(
                type(element) in (str, int, float) or (
                    type(element) in (list, tuple, dict) and
                    len(element.keys()) > 0
                )
            ):
                finaldata[key] = element
        # print("> applyLogicalOperators | finaldata(old):: ", finaldata)

        finaldata = list(finaldata) if type(data) in (list, tuple) else dict(finaldata.values())
        # print("> applyLogicalOperators | finaldata:: ", finaldata)
        """if(len(finaldata) > 0):
            data = finaldata"""
    else:
        data = None

    if(parent == None):
        if(type(data) in (list, tuple, dict)):
            data = list(data.values())

    return data, Table
def applyComparisonOperators(
    data: any,
    co: any,
    lo: any,
    op: any,
    Table: any = None,
    parent: any = None,
):
    data = data if type(data) in (list, tuple, dict, bool, int, float) else data
    co = deepcopy(co)
    lo = deepcopy(lo)
    op = deepcopy(op)
    Table = deepcopy(Table)
    parent = deepcopy(parent)

    parent = parent if type(parent) in [str, int, float] else None

    # print("> applyComparisonOperators - data:: ", data)
    # print("> applyComparisonOperators - co.keys():: ", co.keys())
    # print("> applyComparisonOperators - lo.keys():: ", lo.keys())
    if(
        (
            type(data) in (list, tuple, dict) and
            len(data) > 0
        ) or (
            type(data) == dict and
            len(data.keys()) > 0
        )
    ):
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
            # print("\t> applyComparisonOperators | index:: ", index, " - key:: ", key)
            # print("\t> applyComparisonOperators | index:: ", index, " - cond:: ", cond)

        # - primaryData
        # print("\t> applyComparisonOperators | primaryData:: ", primaryData)
        for index, keyOrValue in enumerate(primaryData):
            key = index if type(primaryData) in (list, tuple) else keyOrValue
            element = primaryData[key]

            # print("\t\t\t---> applyComparisonOperators | index:: ", index, " - key:: ", key)
            if(
                type(element) in (list, tuple)
            ):
                # print("\t\t\t---> applyComparisonOperators | index:: ", index, " - element(old):: ", element)
                # print("\t> applyComparisonOperators | element:: ", element)
                for indexSub, valueSub in enumerate(element):
                    keySub = indexSub
                    elementSub = element[keySub]

                    # print("\t\t\t\t\t---> applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - keySub:: ", keySub)
                    # print("\t\t\t\t\t---> applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - element[", keySub, "] [BEFORE]:: ", element[keySub])
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
                        dataALO, TableALO = applyLogicalOperators(
                            data = elementSub,
                            cond = lo,
                            Table = Table,
                        )
                        elementSub = dataALO
                        Table = TableALO
                        elementSub = co['_and'](elementSub)
                    else:
                        elementSub, TableF = applyComparisonOperators(elementSub, co = co, lo = lo, op = op, Table = Table, parent = keySub)
                        Table = TableF
                    element[keySub] = elementSub
                    # print("\t\t\t\t\t---> applyComparisonOperators | index:: ", index, " -  indexSub:: ", indexSub, " - element[", keySub, "]:: ", element[keySub])
                # print("\t\t\t---> applyComparisonOperators | index:: ", index, " - element:: ", element)

            # --

            # element = applyComparisonOperators(element, co = co, lo = lo, op = op, Table = Table, parent = parent)
            # print("\t\t\t---> applyComparisonOperators | index:: ", index, " - element  [BEFORE]:: ", element)
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
        dataALO, TableALO = applyLogicalOperators(
            data = otherData,
            cond = lo,
            Table = Table,
        )
        otherData = dataALO
        Table = TableALO
        # - primaryData
        primaryData = list(primaryData.values())

        # print("> applyComparisonOperators - otherData:: ", otherData)
        # print("> applyComparisonOperators - primaryData:: ", primaryData)
            
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
            # print("> applyComparisonOperators - co['_and'](otherData):: ", co['_and'](otherData))
            # print("> applyComparisonOperators - co['_and'](primaryData):: ", co['_and'](primaryData))
            # print("> applyComparisonOperators - data [BEFORE]:: ", data)
            data = co['_and']([
                co['_and'](otherData),
                co['_and'](primaryData),
            ])
        elif(
            type(primaryData) in (list, tuple) and
            len(primaryData) > 0
        ):
            data = co['_and'](primaryData)
            # print("> applyComparisonOperators - data:: ", data)
        elif(
            type(otherData) in (list, tuple) and
            len(otherData) > 0
        ):
            data = co['_and'](otherData)
                
    return data, Table