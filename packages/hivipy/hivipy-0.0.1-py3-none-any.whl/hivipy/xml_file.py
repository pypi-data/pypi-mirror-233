from copy import deepcopy
from typing import *
from pathlib import Path
import os
import platform
import asyncio
import logging
import traceback
import sys
import re
import json
import configparser
import xmltodict
# import importlib
from datetime import datetime, date
from werkzeug.datastructures import FileStorage

from .config import dateFormat1
from .confUtils import _transformStringConfToArray


log = logging.getLogger(__name__)

class XMLFile():
    def read(self, path: str, mode: str = 'r', encoding = 'utf-8'):
        try:
            pathTarget = open(path, mode = mode, encoding = encoding).read()
            # print("> hivipy.xml_file.py | XMLFile.read - path:: \n", path)
            # print("> hivipy.xml_file.py | XMLFile.read - pathTarget:: \n", pathTarget)

            return xmltodict.parse(pathTarget, process_namespaces=True)
        except Exception as err:
            e = "[ERROR] hivipy.xml_file.py | read - err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def write(self, path: str, datas: dict, mode: str = 'wb', encoding = 'utf-8'):
        try:
            datas = datas if type(datas) == dict else {}
            out = xmltodict.unparse(datas, pretty=True)
            # print("> hivipy.xml_file.py | XMLFile.write - out:: ", out)
            with open(path, mode) as file:
                file.write(out.encode(encoding))

            return True
        except Exception as err:
            e = "[ERROR] hivipy.xml_file.py | XMLFile.write - err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return False