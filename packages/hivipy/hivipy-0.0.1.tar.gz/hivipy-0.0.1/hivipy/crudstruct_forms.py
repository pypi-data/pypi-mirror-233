import datetime
import pytz
from .string import RandomIdentifier
from .config import pagesPossibles
from .JON import String as JONString, Number as JONNumber, Boolean as JONBoolean, Date as JONDate, File as JONFile, Enum as JONEnum, NotInEnum as JONNotInEnum, ChosenType as JONChosenType, Object as JONObject, Array as JONArray
from .config import pagesPossibles, responsesPossibles


def structEditResult(lang: str):
    return JONObject(lang).struct({
        'data': JONObject(lang).min(1).required(),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    })
def structEditMultipleResult(lang: str):
    return JONObject(lang).struct({
        'data': JONArray(lang).types(
            JONObject(lang).min(1).required(),
        ).min(1).required(),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    })


def structFindOneResult(lang: str):
    return JONObject(lang).struct({
        'data': JONObject(lang).min(1).required(),
        'exists': JONEnum(lang).choices(True).required(),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
def structExistsResult(lang: str):
    return JONObject(lang).struct({
        'exists': JONEnum(lang).choices(True).required(),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
def structFindAllResult(lang: str):
    return JONObject(lang).struct({
        'datas': JONArray(lang).types(
            JONObject(lang).required()
        ).required(),
        'meta': JONObject(lang).struct({
            'pagination': JONObject(lang).struct({
                'page': JONNumber(lang).min(1).required(),
                'pageSize': JONEnum(lang).choices(*pagesPossibles).required(),
                'pageLength': JONNumber(lang).min(1).required(),
                'pageCount': JONNumber(lang).min(1).required(),
                'total': JONNumber(lang).min(0).required(),
            }).required(),
        }).required(),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()
    
def structExtractResult(lang: str):
    return JONObject(lang).struct({
        'datas': JONArray(lang).types(
            JONObject(lang).required()
        ).required(),
        'meta': JONObject(lang).struct({
            'invalid-datas': JONArray(lang).types(
                JONObject(lang).struct({
                    'key': JONNumber(lang).min(1).required(),
                    'schemas': JONArray(lang).types(
                        JONString(lang).min(1).required()
                    ).required(),
                }).required(),
            ).length(0),
        }),
        'notif': JONObject(lang).struct({
            'type': JONEnum(lang).choices(responsesPossibles['good_action']['type']).required(),
            'code': JONEnum(lang).choices(responsesPossibles['good_action']['code']).required(),
            'status': JONEnum(lang).choices(responsesPossibles['good_action']['status']).required(),
            'message': JONEnum(lang).choices(responsesPossibles['good_action']['message'][lang]).required(),
        }).required(),
    }).required()