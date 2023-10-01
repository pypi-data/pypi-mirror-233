from . import JON
from .hivi_init import Manager
from . import schemas


manager = Manager()
structConf = manager.getStructConfig()

class StrictDict(dict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir d'un schema de contrôle JON .
    '''
    _lang = 'fr'
    _struct = None

    def __init__(self, mapping=None, /, **kwargs):
        # print('[INTERFACES] StrictDict - __init__ - ICI')
        self._struct = self.getStruct()
        super().__init__(mapping)

        self.verifyStruct()

    def __setitem__(self, key, value):
        self._struct = self.getStruct()
        super().__setitem__(key, value)

        self.verifyStruct()


    def getStruct(self,):
        '''
        Retourne le schema de contrôle JON .

            Returns:
                JON.Object: Schema JON retourné
        '''
        return JON.Object(self._lang).struct({})
    def verifyStruct(self,):
        '''
        Permet de verifier la structure du dictionnaire en fonction d'un schema de contrôle JON.

            Returns:
                None: Fonction retournée
        '''
        items = dict(self.items())
        # print('[INTERFACES] StrictDict - verifyStruct | items:: ', items)
        validateData = self._struct.validate(items)
        # print('[INTERFACES] StrictDict - verifyStruct | validateData:: ', validateData)
        error = validateData['error']
        if(error is not None):
            # print('[INTERFACES] StrictDict - verifyStruct | error:: ', error)
            # print('[INTERFACES] StrictDict - verifyStruct | type(error):: ', type(error))
            raise error


class CRUDFindAllDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDFindAllSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDFindAllSchema(self._lang)
class CRUDCountAllDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDCountAllSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDCountAllSchema(self._lang)
class CRUDFindDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDFindOneSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDFindOneSchema(self._lang)
class CRUDExistsDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDElementExistsSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDElementExistsSchema(self._lang)
class CRUDOptionDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDOptionSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDOptionSchema(self._lang)
class CRUDExecSingleDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDExecSingleSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDExecSingleSchema(self._lang)
class CRUDExecAllDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDExecAllSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDExecAllSchema(self._lang)
class CRUDExtractDatasDict(StrictDict):
    '''
    Retourne un dictionnaire qui a une structure de donnée stricte verifiée à partir du schema schemas.CRUDExtractDatasSchema .
    '''
    def getStruct(self,):
        return schemas.CRUDExtractDatasSchema(self._lang)
    

# datas: CRUDFindAllDict = CRUDFindAllDict({
#     "datas": [
#         {
#             "name": "bilong"
#         }
#     ],
#     "meta": {
#         "pagination": {
#             "page": 1,
#             "pageCount": 2,
#             "pageLength": 5,
#             "pageSize": 5,
#             "total": 10
#         }
#     },
#     "total": 10,
#     "notif": {
#         "code": "0013__good_action",
#         "message": "action réalisée avec succès",
#         "status": 200,
#         "type": "success"
#     },
# })
# if structConf['debug'] :
#     print("""[INTERFACES] datas:: """, datas)
# 
# datasTotal: CRUDCountAllDict = CRUDCountAllDict({
#     "total": 10,
#     "notif": {
#         "code": "0013__good_action",
#         "message": "action réalisée avec succès",
#         "status": 200,
#         "type": "success"
#     },
# })
# if structConf['debug'] :
#     print("""[INTERFACES] datasTotal:: """, datasTotal)
# 
# data: CRUDFindDict = CRUDFindDict({
#     "data": {
#         "_searchtype": "custom_module_collection",
#         "blocked": False,
#         "blockedat": None,
#         "createdat": "Wed, 17 May 2023 10:38:24 GMT",
#         "description": "description element 1",
#         "parent": None,
#         "size": 20.0,
#         "slug": "collection0001",
#         "stable": True,
#         "status": "visible",
#         "title": "element 1 ",
#         "updatedat": "Mon, 22 May 2023 16:00:14 GMT"
#     },
#     "exists": True,
#     "notif": {
#         "code": "0013__good_action",
#         "message": "action réalisée avec succès",
#         "status": 200,
#         "type": "success"
#     }
# })
# if structConf['debug'] :
#     print("""[INTERFACES] data:: """, data)
#     endPointRes = data, data['notif']['status']
#     print("""[INTERFACES] endPointRes:: """, endPointRes)
# data: CRUDOptionDict = CRUDOptionDict({
#     "notif": {
#         "code": "0013__good_action",
#         "message": "action réalisée avec succès",
#         "status": 200,
#         "type": "success"
#     },
#     "options": {
#         "collection": [
#             {
#                 "label": "element 1 edit 2",
#                 "value": "collection0001"
#             },
#         ]
#     },
# })
# if structConf['debug'] :
#     print("""[INTERFACES] data:: """, data)