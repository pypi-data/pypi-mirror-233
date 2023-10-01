from copy import deepcopy
import re
import logging
import traceback


log = logging.getLogger(__name__)

def _transformStringConfToArray(initialData: str, mapAction = (lambda x: x), regExpVal = r"[^a-zA-Z0-9_,]", otherFormatters = {}):
    """ _transformStringConfToArray - Fonction de convertion d'une chaine de caractère en une liste

    Cette methode permet de convertir une chaîne de caracteres en liste

    Parameters
    ------------
        initialData: str
            le chaine de caractère qui sera converti en liste
        mapAction: def
            la fonction de mappage après la convertion
        regExpVal: str
            l'expression regulière qui permettra de nettoyer la chaine de caractères
        otherFormatters: dict
            d'autres actions de formatage qui pouronts être appliquée
    Return
    -----------
        arrayValue : list
            La liste qui sera produit en guise de resultat. 
    """
    try:
        initialData = initialData if type(initialData) == str else None
        if(initialData is not None):
            initialFormatter = {
                'int': lambda x: int(x),
                'float': lambda x: float(x),
                'str': lambda x: str(x),
                'list': lambda x: list(x),
                'tuple': lambda x: tuple(x),
            }
            otherFormatters = otherFormatters if type(otherFormatters) == dict else {}

            for index, (key, value) in enumerate((deepcopy(otherFormatters)).items()):
                if(not(callable(value) == True)):
                    del otherFormatters[key]
            initialFormatter.update(otherFormatters)

            mapAction = mapAction if callable(mapAction) else (lambda x: x)
            regExpVal = regExpVal if type(regExpVal) == str and type(regExpVal) else r"[^a-zA-Z0-9_,]"
            
            arrayData = initialData.split(",") if type(initialData) == str and len(initialData) > 0 else []
            for index, value in enumerate(arrayData):
                cleanedVal = value.split('->')
                cleanedVal = cleanedVal[:2] if(len(cleanedVal) >= 2) else [cleanedVal[0], None]
                val = re.sub(
                    re.compile(regExpVal, re.MULTILINE),
                    "",
                    cleanedVal[0],
                )
                formatter = re.sub(
                    re.compile(regExpVal, re.MULTILINE),
                    "",
                    cleanedVal[1],
                ) if cleanedVal[1] is not None else None
                try:
                    val = initialFormatter[formatter](val) if formatter in initialFormatter.keys() else val
                except Exception as err:
                    log.error(err)
                arrayData[index] = val
            return arrayData
        else:
            return None
    except:
        stack = str(traceback.format_exc())
        
        log.error(stack)
        return None
def _transformStringConfToObject(initialData: str, mapAction = (lambda x: x), otherFormatters = {}):
    """ _transformStringConfToObject - Fonction de convertion d'une chaine de caractère en une dictionnaire

    Cette methode permet de convertir une chaîne de caracteres en dictionnaire

    Parameters
    ------------
        initialData: str
            le chaine de caractère qui sera converti en liste
        mapAction: def
            la fonction de mappage après la convertion
        otherFormatters: dict
            d'autres actions de formatage qui pouronts être appliquée
    Return
    -----------
        dictValue : list
            Le dictionnaire qui sera produit en guise de resultat. 
    """
    try:
        initialData = initialData if type(initialData) == str else None
        if(initialData is not None):
            initialFormatter = {
                'int': lambda x: int(x),
                'float': lambda x: float(x),
                'str': lambda x: str(x),
                'list': lambda x: list(x),
                'tuple': lambda x: tuple(x),
            }
            otherFormatters = otherFormatters if type(otherFormatters) == dict else {}
            mapAction = mapAction if callable(mapAction) else (lambda x: x)
            regExpVal = r"[^a-zA-Z0-9_,]"
            regExpVal2 = r"[^a-zA-Z0-9_,\>-]"
            regExpVal3 = r"[^\s\t\na-zA-Z0-9_\,\-\>]"

            for index, (key, value) in enumerate((deepcopy(otherFormatters)).items()):
                if(not(callable(value) == True)):
                    del otherFormatters[key]
            initialFormatter.update(otherFormatters)
            
            arrayData = list(initialData.split(",")) if type(initialData) == str and len(initialData) > 0 else []
            arrayData = list(
                map(
                    lambda data: data.split('='),
                    arrayData,
                ),
            )
            arrayData = list(
                filter(
                    lambda data: len(data) == 2,
                    arrayData,
                )
            )
            objectData = {}
            for index, value in enumerate(arrayData):
                key = re.sub(
                    re.compile(regExpVal, re.MULTILINE),
                    "",
                    value[0],
                )
                valNotClean = re.sub(
                    re.compile(regExpVal3, re.MULTILINE),
                    "",
                    value[1],
                )
                cleanedVal = valNotClean.split('->')
                cleanedVal = cleanedVal[:2] if(len(cleanedVal) >= 2) else [cleanedVal[0], None]
                val = re.sub(
                    re.compile(regExpVal3, re.MULTILINE),
                    "",
                    cleanedVal[0],
                )
                formatter = re.sub(
                    re.compile(regExpVal, re.MULTILINE),
                    "",
                    cleanedVal[1],
                ) if cleanedVal[1] is not None else None
                try:
                    val = initialFormatter[formatter](val) if formatter in initialFormatter.keys() else val
                except Exception as err:
                    log.error(err)
                objectData[key] = val

            res = objectData
            return res
        else:
            return None
    except:
        stack = str(traceback.format_exc())
        
        log.error(stack)
        return None