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
import collections
import codecs
# import importlib
from datetime import datetime, date
from werkzeug.datastructures import FileStorage

from .xml_file import XMLFile

from .config import dateFormat1
from .confUtils import _transformStringConfToArray


log = logging.getLogger(__name__)
# PROJECT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.getcwd()
# PROJECT_DIR = './'
print("> hivipy.hivi_init - PROJECT_DIR:: ", PROJECT_DIR)
# print("> hivipy.hivi_init - os.getcwd():: ", os.getcwd())

def convertToBoolean(
    value: any,
) -> bool:
    # value = deepcopy(value)
    defaultVal = deepcopy(value)
    valuesPossibles: list = ('true', 't', '1', 'false', 'f', '0')
    res = defaultVal
    if value is not None and (
        str(value).lower() in valuesPossibles or
        type(value) == bool
    ):
        res = True if str(value).lower() in ('true', 't', '1') else False
    return res

def createModulePath(*paths):
    res: str = createRelativeDir(*paths)
    if res is not None:
        res = '.'.join(
            list(
                filter(
                    lambda x: type(x) == str and len(x) > 0,
                    res.split('/'),
                )
            )
        )
    return res
def createRelativeDir(*paths):
    if(type(paths) in (list, tuple) and paths is not None):
        paths = list(
            map(
                lambda path: str(path),
                list(
                    filter(
                        lambda path: type(path) in (int, float) or ( type(path) == str and len(path) > 0 ),
                        paths,
                    )
                )
            )
        )
        for index, path in enumerate(paths):
            if(index < len(paths) - 1):
                paths[index] = paths[index].replace('.', '/').replace('//', '/')
        return str(os.path.join(*paths).replace('\\', '/').replace('//', '/'))
    else:
        return None
def createDir(*paths):
    """ createDir - Fonction de creation d'un chemin absolu

    Cette methode permet de creer un chemin absolu en fonction de plusieurs autres chemins

    Parameters
    ------------
        paths: list
            l'ensemble de tous les paths que vous ciblez pour votre chemin
    Return
    -----------
        dir : str
            Le path cree en fonction de la racine et des autres paths
    """
    if(type(paths) in (list, tuple) and paths is not None):
        paths = list(
            map(
                lambda path: str(path),
                list(
                    filter(
                        lambda path: type(path) in (int, float) or ( type(path) == str and len(path) > 0 ),
                        paths,
                    )
                )
            )
        )
        for index, path in enumerate(paths):
            if type(paths[index]) == str:
                paths[index] = '/'.join(
                    list(
                        filter(
                            lambda subPath: (type(subPath) == str and len(subPath)),
                            str(paths[index]).split('/'),
                        )
                    )
                )
                paths[index] = '\\'.join(
                    list(
                        filter(
                            lambda subPath: (type(subPath) == str and len(subPath)),
                            str(paths[index]).split('\\'),
                        )
                    )
                )
            if(index < len(paths) - 1):
                paths[index] = paths[index].replace('.', '/').replace('//', '/')
        # print("> hivipy.hivi_init.py | createDir - paths:: ", paths)
        return str(os.path.join(PROJECT_DIR, *paths).replace('\\', '/').replace('//', '/'))
    else:
        return None
def createStaticMediaPath(*paths):
    manager = Manager()
    structConf = manager.getStructConfig()
    staticFolder = structConf['staticFolder']
    return createDir(staticFolder, *paths)
def createStaticModelPath(*paths):
    manager = Manager()
    structConf = manager.getStructConfig()
    staticModelFolder = structConf['staticModelFolder']
    return createDir(staticModelFolder, *paths)

class Manager():
    """Permet de gerer les proprités se trouvant dans le .ini du dossier main et tous les fichiers de configurations des modules
    """
    defaultPropertiesFile = 'main/hiviconfig.xml'
    allProperties = []
    config: configparser.ConfigParser = None
    allConf: dict = None
    readAction = True

    def __init__(self) -> None:
        pass

    def getInitProperties(self,):
        return self.getPropertiesModule(self.defaultPropertiesFile)

    def getAllModuleNames(self,):
        return self.getAppModuleNames(haveInitialModule = True)
    def getAppModuleNames(self, haveInitialModule: bool = False):
        res = None
        haveInitialModule = haveInitialModule if type(haveInitialModule) == bool else False
        allModules = []
        try:
            properties = self.getInitProperties()
            # print("> hivipy.hivi_init.py | getAppModuleNames - properties:: ", properties)
            propertiesContent = properties if type(properties) == dict and len(properties.keys()) > 0 else {}
            modulesStr = None
            # print("> hivipy.hivi_init.py | getAppModuleNames - propertiesContent:: ", propertiesContent)
            if("DEFAULT" in propertiesContent):
                if("modules" in propertiesContent["DEFAULT"].keys()):
                    modulesStr = propertiesContent["DEFAULT"]["modules"]
                    modulesStr = modulesStr if type(modulesStr) in (list, tuple) else [deepcopy(modulesStr)]

            if modulesStr is not None :
                allModules = deepcopy(modulesStr)

                # print("> hivipy.hivi_init.py | getAppModuleNames - properties:: ", properties)
                # print("> hivipy.hivi_init.py | getAppModuleNames - propertiesContent:: ", propertiesContent)
                # print("> hivipy.hivi_init.py | getAppModuleNames - modulesStr:: ", modulesStr)

                res = list(
                    filter(
                        lambda module: Path(createDir(
                            module,
                            "conf".replace('.', '/') + ".xml"
                        )).exists(),
                        allModules,
                    )
                ) if allModules is not None else None
            else:
                res = []
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES NOMS DE MODULE | err:: {err} ".format(
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            res = None

        copyModules1 = deepcopy(allModules)
        self.checkInvalidModules(copyModules1)
        # copyModules2 = deepcopy(allModules)

        return ['init'] + res if haveInitialModule == True else res
    def getAppModuleProperties(self,):
        modulesStr = self.getAppModuleNames()
        # print("> hivipy.hivi_init.py | getAppModuleProperties - modulesStr:: \n", modulesStr)
        modules = {}
        if modulesStr is not None:
            for index, data in enumerate(modulesStr):
                modules[data] = os.path.join(data, 'conf.xml')
            # print("> hivipy.hivi_init.py | getAppModuleProperties - modules:: \n", modules)
        return self.getProperties(**modules)
    def getAppModuleUrlConfPath(self,):
        allModuleNames = self.getAppModuleNames()
        allModuleNames = list(
            filter(
                lambda module: Path(createDir(
                    module,
                    "conf".replace('.', '/') + ".xml"
                )).exists(),
                allModuleNames,
            )
        ) if allModuleNames is not None else None
        FallModuleNames = {
            'init': createDir(self.defaultPropertiesFile),
        }
        if allModuleNames is not None:
            modulePath = {}
            for index, moduleName in enumerate(allModuleNames):
                modulePath[moduleName] = createDir(
                    moduleName if moduleName != 'init' else 'main',
                    "conf".replace('.', '/') + ".xml"
                )
            FallModuleNames.update(modulePath)
        return FallModuleNames
    def checkInvalidModules(self, moduleNames: list, sendError = True):
        sendError = sendError if type(sendError) == bool else True
        moduleNames = list(
            filter(
                lambda name: type(name) == str and len(name) > 0,
                moduleNames,
            )
        ) if type(moduleNames) in (list, tuple) else []
        errRes = None
        invalidModules = []
        try:
            invalidModules = list(
                filter(
                    lambda module: not(Path(createDir(
                        module,
                        "conf".replace('.', '/') + ".xml"
                    )).exists() == True),
                    moduleNames,
                )
            ) if moduleNames is not None else None
            if(
                (
                    invalidModules is not None and
                    len(invalidModules) > 0
                ) or invalidModules is None
            ):
                errRes = Exception('[ERROR] hivipy.hivi_init.py | LES MODULES SUIVANTS SONT INTROUVABLES:: "{value}"'.format(
                    value = ', '.join(invalidModules)
                ))
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA VERIFICATION DES MODULES SUIVANT:: \"{value}\" | err:: {err} ".format(
                value = ', '.join(moduleNames),
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            errRes = Exception(stack)
            invalidModules = None

        if(sendError and errRes is not None):
            raise errRes
        elif(not(sendError == True) and type(invalidModules) in (list, tuple)):
            return invalidModules
    def initAppModuleProperties(self,):
        self.allConf = self.getAppModuleProperties()
        return self
    def getModulesRequiredForModule(self, moduleName: str):
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            modulesRequired = moduleProperties['DEFAULT']['modules_required'] if(
                "DEFAULT" in moduleProperties and
                "modules_required" in moduleProperties["DEFAULT"]
            ) else None
            if modulesRequired is not None:
                modulesRequired = modulesRequired if type(modulesRequired) in (list, tuple) else [modulesRequired]

            self.checkInvalidModules(modulesRequired)
            
            return list(
                filter(
                    lambda module: Path(createDir(
                        module,
                        "conf".replace('.', '/') + ".xml"
                    )).exists(),
                    modulesRequired,
                )
            ) if type(modulesRequired) in (list, tuple) else None
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES MODULES REQUIS DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def checkAllModulesRequiredForModule(self, moduleName: str):
        res = None
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            modulesRequired = moduleProperties['DEFAULT']['modules_required'] if(
                "DEFAULT" in moduleProperties and
                "modules_required" in moduleProperties["DEFAULT"]
            ) else None
            if modulesRequired is not None:
                modulesRequired = modulesRequired if type(modulesRequired) in (list, tuple) else [modulesRequired]

            if(
                modulesRequired is None or
                (
                    type(modulesRequired) in (list, tuple) and
                    len(modulesRequired) <= 0
                ) or moduleName == 'init'
            ):
                res = True
            else:
                invalidModules = self.checkInvalidModules(modulesRequired, sendError=False)
                if(
                    invalidModules is not None and
                    len(invalidModules) > 0
                ):
                    res = False
                    raise Exception('[ERROR] hivipy.hivi_init.py | LES MODULES REQUIS SUIVANT SONT INEXISTANTS:: "{value}" DANS LE MODULE "{module}"'.format(
                        value = ', '.join(invalidModules),
                        module = moduleName,
                    ))
                elif invalidModules is None:
                    res = False
                    raise Exception(
                        "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA VERIFICATION DES MODULES REQUIS POUR LE MODULE \"{name}\"".format(
                            name = moduleName,
                        )
                    )

        except Exception as err:
            e = str(err)
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            res = False
            raise Exception(stack)

        return res
    def getModuleProperties(self, moduleName: str):
        try:
            # print("> hivipy.hivi_init.py | getModuleProperties - moduleName:: ", moduleName)
            return self.getPropertiesModule(moduleName = moduleName)
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES PROPRIETES DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModuleServices(self, moduleName: str):
        try:
            # print("> hivipy.hivi_init.py | getModuleServices <")
            moduleProperties = self.getModuleProperties(moduleName)
            # print("> hivipy.hivi_init.py | getModuleServices - moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py | getModuleServices - moduleProperties:: ", moduleProperties)
            services = moduleProperties['DEFAULT']['services'] if(
                "DEFAULT" in moduleProperties and
                "services" in moduleProperties["DEFAULT"]
            ) else None
            if services is not None:
                services = services if type(services) in (list, tuple) else [services]
            if(services is not None):
                notFoundServices = list(
                    filter(
                        lambda service: not(
                            Path(createDir(
                                moduleName,
                                "views",
                                service.replace('.', '/') + ".py"
                            )).exists()
                        ),
                        services,
                    )
                )
                if(len(notFoundServices) <= 0):
                    services = list(
                        filter(
                            lambda service: Path(createDir(
                                moduleName,
                                "views",
                                service.replace('.', '/') + ".py"
                            )).exists(),
                            services,
                        )
                    )
                    services = list(
                        map(
                            lambda service: __import__(
                                "{module}.views.{service}".format(
                                    module = moduleName,
                                    service = service,
                                ),
                                globals(),
                                locals(),
                                ['*'],
                            ),
                            services,
                        )
                    )
                    # print("> hivipy.hivi_init.py | getModuleServices - services:: ", services)
                else:
                    raise Exception("Le service \"{service}\" est inexistant dans le module \"{name}\"".format(
                        name = moduleName,
                        service = notFoundServices[0],
                    ))

            return services
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES SERVICES DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getAppMiddlewares(self,):
        try:
            moduleNames = self.getAllModuleNames()
            res: list = []
            for index, moduleName in enumerate(moduleNames):
                moduleMiddlewares = self.getModuleMiddlewares(moduleName=moduleName)
                if moduleMiddlewares is not None:
                    res = res + moduleMiddlewares
            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES MIDDLEWARES DES MODULES | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModuleMiddlewares(self, moduleName: str):
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            moduleName = 'main' if moduleName == 'init' else moduleName
            # print("> hivipy.hivi_init.py | getModuleMiddlewares - moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py | getModuleMiddlewares - moduleProperties:: ", moduleProperties)
            middlewares = moduleProperties['DEFAULT']['middlewares'] if(
                "DEFAULT" in moduleProperties and
                "middlewares" in moduleProperties["DEFAULT"]
            ) else None
            if middlewares is not None:
                middlewares = middlewares if type(middlewares) in (list, tuple) else [middlewares]
            # print("> hivipy.hivi_init.py | getModuleMiddlewares - middlewares:: ", middlewares)
            if(middlewares is not None):
                notFoundMiddlewares = list(
                    filter(
                        lambda middleware: not(
                            Path(createDir(
                                moduleName,
                                "middlewares",
                                middleware.replace('.', '/') + ".py"
                            )).exists()
                        ),
                        middlewares,
                    )
                )
                if(len(notFoundMiddlewares) <= 0):
                    middlewares = list(
                        filter(
                            lambda middleware: Path(createDir(
                                moduleName,
                                "middlewares",
                                middleware.replace('.', '/') + ".py"
                            )).exists(),
                            middlewares,
                        )
                    )
                    middlewares = list(
                        map(
                            lambda middleware: __import__(
                                "{module}.middlewares.{middleware}".format(
                                    module = moduleName,
                                    middleware = middleware,
                                ),
                                globals(),
                                locals(),
                                ['*'],
                            ).AppMiddleware,
                            middlewares,
                        )
                    )
                else:
                    raise Exception("Le middleware \"{middleware}\" est inexistant dans le module \"{name}\"".format(
                        name = moduleName,
                        middleware = notFoundMiddlewares[0],
                    ))

            return middlewares
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES MIDDLEWARES DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

    def getMaintenanceConf(self,):
        defaultVal = False
        MainConf = self.getModuleProperties(moduleName='init')
        if MainConf is not None:
            maintenanceState = MainConf['DEFAULT']['maintenance'] if(
                type(MainConf) == dict and
                'DEFAULT' in MainConf.keys() and
                'maintenance' in MainConf['DEFAULT']
            ) else defaultVal
            
            return {
                'maintenance': convertToBoolean(maintenanceState),
            }
        return {
            'maintenance': defaultVal,
        }

    def getGenConf(self, genModulename: str = 'gen'):
        try:
            genModulename = genModulename if type(genModulename) == str and len(genModulename) > 0 else 'gen'
            genModuleFolderContent: str = 'gen-files'
            genModuleFolderContentStorage: str = 'datas'
            genModuleDoor: str = 'gen-file.xml'
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getGenConf - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            genConf = []
            for index, (key, conf) in enumerate(allConf.items()):
                if(
                    "GEN-CONF" in conf and
                    "gen-files" in conf["GEN-CONF"] and
                    (
                        (
                            type(conf["GEN-CONF"]["gen-files"]) == str and
                            len(conf["GEN-CONF"]["gen-files"]) > 0
                        ) or type(conf["GEN-CONF"]["gen-files"]) in (list, tuple)
                    )
                ):
                    genFiles = conf["GEN-CONF"]["gen-files"] if type(conf["GEN-CONF"]["gen-files"]) in (list, tuple) else [ conf["GEN-CONF"]["gen-files"] ]
                    genFiles = list(
                        filter(
                            lambda x: (
                                type(x) == str and
                                len(x) > 0 and
                                os.path.isdir(createDir(
                                    key,
                                    genModuleFolderContent,
                                    x,
                                )) and
                                Path(createDir(
                                    key,
                                    genModuleFolderContent,
                                    x,
                                    genModuleDoor,
                                )).exists()
                            ),
                            genFiles,
                        )
                    )
                    genFilesContent = []
                    for indexGF, valGF in enumerate(deepcopy(genFiles)):
                        valGFFinal = XMLFile().read(path = createDir(
                            key,
                            genModuleFolderContent,
                            deepcopy(valGF),
                            genModuleDoor,
                        ))
                        if (
                            type(valGFFinal) == dict and
                            len(valGFFinal.keys()) == 1 and
                            type(list(valGFFinal.values())[0]) == dict
                        ):
                            valGFFinal = deepcopy(list(valGFFinal.values())[0])
                            valGFFinal['module'] = deepcopy(key)
                            valGFFinal['name'] = deepcopy(valGF)
                            valGFFinal['label'] = '{module}.{name}'.format(
                                module = deepcopy(key),
                                name = deepcopy(valGF),
                            )
                            # genModuleFolderContentStorage
                            # print("> hivipy.hivi_init.py | getGenConf - createDir(valGFFinal['dest']):: ", createDir(valGFFinal['dest']))
                            if(
                                not(
                                    'dest' in valGFFinal.keys() and
                                    type(valGFFinal['dest']) == str and
                                    len(valGFFinal['dest']) > 0 and
                                    os.path.isdir(createDir(valGFFinal['dest']))
                                )
                            ):
                                valGFFinal['dest'] = '/'
                            valGFFinal['dest-f'] = createDir(valGFFinal['dest'])
                            if(
                                (
                                    'script' in valGFFinal.keys() and
                                    Path(createDir(
                                        deepcopy(key),
                                        genModuleFolderContent,
                                        deepcopy(valGF),
                                        deepcopy(valGFFinal['script']) + '.py',
                                    )).exists()
                                ) and (
                                    'nodes' in valGFFinal.keys() and
                                    type(valGFFinal['nodes']) == dict and
                                    len(valGFFinal['nodes'].keys()) > 0
                                )
                            ):
                                valGFFinal['module-path'] = deepcopy(valGFFinal['module']) + '.' + 'gen-files' + '.' + deepcopy(valGFFinal['name']) + '.' + deepcopy(valGFFinal['script'])
                                genFilesContent.append(deepcopy(valGFFinal))

                    # print("> hivipy.hivi_init.py | getGenConf - genFilesContent:: ", genFilesContent)
                    finalGF = deepcopy(genFilesContent)

                    lastGenConf = deepcopy(genConf)
                    genConf = lastGenConf + finalGF

            res = genConf
            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT gen D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getMigrationsConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getMigrationsConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            migrationConf = {}
            for index, (key, conf) in enumerate(allConf.items()):
                if(
                    "DEFAULT" in conf and
                    "migration" in conf["DEFAULT"] and
                    type(conf["DEFAULT"]["migration"]) == str and
                    len(conf["DEFAULT"]["migration"]) > 0 and
                    Path(createDir(
                        key,
                        (conf["DEFAULT"]["migration"] if "migration" in conf["DEFAULT"].keys() else "migrations").replace('.', '/') + ".py"
                    )).exists()
                ):
                    mgrtnCnf = (conf["DEFAULT"]["migration"] if "migration" in conf["DEFAULT"].keys() else "migrations")
                    mgrtnCnf_url = createDir(
                        key,
                        mgrtnCnf.replace('.', '/') + ".py"
                    )
                    mgrtnCnf_src = '{module}.{migration}'.format(
                        module=key,
                        migration=mgrtnCnf,
                    )
                    migrationConf[key] = {
                        'module': key,
                        'src': mgrtnCnf_src,
                    }
                    # print("> hivipy.hivi_init.py | getMigrationsConfig - migrationConf['", key, "']:: ", migrationConf[key])
                    migrationConf[key] = __import__(
                        migrationConf[key]['src'],
                        globals(),
                        locals(),
                        ['*'],
                    )
            res = migrationConf
            # print("> hivipy.hivi_init.py | getMigrationsConfig - migrationConf:: ", migrationConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT migration D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getMigrationsViewConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getMigrationsConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            # print("> hivipy.hivi_init.py | getMigrationsConfig -> allConf:: ", allConf)
            migrationViewConf = {}
            for index, (key, conf) in enumerate(allConf.items()):
                # print("> hivipy.hivi_init.py | getMigrationsConfig -> index:: ", index, " - conf:: ", conf)
                if(
                    "DEFAULT" in conf and
                    "migration_view" in conf["DEFAULT"] and
                    type(conf["DEFAULT"]["migration_view"]) == str and
                    len(conf["DEFAULT"]["migration_view"]) > 0 and
                    Path(createDir(
                        key,
                        (conf["DEFAULT"]["migration_view"] if "migration_view" in conf["DEFAULT"].keys() else "migrations_view").replace('.', '/') + ".py"
                    )).exists()
                ):
                    mgrtnCnf = (conf["DEFAULT"]["migration_view"] if "migration_view" in conf["DEFAULT"].keys() else "migrations_view")
                    
                    mgrtnCnf_url = createDir(
                        key,
                        mgrtnCnf.replace('.', '/') + ".py"
                    )
                    mgrtnCnf_src = '{module}.{migration}'.format(
                        module=key,
                        migration=mgrtnCnf,
                    )
                    migrationViewConf[key] = {
                        'module': key,
                        'src': mgrtnCnf_src,
                    }
                    # print("> hivipy.hivi_init.py | getMigrationsConfig - migrationViewConf['", key, "']:: ", migrationViewConf[key])
                    migrationViewConf[key] = __import__(
                        migrationViewConf[key]['src'],
                        globals(),
                        locals(),
                        ['*'],
                    )
            res = migrationViewConf
            # print("> hivipy.hivi_init.py | getMigrationsConfig - migrationViewConf:: ", migrationViewConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT migration D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModuleMigrationsFile(self, moduleName: str):
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsFile - moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsFile - moduleProperties:: ", moduleProperties)
            targets = [
                (moduleName + '.' + 'migration_files' + '.' + os.path.splitext(f)[0]) for f in os.listdir(
                    createDir(
                        moduleName,
                        "migration_files",
                    )
                ) if os.path.isfile(
                    createDir(
                        moduleName,
                        "migration_files",
                        f
                    )
                )
            ]
            if targets is not None:
                targets = targets if type(targets) in (list, tuple) else [targets]
            else:
                targets = []

            # return targets
            return list(
                map(
                    lambda target: __import__(
                        target,
                        globals(),
                        locals(),
                        ['*'],
                    ),
                    targets
                )
            )
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES FICHIERS DE MIGRATIONS DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModuleMigrationsViewsFile(self, moduleName: str):
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsViewsFile - moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsViewsFile - moduleProperties:: ", moduleProperties)
            targets = [
                (moduleName + '.' + 'migration_views_files' + '.' + os.path.splitext(f)[0]) for f in os.listdir(
                    createDir(
                        moduleName,
                        "migration_views_files",
                    )
                ) if os.path.isfile(
                    createDir(
                        moduleName,
                        "migration_views_files",
                        f
                    )
                )
            ]
            if targets is not None:
                targets = targets if type(targets) in (list, tuple) else [targets]
            else:
                targets = []

            return list(
                map(
                    lambda target: __import__(
                        target,
                        globals(),
                        locals(),
                        ['*'],
                    ),
                    targets
                )
            )
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES FICHIERS DE MIGRATIONS DE VIEW DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModuleMigrationsViewsFileAction(self, moduleName: str):
        try:
            moduleProperties = self.getModuleProperties(moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsViewsFileAction - moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py | getModuleMigrationsViewsFileAction - moduleProperties:: ", moduleProperties)
            targets = [
                (moduleName + '.' + 'migration_views_files_actions' + '.' + os.path.splitext(f)[0]) for f in os.listdir(
                    createDir(
                        moduleName,
                        "migration_views_files_actions",
                    )
                ) if os.path.isfile(
                    createDir(
                        moduleName,
                        "migration_views_files_actions",
                        f
                    )
                )
            ]
            if targets is not None:
                targets = targets if type(targets) in (list, tuple) else [targets]
            else:
                targets = []

            return list(
                map(
                    lambda target: __import__(
                        target,
                        globals(),
                        locals(),
                        ['*'],
                    ),
                    targets
                )
            )
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR LORS DE LA RECUPERATION DES FICHIERS DE MIGRATIONS ACTION DE VIEW DU MODULE \"{name}\" | err:: {err} ".format(
                name = moduleName,
                err = str(err)
            )
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getModelsConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getModelsConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            modelConf = {}
            for index, (key, conf) in enumerate(allConf.items()):
                # print("> hivipy.hivi_init.py | getModelsConfig - index:: ", index, " - conf:: ", conf)
                if(
                    "DEFAULT" in conf and
                    "model" in conf["DEFAULT"] and
                    type(conf["DEFAULT"]["model"]) == str and
                    len(conf["DEFAULT"]["model"]) > 0 and
                    Path(createDir(
                        key,
                        (conf["DEFAULT"]["model"] if "model" in conf["DEFAULT"].keys() else "models").replace('.', '/') + ".py"
                    )).exists()
                ):
                    modelConf[key] = {
                        'module': key,
                        'src': '{module}.{model}'.format(
                            module=key,
                            model=(conf["DEFAULT"]["model"] if "model" in conf["DEFAULT"].keys() else "models"),
                        ),
                    }
                    # print("> hivipy.hivi_init.py | getModelsConfig - index:: ", index, " - modelConf[", key, "]:: ", modelConf[key])
                    # print("> hivipy.hivi_init.py | getModelsConfig - index:: ", index, " - modelConf[", key, "]['src']:: ", modelConf[key]['src'])
                    # print("> hivipy.hivi_init.py | getModelsConfig - modelConf[", key, "]['src']:: ", modelConf[key]['src'])
                    # print("> hivipy.hivi_init.py | getModelsConfig - index:: ", index, " - self.allConf:: ", self.allConf)
                    modelConf[key] = __import__(
                        modelConf[key]['src'],
                        globals(),
                        locals(),
                        ['*'],
                    )
                    # print("> hivipy.hivi_init.py | getModelsConfig - modelConf[", key, "]:: ", modelConf[key])
                    # modelConf[key]['data'] = importlib.import_module(modelConf[key]['src'])
            res = modelConf
            # print("> hivipy.hivi_init.py | getModelsConfig - modelConf:: ", modelConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT model D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def loadJsonFile(self, filePath: str, mode: str = 'r', encoder: str = 'utf-8'):
        try:
            data = None
            mode = deepcopy(mode) if type(mode) == str and len(mode) > 0 else 'r'
            encoder = deepcopy(encoder) if type(encoder) == str and len(encoder) > 0 else 'utf-8'
            json_file = codecs.open(filePath, mode, encoder).read()
            data = json.loads(json_file) if (
                type(json_file) == str and
                len(json_file) > 0
            ) else None
            return data
        except: 
            stack = str(traceback.format_exc())
            log.error(stack)

            return None
    def getTranslations(self, lang: str = 'fr'):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getTranslations - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            # print("> hivipy.hivi_init.py | getTranslations - allConf:: ", allConf)
            translations = {}
            translationsConf = {}
            for index, (key, conf) in enumerate(allConf.items()):
                # print("> hivipy.hivi_init.py | getTranslations - index:: ", index, " - conf:: ", conf)
                filenameTranslations = (conf["DEFAULT"]["translations"] if "translations" in conf["DEFAULT"].keys() else "translations")
                # print("> hivipy.hivi_init.py | getTranslations - index:: ", index, " - filenameTranslations:: ", filenameTranslations)
                if(
                    Path(createDir(
                        key,
                        filenameTranslations + ".py"
                    )).exists()
                ):
                    translationsConf[key] = {
                        'module': key,
                        'src': '{module}.{translations}'.format(
                            module=key,
                            translations=(conf["DEFAULT"]["translations"] if "translations" in conf["DEFAULT"].keys() else "translations"),
                        ),
                    }
                    # print("> hivipy.hivi_init.py | getTranslations - index:: ", index, " - translationsConf[", key, "]:: ", translationsConf[key])
                    # print("> hivipy.hivi_init.py | getTranslations - index:: ", index, " - translationsConf[", key, "]['src']:: ", translationsConf[key]['src'])
                    # print("> hivipy.hivi_init.py | getTranslations - translationsConf[", key, "]['src']:: ", translationsConf[key]['src'])
                    # print("> hivipy.hivi_init.py | getTranslations - index:: ", index, " - self.allConf:: ", self.allConf)
                    translationsConf[key] = __import__(
                        translationsConf[key]['src'],
                        globals(),
                        locals(),
                        ['*'],
                    )
                    subTranslations = translationsConf[key].getTranslations(lang=lang)
                    if(
                        type(subTranslations) == dict and
                        len(subTranslations.keys()) > 0
                    ):
                        translations = {
                            **translations,
                            **subTranslations,
                        }
                        # print("> hivipy.hivi_init.py | getTranslations - translationsConf[", key, "]:: ", translationsConf[key])
                    # translationsConf[key]['data'] = importlib.import_module(translationsConf[key]['src'])
            # print("> hivipy.hivi_init.py | getTranslations - translationsConf:: ", translationsConf)
            # print("> hivipy.hivi_init.py | getTranslations - translations.keys():: ", translations.keys())

            return translations
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT translations D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getTestsConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getTestsConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            testsConf = []
            for index, (key, conf) in enumerate(allConf.items()):
                pathDir = conf["DEFAULT"]["tests"] if (
                    "DEFAULT" in conf and
                    "tests" in conf["DEFAULT"] and
                    type(conf["DEFAULT"]["tests"]) == str and
                    len(conf["DEFAULT"]["tests"]) > 0 and
                    os.path.isdir(
                        createDir(
                            key,
                            conf["DEFAULT"]["tests"]
                        )
                    ) == True
                ) else "tests"
                pathDirF = pathDir if os.path.isdir(createDir(key, pathDir)) else None
                if(pathDirF is not None):
                    for indexFile, file in enumerate(os.listdir(createDir(key, pathDir))):
                        ext = file.split('.')[-1] if len(file.split('.')) >= 2 else None
                        file__noext = '.'.join(file.split('.')[:-1])
                        finalDirFile = createDir(key, pathDir, file)
                        finalDirFile__modulepath = createModulePath(key, pathDir, file__noext)
                        finalDirFile__withoutext = createDir(key, pathDir, file__noext)
                        finalDirFile__exists = Path(finalDirFile).exists()
                        if(
                            finalDirFile__exists and
                            file__noext != "__pycach__" and
                            not(os.path.isdir(finalDirFile) == True) and
                            ext == "py"
                        ):
                            testsConf.append(
                                __import__(
                                    finalDirFile__modulepath,
                                    globals(),
                                    locals(),
                                    ['*'],
                                )
                            )
                        # print("> hivipy.hivi_init.py | getTestsConfig - allConf[", key, "] - files[", indexFile ,"].ext :: ", ext)
            res = testsConf
            # print("> hivipy.hivi_init.py | getTestsConfig - testsConf:: ", testsConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION TEST, ELEMENT model D'UN DES TESTS | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getUrlsConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getUrlsConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                # print("> hivipy.hivi_init.py | getUrlsConfig - self.allConf[", key, "]:: ", self.allConf[key])
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value
            urlConf = {}
            for index, (key, conf) in enumerate(allConf.items()):
                if(
                    "DEFAULT" in conf and
                    "url" in conf["DEFAULT"] and
                    type(conf["DEFAULT"]["url"]) == str and
                    len(conf["DEFAULT"]["url"]) > 0 and
                    Path(createDir(
                        key,
                        "__entry__".replace('.', '/') + ".py"
                    )).exists()
                ):
                    urlConf[key] = {
                        'module': key,
                        'url': conf["DEFAULT"]["url"],
                        'urlname': conf["DEFAULT"]["urlname"] if "urlname" in conf["DEFAULT"].keys() else "__entry__",
                    }
                    urlConf[key]["src"] = __import__(
                        (key + '.' + '__entry__'),
                        globals(),
                        locals(),
                        ['*'],
                    )
            res = list(urlConf.values())
            # print("> hivipy.hivi_init.py | getUrlsConfig - urlConf:: ", urlConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT url ou urlname D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getCommunicationConfig(self,):
        try:
            communicationConf = (self.getAppModuleProperties())["init"]['COMMUNICATION']

            return {
                'mail': {
                    'server': (communicationConf['mail_server'] if('mail_server' in communicationConf.keys()) else 'localhost'),
                    'port': (communicationConf['mail_port'] if('mail_port' in communicationConf.keys()) else 25),
                    'useTLS': (communicationConf['mail_use_tls'] if('mail_use_tls' in communicationConf.keys()) else True),
                    'useSSL': (communicationConf['mail_use_ssl'] if('mail_use_ssl' in communicationConf.keys()) else False),
                    'debug': (communicationConf['mail_debug'] if('mail_debug' in communicationConf.keys()) else "app.debug"),
                    'username': (communicationConf['mail_username'] if('mail_username' in communicationConf.keys()) else None),
                    'password': (communicationConf['mail_password'] if('mail_password' in communicationConf.keys()) else None),
                    'defaultSender': (communicationConf['mail_default_sender'] if('mail_default_sender' in communicationConf.keys()) else None),
                    'maxEmails': (communicationConf['mail_max_emails'] if('mail_max_emails' in communicationConf.keys()) else None),
                    'suppressSend': (communicationConf['mail_suppress_send'] if('mail_suppress_send' in communicationConf.keys()) else "app.testing"),
                    'ASCIIAttachments': (communicationConf['mail_ascii_attachments'] if('mail_ascii_attachments' in communicationConf.keys()) else False),
                },
                'twilio': (communicationConf['TWILIO'] if('TWILIO' in communicationConf.keys()) else None),
            }
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LE hiviconfig.ini concernant la section COMMUNICATION | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getDatabaseConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            databaseConf = self.allConf["init"]['DATABASE'] if (
                type(self.allConf) == dict and
                'init' in self.allConf.keys() and
                type(self.allConf['init']) == dict and
                'DATABASE' in self.allConf['init'].keys() and
                type(self.allConf["init"]['DATABASE']) == dict
            ) else {}
            dialect = databaseConf['dialect'] if('dialect' in databaseConf.keys()) else None
            dbType = None
            if dialect in ('mysql', 'postgres', 'oracle', 'sqlite', 'mssql'):
                dbType = 'sql'
            elif dialect == 'mongodb' :
                dbType = 'nosql'
            elif dialect == 'tinydb' :
                dbType = 'memorydb'
            # print("> hivipy.hivi_init.py - getDatabaseConfig | dialect:: ", dialect)
            # print("> hivipy.hivi_init.py - getDatabaseConfig | dbType:: ", dbType)
            # print("> hivipy.hivi_init.py - getDatabaseConfig | PROJECT_DIR:: ", PROJECT_DIR)
            name = databaseConf['name'] if('name' in databaseConf.keys()) else None
            host = databaseConf['host'] if('host' in databaseConf.keys()) else None
            port = databaseConf['port'] if('port' in databaseConf.keys()) else None
            user = databaseConf['user'] if('user' in databaseConf.keys()) else None
            password = databaseConf['password'] if('password' in databaseConf.keys()) else None
            if(dbType == 'sql' and dialect != 'sqlite'):
                return {
                    'dialect': dialect,
                    'dbtype': dbType,
                    'name': name,
                    'host': host,
                    'port': port,
                    'user': user,
                    'password': password,
                }
            elif(dbType == 'sql' and dialect == 'sqlite'):
                return {
                    'dialect': dialect,
                    'dbtype': dbType,
                    'name': createDir(name),
                    'host': None,
                    'port': None,
                    'user': None,
                    'password': None,
                }
            elif(dbType == 'nosql' and dialect == 'mongodb'):
                return {
                    'dialect': dialect,
                    'dbtype': dbType,
                    'name': name,
                    'host': host,
                    'port': port,
                    'user': None,
                    'password': None,
                }
            elif(dbType == 'memorydb' and dialect == 'tinydb'):
                return {
                    'dialect': dialect,
                    'dbtype': dbType,
                    'name': PROJECT_DIR / name,
                    'host': None,
                    'port': None,
                    'user': None,
                    'password': None,
                }
            else:
                raise Exception("dialect inexistant")
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LE hiviconfig.ini concernant la section DATABASE | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getSecurityConfig(self,):
        try:
            securityConf = (self.getAppModuleProperties())["init"]['SECURITY']
            keysecret = securityConf['keysecret'] if('keysecret' in securityConf.keys()) else None
            fsalt = securityConf['fsalt'] if('fsalt' in securityConf.keys()) else None
            ipaddresswhitelist = securityConf['ipaddresswhitelist'] if('ipaddresswhitelist' in securityConf.keys()) else None
            if ipaddresswhitelist is not None:
                ipaddresswhitelist = ipaddresswhitelist if type(ipaddresswhitelist) in (list, tuple) else [ipaddresswhitelist]
            blockedcidr = securityConf['blockedcidr'] if('blockedcidr' in securityConf.keys()) else None
            if blockedcidr is not None:
                blockedcidr = blockedcidr if type(blockedcidr) in (list, tuple) else [blockedcidr]
            limiter = securityConf['limiter'] if('limiter' in securityConf.keys()) else None
            if limiter is not None:
                limiter = limiter if type(limiter) in (list, tuple) else [limiter]

            return {
                'keysecret': keysecret,
                'fsalt': fsalt,
                'ipaddresswhitelist': ipaddresswhitelist,
                'blockedcidr': blockedcidr,
                'limiter': limiter,
            }
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LE hiviconfig.ini concernant la section SECURITY | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getStructConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            host = self.allConf['init']['DEFAULT']['host'].replace(' ', '') if(
                type(self.allConf) == dict and
                'init' in self.allConf.keys() and
                'DEFAULT' in self.allConf['init'].keys() and
                'host' in self.allConf['init']['DEFAULT'] and
                self.allConf['init']['DEFAULT']['host'] is not None and
                type(self.allConf['init']['DEFAULT']['host']) == str and
                len(self.allConf['init']['DEFAULT']['host'].replace(' ', '')) > 0
            ) else '0.0.0.0'
            port = self.allConf['init']['DEFAULT']['port'] if(
                type(self.allConf) == dict and
                'init' in self.allConf.keys() and
                'DEFAULT' in self.allConf['init'].keys() and
                'port' in self.allConf['init']['DEFAULT']
            ) else 8000
            return {
                'templateFolder': self.allConf['init']['DEFAULT']['template_folder'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    'init' in self.allConf.keys() and
                    'DEFAULT' in self.allConf['init'].keys() and
                    'template_folder' in self.allConf['init']['DEFAULT'] and
                    self.allConf['init']['DEFAULT']['template_folder'] is not None and
                    type(self.allConf['init']['DEFAULT']['template_folder']) == str and
                    len(self.allConf['init']['DEFAULT']['template_folder'].replace(' ', '')) > 0
                ) else 'main/templates',
                'staticFolder': self.allConf['init']['DEFAULT']['static_folder'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    'init' in self.allConf.keys() and
                    'DEFAULT' in self.allConf['init'].keys() and
                    'static_folder' in self.allConf['init']['DEFAULT'] and
                    self.allConf['init']['DEFAULT']['static_folder'] is not None and
                    type(self.allConf['init']['DEFAULT']['static_folder']) == str and
                    len(self.allConf['init']['DEFAULT']['static_folder'].replace(' ', '')) > 0
                ) else 'main/static',
                'staticModelFolder': self.allConf['init']['DEFAULT']['static_model_folder'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    'init' in self.allConf.keys() and
                    'DEFAULT' in self.allConf['init'].keys() and
                    'static_model_folder' in self.allConf['init']['DEFAULT'] and
                    self.allConf['init']['DEFAULT']['static_model_folder'] is not None and
                    type(self.allConf['init']['DEFAULT']['static_model_folder']) == str and
                    len(self.allConf['init']['DEFAULT']['static_model_folder'].replace(' ', '')) > 0
                ) else 'main/models',
                'staticUrlPath': self.allConf['init']['DEFAULT']['static_url_path'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    'init' in self.allConf.keys() and
                    'DEFAULT' in self.allConf['init'].keys() and
                    'static_url_path' in self.allConf['init']['DEFAULT'] and
                    self.allConf['init']['DEFAULT']['static_url_path'] is not None and
                    type(self.allConf['init']['DEFAULT']['static_url_path']) == str and
                    len(self.allConf['init']['DEFAULT']['static_url_path'].replace(' ', '')) > 0
                ) else '/public',
                'host': host,
                'port': port,
                'baseUrl': "http://{host}:{port}".format(host = host, port = port),
                'debug': convertToBoolean(self.allConf['init']['DEFAULT']['debug']) if(
                    type(self.allConf) == dict and
                    'init' in self.allConf.keys() and
                    'DEFAULT' in self.allConf['init'].keys() and
                    'debug' in self.allConf['init']['DEFAULT']
                ) else False,
            }
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LE hiviconfig.ini concernant la struct config | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getAssetStructModulesConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py | getAssetStructModulesConfig - self.allConf:: ", self.allConf)
            allConf = {}
            for key in self.allConf:
                value = self.allConf[key]
                if(key != 'init'):
                    allConf[key] = value

            def getAssetStructModuleConfig(confName: str):
                moduleName: str = 'main' if confName == 'init' else confName
                templateFolder = self.allConf[confName]['DEFAULT']['template_folder'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    confName in self.allConf.keys() and
                    'DEFAULT' in self.allConf[confName].keys() and
                    'template_folder' in self.allConf[confName]['DEFAULT'] and
                    self.allConf[confName]['DEFAULT']['template_folder'] is not None and
                    type(self.allConf[confName]['DEFAULT']['template_folder']) == str and
                    len(self.allConf[confName]['DEFAULT']['template_folder'].replace(' ', '')) > 0
                ) else ('/templates' if confName == 'init' else './templates')
                if (
                    os.path.isdir(
                        createDir(
                            moduleName,
                            templateFolder
                        )
                    ) == True
                ):
                    if confName == 'init':
                        templateFolder = moduleName + '/' + templateFolder
                else:
                    templateFolder = None

                staticFolder = self.allConf[confName]['DEFAULT']['static_folder'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    confName in self.allConf.keys() and
                    'DEFAULT' in self.allConf[confName].keys() and
                    'static_folder' in self.allConf[confName]['DEFAULT'] and
                    self.allConf[confName]['DEFAULT']['static_folder'] is not None and
                    type(self.allConf[confName]['DEFAULT']['static_folder']) == str and
                    len(self.allConf[confName]['DEFAULT']['static_folder'].replace(' ', '')) > 0
                ) else ('/static' if confName == 'init' else './static')
                staticUrlPath = self.allConf[confName]['DEFAULT']['static_url_path'].replace(' ', '') if(
                    type(self.allConf) == dict and
                    confName in self.allConf.keys() and
                    'DEFAULT' in self.allConf[confName].keys() and
                    'static_url_path' in self.allConf[confName]['DEFAULT'] and
                    self.allConf[confName]['DEFAULT']['static_url_path'] is not None and
                    type(self.allConf[confName]['DEFAULT']['static_url_path']) == str and
                    len(self.allConf[confName]['DEFAULT']['static_url_path'].replace(' ', '')) > 0
                ) else '/public'
                if (
                    os.path.isdir(
                        createDir(
                            moduleName,
                            staticFolder
                        )
                    ) == True
                ):
                    if confName == 'init':
                        staticFolder = moduleName + '/' + staticFolder
                else:
                    staticFolder = None
                    staticUrlPath = None
                
                return {
                    'templateFolder': templateFolder,
                    'staticFolder': staticFolder,
                    'staticUrlPath': staticUrlPath,
                }
            
            res = {}
            for index, (key, conf) in enumerate(allConf.items()):
                res[key] = getAssetStructModuleConfig(confName=key)
            # print("> hivipy.hivi_init.py | getAssetStructModulesConfig - structModuleConf:: ", structModuleConf)

            return res
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LA SECTION MODULE, ELEMENT template_folder, static_folder, static_url_path D'UN DES MODULES | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getAssetStructModuleConfig(self, name: str):
        datas = self.getAssetStructModulesConfig()
        # print("> hivipy.hivi_init.py | getAssetStructModuleConfig - datas:: ", datas)
        datas = datas if type(datas) == dict else {}

        return datas[name] if name in datas.keys() else {
            'templateFolder': None,
            'staticFolder': None,
            'staticUrlPath': None,
        }
    def getOSConfig(self,):
        try:
            self.allConf = self.getAppModuleProperties()
            # print("> hivipy.hivi_init.py - self.allConf['init']:: ", self.allConf['init'])
            return self.allConf['init']['DEFAULT']['os'] if(
                type(self.allConf) == dict and
                'init' in self.allConf.keys() and
                'DEFAULT' in self.allConf['init'].keys() and
                'os' in self.allConf['init']['DEFAULT'] and
                type(self.allConf['init']['DEFAULT']['os']) == dict
            ) else None
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | ERREUR DE CONFIGURATION DANS LE hiviconfig.ini concernant os config | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def getProperties(self,**modules: dict):
        modulesConfig = {
            'init': self.defaultPropertiesFile,
        }
        if(modules is not None):
            modulesConfig.update(modules)
        # print("> hivipy.hivi_init.py | getProperties - modules:: ", modules)
        # print("> hivipy.hivi_init.py | getProperties - modulesConfig:: ", modulesConfig)
        res = {}
        for index, (key, value) in enumerate(modulesConfig.items()):
            res[key] = self.getPropertiesModule(value)
        return res
    def getPropertiesModule(self, moduleName: str = None, isAbsoluteUrl: bool = False):
        try:
            initialModuleName = deepcopy(moduleName)
            isAbsoluteUrl = isAbsoluteUrl if type(isAbsoluteUrl) == bool else False
            partFilename = deepcopy(moduleName) if(
                type(moduleName) == str and
                len(moduleName) > 0
            ) else self.defaultPropertiesFile
            fileName = partFilename
            if not(isAbsoluteUrl == True) :
                if(
                    Path(createDir(
                        moduleName,
                        "conf".replace('.', '/') + ".xml"
                    )).exists()
                ) :
                    fileName = createDir(
                        moduleName,
                        "conf".replace('.', '/') + ".xml"
                    )
                elif (
                    moduleName == 'init' and
                    Path(createDir(self.defaultPropertiesFile)).exists()
                ) :
                    fileName = createDir(self.defaultPropertiesFile)
            res = XMLFile().read(path = fileName, mode = "r", encoding = "utf-8")
            if type(res) == dict and moduleName in ('init', 'main/hiviconfig.xml'):
                res['init']['DEFAULT']['os'] = {
                    '_os': os.name,
                    'os': platform.system(),
                    'release': platform.release(),
                }

            # print("> hivipy.hivi_init.py - getPropertiesModule | moduleName:: ", moduleName)
            # print("> hivipy.hivi_init.py - getPropertiesModule | res:: ", res)

            resF = self.loopObject(
                data = res,
                map = (lambda index, key, element, data: self.ConvertStringToInitialType(strValue = element) if type(element) == str else element),
            ) if type(res) == dict or type(res) is OrderedDict or type(res) is collections.OrderedDict else {}
            # print("> hivipy.hivi_init.py - getPropertiesModule | resF:: ", resF)
            resFi = list(resF.values())[0] if type(resF) == dict and len(resF.values()) > 0 else None
            return resFi
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
    def setPropertyModule(self, module: str, value):
        res = 0
        try:
            module = module if type(module) == str and len(module) > 0 else None
            
            urlPathConf = self.getAppModuleUrlConfPath()[module]

            lastConf = self.getPropertiesModule(moduleName=urlPathConf, isAbsoluteUrl=True)
            lastConf = list(lastConf.values())[0] if type(lastConf) == dict and len(lastConf.values()) > 0 else {}
            # print("> hivipy.hivi_init.py | setPropertyModule - lastConf:: ", lastConf)

            newElement = deepcopy(value)
            conf = {
                module: self.ElementForUpdate(
                    oldElement=lastConf,
                    newElement=newElement,
                    strictColumns=False
                ),
            }
            # print("> hivipy.hivi_init.py | setPropertyModule - conf:: ", conf)
            # print("> hivipy.hivi_init.py | setPropertyModule - value:: ", value)
            # print("> hivipy.hivi_init.py | setPropertyModule - newElement:: ", newElement)

            # print("> hivipy.hivi_init.py | setPropertyModule - urlPathConf:: ", urlPathConf)
            # print("> hivipy.hivi_init.py | setPropertyModule - conf (old):: ", conf)
            # print("> hivipy.hivi_init.py | setPropertyModule - session:: ", session)
            # print("> hivipy.hivi_init.py | setPropertyModule - (session in conf):: ", (session in conf))
            # print("> hivipy.hivi_init.py | setPropertyModule - name:: ", name)

            outWrite = XMLFile().write(path=urlPathConf, datas = conf, mode = 'wb', encoding = 'utf-8')
            res = 1 if outWrite == True else 2
                
            # print("> hivipy.hivi_init.py | setPropertyModule - dict(conf):: ", dict(conf))
        except Exception as err:
            e = "[ERROR] hivipy.hivi_init.py | err:: {err} ".format(err = str(err))
            # print(e)
            stack = str(traceback.format_exc())
            log.error(stack)
            res =  0

        return res


    def ConvertStringToInitialType(self, strValue: str):
        if type(strValue) == str :
            if self.isObject(strValue) == True :
                return json.load(strValue)
            elif self.isDate(value = strValue, dateFormat = dateFormat1) == True:
                return self.getDate(value = strValue, dateFormat = dateFormat1)
            elif self.isNumber(value = strValue) :
                if strValue.isdigit():
                    return int(strValue)
                else:
                    return float(strValue)
            elif self.isBoolean(value = strValue) :
                return float(strValue)
            return strValue
        return strValue
    def isObject(self,
        value: str,
    ):
        res = False
        try:
            if type(value) == dict :
                res = True
            else:
                json.load(value)
                res = True
        except Exception as err:
            res = False
        return res
    def isDatetimeFormat(
        self,
        value: str,
        format: str,
    ):
        res = False
        try:
            datetime.strptime(value, format)
            res = True
        except Exception as err:
            res = False
        return res
    def getDate(
        self,
        value: any,
        dateFormat: str = None,
        timezone = None,
        typeValue = None,
    ):
        res = None
        typesPossible = ('datetime', 'date', 'time')
        typeValue = typeValue if typeValue in typesPossible else None
        timezone = timezone if timezone is not None else None
        dateFormat = dateFormat if (
            type(dateFormat) == str and
            len(dateFormat) > 0
        ) else None

        if(
            type(value) == str and
            len(value) > 0 and
            dateFormat is not None and
            self.isDatetimeFormat(value, format = dateFormat)
        ):
            res = datetime.strptime(value, dateFormat)
            if(timezone is not None):
                res = res.astimezone(timezone)
            if(typeValue == 'date'):
                res = res.date()
            if(typeValue == 'time'):
                res = res.time()
        if(
            type(value) is datetime or
            type(value) is datetime.date or
            type(value) is datetime.time
        ):
            res = value
            if(
                type(value) is datetime and
                timezone is not None
            ):
                res = res.astimezone(timezone)

        return res
    def isDate(
        self,
        value: any,
        typeValue: str = None,
        dateFormat: str = None,
    ) -> bool:
        dateFormat = dateFormat if (
            type(dateFormat) == str and
            len(dateFormat) > 0
        ) else None
        types: tuple = ('datetime', 'date', 'time', 'null', 'string')
        typeValue = typeValue if typeValue in types else None

        if (
            typeValue == "string" and
            type(value) == str and
            len(value) > 0 and
            dateFormat is not None
        ) :
            return (
                self.isDatetimeFormat(value, format = dateFormat) or
                value is None
            )
        else :
            res = (
                ( type(value) is datetime and ( typeValue in (None, 'datetime') ) ) or
                ( type(value) is datetime.time and ( typeValue in (None, 'time') ) ) or
                ( type(value) is datetime.date and ( typeValue in (None, 'date') ) ) or
                ( type(value) == str and len(value) > 0 and self.isDatetimeFormat(value, format = dateFormat) and ( typeValue in (None, 'string') ) ) or
                ( type(value) is None and ( typeValue in (None, 'null') ) )
            )
            return res
    def isString(
        self,
        value: any,
        typeValue: str = None,
    ) -> bool:
        types: tuple = ('datetime', 'date', 'time', 'null', 'other')
        typeValue = typeValue if typeValue in types else None
        res = (
            (
                value is None or (
                    type(value) in (str, int, float, bool, list, tuple, dict) and (
                        typeValue is None or
                        typeValue == 'other'
                    )
                )
            ) or 
            (
                value is None or (
                    type(value) is datetime and (
                        typeValue is None or
                        typeValue == 'datetime'
                    )
                )
            ) or
            (
                value is None or (
                    type(value) is datetime.time and (
                        typeValue is None or
                        typeValue == 'time'
                    )
                )
            ) or
            (
                value is None or (
                    type(value) is datetime.date and (
                        typeValue is None or
                        typeValue == 'date'
                    )
                )
            ) or
            (
                value is None or (
                    type(value) is None and (
                        typeValue is None or
                        typeValue == 'null'
                    )
                )
            )
        )
        return res
    def isNumber(self, value: any) -> bool:
        res = True
        try:
            if(value is not None):
                float(value)
        except:
            res = False
        res = (
            (res == True and type(value) in [str, int, float]) or
            value is None
        )
        return res
    def isBoolean(
        self,
        value: any,
        valuesPossibles: list = None,
        strict: bool = False
    ) -> bool:
        valuesPossibles = valuesPossibles if type(valuesPossibles) in (list, tuple) else []
        res = (
            (
                value in valuesPossibles or
                (
                    type(value) == str and
                    value.lower() in valuesPossibles
                )
            ) or
            (value is None and strict == False)
        )
        return res
    def isFile(self, value: any) -> bool:
        res = (type(value) is FileStorage)
        return res
    def loopObject(
        self,
        data: dict,
        map = lambda index, key, element, data: element
    ):
        map = map if callable(map) else (lambda index, key, element, data: element)
        if type(data) is OrderedDict or type(data) is collections.OrderedDict:
            data = dict(deepcopy(data))
        if type(data) == dict:
            data = deepcopy(dict(data))
            for index, (key, element) in enumerate(data.items()):
                data[key] = map(index=index, key=key, element=element, data=data)
                data[key] = self.loopObject(data=data[key], map=map)
        elif type(data) in (list, tuple):
            data = deepcopy(list(data))
            for index, element in enumerate(data):
                data[index] = map(index=index, key=index, element=element, data=data)
                data[index] = self.loopObject(data=data[index], map=map)
        return data
    def ElementForUpdate(
        self,
        oldElement: any,
        newElement: any,
        nullableAttributes: list = [],
        strictColumns: bool = True
    ):
        strictColumns = strictColumns if type(strictColumns) == bool else True
        nullableAttributes = list(
            filter(
                lambda x: type(x) == str and len(x) > 0,
                nullableAttributes,
            ),
        ) if type(nullableAttributes) in (list, tuple) else []
        oldElement = oldElement if type(oldElement) == dict else {}
        newElement = newElement if type(newElement) == dict else {}

        newElementClone = {}
        for index, key in enumerate(newElement):
            value = newElement[key]
            if(value is None and key in nullableAttributes):
                newElementClone[key] = None
            elif(value is not None):
                newElementClone[key] = value
        newElement = newElementClone
        oldElementClone = {}
        for index, key in enumerate(oldElement):
            value = oldElement[key]
            if(value is None and key in nullableAttributes):
                oldElementClone[key] = None
            elif(value is not None):
                oldElementClone[key] = value
        oldElement = oldElementClone

        if(strictColumns == True):
            oldElementClone = {}
            for index, key in enumerate(oldElement):
                value = oldElement[key]
                if(key in newElement.keys()):
                    oldElementClone[key] = value
            oldElement = oldElementClone
        res = {}
        for index, key in enumerate(oldElement):
            value = oldElement[key]
            finalValue = None
            if(
                (
                    not(key in nullableAttributes) and
                    (
                        value or
                        type(value) == bool or
                        value is None
                    ) and
                    (
                        key in newElement.keys() and (
                            newElement[key] or
                            type(newElement[key]) == bool or
                            newElement[key] is None
                        )
                    )
                )
            ):
                if(
                    type(newElement[key]) in (int, float, str, bool) or
                    type(newElement[key]) is FileStorage or
                    type(newElement[key]) is datetime or
                    type(newElement[key]) is date
                ):
                    finalValue = newElement[key]
                elif(
                    type(newElement[key]) == dict and
                    type(value) == dict
                ):
                    finalValue = self.ElementForUpdate(
                        oldElement=value,
                        newElement=newElement[key],
                        nullableAttributes=nullableAttributes,
                        strictColumns=strictColumns,
                    )
                elif(
                    type(newElement[key]) in (list, tuple) and
                    type(value) in (list, tuple)
                ):
                    finalValue = newElement[key]
                else:
                    finalValue = newElement[key]
            elif(
                key in nullableAttributes and
                value is None and
                newElement[key] is None
            ):
                finalValue = newElement[key]
            else:
                finalValue = value
            res[key] = finalValue
        return res

# print("---> ICI - HIVI_INIT <---")

manager = Manager()
# translations = manager.getTranslations(lang = 'en')
# print("> hivipy.hivi_init.py - translations:: ", translations)

# allMigrationFiles = manager.getModuleMigrationsFile(moduleName='mymoduletest')
# print("> hivipy.hivi_init.py - allMigrationFiles:: ", allMigrationFiles)
# allMigrationViewFiles = manager.getModuleMigrationsViewsFile(moduleName='mymoduletest')
# print("> hivipy.hivi_init.py - allMigrationViewFiles:: ", allMigrationViewFiles)

# mainConfig = manager.getInitProperties()
# print("> hivipy.hivi_init.py - mainConfig:: ", mainConfig)
# AUTHmodulePropertiesConfig = manager.getModuleProperties(moduleName='auth')
# print("> hivipy.hivi_init.py - AUTHmodulePropertiesConfig:: ", AUTHmodulePropertiesConfig)
# AUTHmoduleServicesConfig = manager.getModuleServices(moduleName='auth')
# print("> hivipy.hivi_init.py - AUTHmoduleServicesConfig:: ", AUTHmoduleServicesConfig)
# modulesRequiredForModule = manager.getModulesRequiredForModule(moduleName='auth')
# print("> hivipy.hivi_init.py - modulesRequiredForModule:: ", modulesRequiredForModule)
# checkModulesRequiredForModule = manager.checkAllModulesRequiredForModule(moduleName='auth')
# print("> hivipy.hivi_init.py - checkModulesRequiredForModule:: ", checkModulesRequiredForModule)

# allModuleNames = manager.getAllModuleNames()
# print("> hivipy.hivi_init.py - allModuleNames:: ", allModuleNames)
# moduleNames = manager.getAppModuleNames()
# print("> hivipy.hivi_init.py - moduleNames:: ", moduleNames)
# allConfPath = manager.getAppModuleUrlConfPath()
# print("> hivipy.hivi_init.py - allConfPath:: ", allConfPath)
# initModuleProperties = manager.getPropertiesModule()
# print("> hivipy.hivi_init.py - initModuleProperties:: ", initModuleProperties)
# appModuleProperties = manager.getAppModuleProperties()
# print("> hivipy.hivi_init.py - appModuleProperties:: ", appModuleProperties)
# manager.setPropertyModule(module='init', value = {
#     "META": {
#         "author": "billy"
#     }
# })
# structConfig = manager.getStructConfig()
# print("> hivipy.hivi_init.py - structConfig:: ", structConfig)
# securityConfig = manager.getSecurityConfig()
# print("> hivipy.hivi_init.py - securityConfig:: ", securityConfig)
# databaseConfig = manager.getDatabaseConfig()
# print("> hivipy.hivi_init.py - databaseConfig:: ", databaseConfig)
# urlsConfig = manager.getUrlsConfig()
# print("> hivipy.hivi_init.py - urlsConfig:: ", urlsConfig)
# communicationConfig = manager.getCommunicationConfig()
# print("> hivipy.hivi_init.py - communicationConfig:: ", communicationConfig)
# testsConfig = manager.getTestsConfig()
# print("> hivipy.hivi_init.py - testsConfig:: ", testsConfig)
# modelsConfig = manager.getModelsConfig()
# print("> hivipy.hivi_init.py - modelsConfig:: ", modelsConfig)
# migrationsConfig = manager.getMigrationsConfig()
# print("> hivipy.hivi_init.py - migrationsConfig:: ", migrationsConfig)
# migrationsViewConfig = manager.getMigrationsViewConfig()
# print("> hivipy.hivi_init.py - migrationsViewConfig:: ", migrationsViewConfig)