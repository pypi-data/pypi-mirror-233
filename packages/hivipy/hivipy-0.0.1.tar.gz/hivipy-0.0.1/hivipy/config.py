from typing import *

eseDatas = {
    'name': 'Company Name',
    'datas': [
        'BP.292 Douala',
        'CAMEROUN',
        '+237697545963',
        'contact@email.com',
    ]
}

encoder = "UTF-8"

statusInitial = ['visible', 'archived']
status = statusInitial + ['blocked']
canals = ['mail', 'sms']
langs = ['en', 'fr']
langCodes = {
    'fr': 'fr_FR',
    'en': 'en_US',
}
levelsLang = [ "intermediate" , "pre_intermediate" , "current" , "elementary" ]

certificationTypes = [ "classic", "bronze", "silver", "gold" ]

requestUpdateTypes = [ "security_data", "password" ]

exportTypes = [ 'csv', 'excel', 'pdf', 'json' ]

socialNetworks = [ "google", "facebook", "twitter","apple"]

weekDays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

dateTimeFormatInitial = '%Y-%m-%dT%H:%M:%S.%fZ'
dateFormatInitial = '%Y-%m-%d'
timeFormatInitial = '%H:%M:%S.%fZ'

dateFormatForFile = '%Y%m%d%H%M%S'
dateFormat1 = '%Y/%m/%d %H:%M:%S.%fZ'
dateFormat2 = '%Y/%m/%d %H:%M:%S'
dateFormat3 = '%Y/%m/%d %H:%M'
dateFormat4 = '%d/%m/%Y %H:%M:%S GMT%z'
dateFormat5 = '%Y/%m/%d'
timeFormat1 = '%H:%M:%S.%fZ'
timeFormat2 = '%H:%M:%S'
pagesPossibles = [ 5, 10, 15, 25, 50, 100, -1 ]

regExpForAlphanumeric = r"^[\w\s]{1,}"

tabNumerique = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
tabNumerique = list(map(lambda x: str(x), tabNumerique))
tabAlphabetique = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
tabAlphabetique = list(map(lambda x: x.lower(), tabAlphabetique))
tabAlphabetiqueInsensitive = tabAlphabetique + list(map(lambda x: x.upper(), tabAlphabetique))
tabAlphanumerique = tabNumerique + tabAlphabetique
tabAlphanumeriqueInsensitive = tabNumerique + tabAlphabetiqueInsensitive


actionTypes = ('personal-data', 'security-data', 'password-data')


responsesPossibles = {
    "unknown_error": {
        "type": "danger",
        "code": "0001__unknown_error",
        "status": 500,
        "message": {
            "fr": "erreur interne inconnue",
            "en": "unknown internal error"
        }
    },
    "invalid_form": {
        "type": "warning",
        "code": "0002__invalid_form",
        "status": 422,
        "message": {
            "fr": "votre formulaire est invalid",
            "en": "your form is invalid"
        }
    },
    "data_exists": {
        "type": "danger",
        "code": "0003__data_exists",
        "status": 500,
        "message": {
            "fr": "la donnée existe déjà",
            "en": "the data already exists"
        }
    },
    "data_doesnt_exists": {
        "type": "danger",
        "code": "0004__data_doesnt_exists",
        "status": 500,
        "message": {
            "fr": "la donnée n'existe pas",
            "en": "the data does not exist"
        }
    },
    "fail_send_email": {
        "type": "danger",
        "code": "0005__fail_send_email",
        "status": 500,
        "message": {
            "fr": "echec lors de l'envoi du mail",
            "en": "echec lors de l'envoi du mail"
        }
    },
    "request_not_processed": {
        "type": "danger",
        "code": "0006__request_not_processed",
        "status": 500,
        "message": {
            "fr": "la demande n'a pas été traité",
            "en": "the request has not been processed"
        }
    },
    "auth_no_access": {
        "type": "danger",
        "code": "0007__auth_no_access",
        "status": 403,
        "message": {
            "fr": "accès refusée à cette ressource",
            "en": "access denied to this resource"
        }
    },
    "no_activated": {
        "type": "success",
        "code": "0008__good_action",
        "status": 403,
        "message": {
            "fr": "votre compte utilisateur n'est pas activé",
            "en": "account is not activated"
        }
    },
    "auth_no_permission": {
        "type": "danger",
        "code": "0009__auth_no_permission",
        "status": 403,
        "message": {
            "fr": "vous n'avez pas la permission necessaire pour acceder à cette ressource",
            "en": "you do not have permission to access this resource"
        }
    },
    "failure_authentication": {
        "type": "danger",
        "code": "0010__request_not_processed",
        "status": 401,
        "message": {
            "fr": "echec lors de l'authentification",
            "en": "failure during authentication"
        }
    },
    "not_found": {
        "type": "danger",
        "code": "0011__not_found",
        "status": 404,
        "message": {
            "fr": "page/ressource introuvable",
            "en": "page/resource not found"
        }
    },
    "maintenance": {
        "type": "info",
        "code": "0012__maintenance",
        "status": 501,
        "message": {
            "fr": "l'application est en maintenance",
            "en": "the app is under maintenance"
        }
    },
    "good_action": {
        "type": "success",
        "code": "0013__good_action",
        "status": 200,
        "message": {
            "fr": "action réalisée avec succès",
            "en": "action successfully completed"
        }
    },
    "good_action__0": {
        "type": "success",
        "code": "0013__good_action__0",
        "status": 200,
        "message": {
            "fr": "action réalisée avec succès",
            "en": "action successfully completed"
        }
    },
    "good_action__1": {
        "type": "success",
        "code": "0013__good_action__1",
        "status": 200,
        "message": {
            "fr": "action réalisée avec succès",
            "en": "action successfully completed"
        }
    },
    "no_network": {
        "type": "danger",
        "code": "0014__no_network",
        "status": 404,
        "message": {
            "fr": "echec de la connexion au serveur. Verifier votre connexion internet",
            "en": "Failed to connect to server. Check your internet connection"
        }
    },
    "good_conn": {
        "type": "success",
        "code": "0015__good_conn",
        "status": 200,
        "message": {
            "fr": "test de la connexion au serveur réussi avec succès",
            "en": "successful server connection test"
        }
    },
}