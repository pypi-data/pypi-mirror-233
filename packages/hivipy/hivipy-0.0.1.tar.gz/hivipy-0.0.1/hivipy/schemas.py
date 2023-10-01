from . import JON
from .config import responsesPossibles
from .hivi_init import Manager


manager = Manager()
structConf = manager.getStructConfig()


def CRUDDatasSchema(lang: str, required: bool = False):
    '''
    Retourne le schema utilsé pour valider l'attribut datas qui represente l'ensembles des enregistrements retournée de type tableau de dictionnaires.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Array: Schema JON retourné
    '''
    required = required if type(required) == bool else False
    res = JON.Array(lang).types(
        JON.Object(lang).required()
    ).defaultError({
        "fr": "datas doit être de type tableau contenant uniquement des objets",
        "en": "datas doit être de type tableau contenant uniquement des objets"
    })
    if required:
        res = res.required()

    return res
def CRUDDataSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut data qui represente l'enregistrement recherché de type dictionnaire.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).defaultError({
        "fr": "data doit être un objet",
        "en": "data doit être un objet"
    })
def CRUDExistsSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut exists qui represente la valeur de verification de l'existence de la donnée.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Boolean: Schema JON retourné
    '''
    return JON.Boolean(lang)# .required()# .defaultError({
    #     "fr": "exists doit être un booleen",
    #     "en": "exists doit être un booleen"
    # })
def CRUDMetaSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut meta qui les metadonnées supplementaires lors de la recherche de tous les enresgistrements telles que la pagination.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "pagination": JON.Object(lang).struct({
            "page": JON.Number(lang).integer().required().defaultError({
                "fr": "page n'est pas de type entier",
                "en": "page n'est pas de type entier",
            }),
            "pageCount": JON.Number(lang).integer().required().defaultError({
                "fr": "pageCount n'est pas de type entier",
                "en": "pageCount n'est pas de type entier",
            }),
            "pageLength": JON.Number(lang).integer().required().defaultError({
                "fr": "pageLength n'est pas de type entier",
                "en": "pageLength n'est pas de type entier",
            }),
            "pageSize": JON.Number(lang).integer().required().defaultError({
                "fr": "pageSize n'est pas de type entier",
                "en": "pageSize n'est pas de type entier",
            }),
            "total": JON.Number(lang).integer().required().defaultError({
                "fr": "total n'est pas de type entier",
                "en": "total n'est pas de type entier",
            }),
        }).required().applyApp(
            rule=(lambda pagination: (
                (pagination["pageCount"] >= pagination["page"]) or (
                    pagination["pageCount"] == 0 and pagination["page"] == 1
                )
            )),
            exception={
                "fr": "pageCount doit toujours être superieur ou egal à page",
                "en": "pageCount doit toujours être superieur ou egal à page",
            },
        ).defaultError({
            "fr": "pagination n'est pas un objet valide",
            "en": "pagination n'est pas un objet valide"
        }),
    }).required().defaultError({
        "fr": "meta n'est pas un objet valide",
        "en": "meta n'est pas un objet valide"
    })
def CRUDMetaExtractSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut meta qui les metadonnées supplementaires lors de l'extraction de toutes les données telles que les données invalides.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "invalid-datas": JON.Array(lang).types(
            JON.Object(lang).struct({
                'index': JON.Number(lang).integer().required().defaultError({
                    "fr": "l'index des données invalides n'est pas de type entier",
                    "en": "invalid data index is not of integer type",
                }),
                'schemas': JON.Array(lang).types(
                    JON.String(lang).required().defaultError({
                        "fr": "le schema des données invalides n'est pas une chaîne de caractère",
                        "en": "invalid data schema is not a string",
                    }),
                ),
            }).required()
        ).defaultError({
            "fr": "invalide structure des données invalides",
            "en": "invalid invalid data structure"
        })
    }).required().defaultError({
        "fr": "meta n'est pas un objet valide",
        "en": "meta n'est pas un objet valide"
    })
def CRUDNotifSchema(lang: str, required: bool = False):
    '''
    Retourne le schema utilsé pour valider l'attribut notif qui represente le message retourné après une execution specifique.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    required = required if type(required) == bool else False
    res = JON.Object(lang).struct({
        "code": JON.Enum(lang).choices(*list(
            map(
                lambda response: response['code'],
                responsesPossibles.values()
            )
        )).defaultError({
            "fr": "code de la notification est invalide",
            "en": "code de la notification est invalide",
        }),
        "message": JON.String(lang).required().defaultError({
            "fr": "message de la notification n'est pas une chaîne de caractère",
            "en": "message de la notification n'est pas une chaîne de caractère",
        }),
        "status": JON.Enum(lang).choices(*list(
            map(
                lambda response: response['status'],
                responsesPossibles.values()
            )
        )).defaultError({
            "fr": "statut de la notification est invalide",
            "en": "statut de la notification est invalide",
        }),
        "type": JON.Enum(lang).choices(*list(
            map(
                lambda response: response['type'],
                responsesPossibles.values()
            )
        )).defaultError({
            "fr": "type de la notification est invalide",
            "en": "type de la notification est invalide",
        }),
    }).defaultError({
        "fr": "notif n'est pas un objet valide",
        "en": "notif n'est pas un objet valide"
    })
    if required:
        res = res.required()

    return res
def CRUDTotalSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut total qui represente le nombre total d'enregistrement pour une collection.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Number: Schema JON retourné
    '''
    return JON.Number(lang).integer().required().defaultError({
        "fr": "total n'est pas de type entier",
        "en": "total n'est pas de type entier",
    })
def CRUDOptionsSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider l'attribut options qui represente l'enregistrement recherché de type dictionnaire.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).typesValues(
        CRUDDatasSchema(lang)
    ).defaultError({
        "fr": "options doit être un objet",
        "en": "options doit être un objet"
    })


def CRUDOptionSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente les données en option possibles lors de l'écriture dans une collection.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "options": CRUDOptionsSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })
def CRUDFindAllSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors de la fonction _findAll de la classe hivipy.crud.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "datas": CRUDDatasSchema(lang),
        "meta": CRUDMetaSchema(lang),
        "total": CRUDTotalSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })
def CRUDCountAllSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors de la fonction _countAll de la classe hivipy.crud.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "total": CRUDTotalSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })
def CRUDFindOneSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors de la fonction _findOne de la classe hivipy.crud.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "data": CRUDDataSchema(lang),
        "exists": CRUDExistsSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })# .applyApp(
    #     rule=(lambda value: (
    #         (
    #             value['data'] is None and
    #             value['exists'] == False
    #         ) or (
    #             value['data'] is not None and
    #             value['exists'] == True
    #         )
    #     )),
    #     exception={
    #         "fr": "si la donnée n'existe pas alors exists doit être à False",
    #         "en": "si la donnée n'existe pas alors exists doit être à False",
    #     },
    # )
def CRUDElementExistsSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors de la fonction _exists de la classe hivipy.crud.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "exists": CRUDExistsSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })
def CRUDExecSingleSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors d'une action d'ecriture dans la bd à l'aide de la classe hivipy.crud .

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "data": CRUDDataSchema(lang),
        "notif": CRUDNotifSchema(lang, required=True),
    })
def CRUDExecAllSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors d'une action d'ecriture multiple dans la bd à l'aide de la classe hivipy.crud .

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "data": CRUDDatasSchema(lang),
        "notif": CRUDNotifSchema(lang, required=True),
    })

def CRUDExtractDatasSchema(lang: str):
    '''
    Retourne le schema utilsé pour valider un dictionnaire qui represente la reponse attendu lors de la fonction _extract de la classe hivipy.crud.

        Parameters:
            lang (str): La langue du message d'erreur

        Returns:
            JON.Object: Schema JON retourné
    '''
    return JON.Object(lang).struct({
        "datas": CRUDDatasSchema(lang),
        "meta": CRUDMetaExtractSchema(lang),
        "notif": CRUDNotifSchema(lang),
    })