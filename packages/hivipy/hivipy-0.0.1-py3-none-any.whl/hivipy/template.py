import copy
import math
import json
import pygeoip
from random import *
from datetime import datetime, date
from dateutil.parser import parse
from urllib.parse import urljoin, urlencode
from copy import deepcopy
from .utils import JSONStringify, dataBinding
from .string import RandomStr, toStringToSpecifFormat, tocamelcase, sanitizeRouteaUrl


def getInitialContext():
    return {
        '_formatters': {
            'lower': (lambda value: str(value).lower()),
            'upper': (lambda value: str(value).upper()),
            'capitalize': (lambda value: str(value).capitalize()),
            'ucFirst': (lambda value: str(value)[0].upper() + str(value)[1:].lower()),
            'camelcase': (lambda value: tocamelcase(value, allState=False)),
            'Camelcase': (lambda value: tocamelcase(value, allState=True)),
            'cleanedLabel': (lambda value: toStringToSpecifFormat(value, sep='')),
            'stringToHyphenFormat': (lambda value: toStringToSpecifFormat(value, sep='-')),
            'stringToUnderscoreFormat': (lambda value: toStringToSpecifFormat(value, sep='_')),
            'JSONStringify': JSONStringify,
            'dataBinding': dataBinding,
        }
    }

initialContext = getInitialContext()