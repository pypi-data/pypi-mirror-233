import base64
from dbm import dumb
import hashlib
import logging
import traceback
import datetime
import json
from Crypto.Hash import HMAC, SHA256, MD5 as MD5_
from Crypto.Cipher import AES as AES_
from Crypto.Random import get_random_bytes
import jwt
import pytz
from copy import deepcopy

from .string import RandomIdentifier
from .objects import loopObject
from .config import dateFormat1, timeFormat1, dateFormat5

from .hivi_init import Manager


log = logging.getLogger(__name__)
manager = Manager()
structConf = manager.getStructConfig()
DEBUG = structConf['debug']
securityConfig = manager.getSecurityConfig()
# if DEBUG : 
    # print("> hivipy.crypto | securityConfig:: ", securityConfig)

class MD5():
    """ Permet d'hacher un texte à l'aide de la fonction de hachage MD5
    """
    SECRET_KEY = securityConfig['keysecret']

    def hash(self, message: str):
        """ MD5 - Fonction de hachage d'un texte 
 
        Cette methode permet de hacher un texte et retourner un string qui represente la valeur hachée
    
        Parameters
        ------------
            message: str
                le texte de depart qui sera haché
        Return
        -----------
            hachedText : str
                Le texte haché en fonction de la clé de cryptage se trouvant dans main/hivi_init.ini > section SECURITY > attribut <keysecret>. 
        """
        try:
            h = HMAC.new(self.SECRET_KEY.encode("utf8"), msg = message.encode("utf8"), digestmod=MD5_)
            return base64.b64encode(h.digest()).decode()
        except ValueError:
            stack = str(traceback.format_exc())
            log.error(stack)
            return None
class SHA():
    """ Permet d'hacher un texte à l'aide de la fonction de hachage SHA
    """
    SECRET_KEY = securityConfig['keysecret']
    mode = SHA256

    def __init__(self,):
        pass

    def hash(self,
        message: str,
    ):
        """ SHA - Fonction de hachage d'un texte 
 
        Cette methode permet de hacher un texte et retourner un string qui represente la valeur hachée
    
        Parameters
        ------------
            message: str
                le texte de depart qui sera haché
        Return
        -----------
            hachedText : str
                Le texte haché en fonction de la clé de cryptage se trouvant dans main/hivi_init.ini > section SECURITY > attribut <keysecret>. 
        """
        try:
            h = HMAC.new(self.SECRET_KEY.encode("utf8"), msg = message.encode("utf8"), digestmod=self.mode)
            return base64.b64encode(h.digest()).decode()
        except ValueError:
            stack = str(traceback.format_exc())
            log.error(stack)
            return None

class AES:
    """ Permet de crypter et decrypter une texte à l'aide de l'algorithme de chiffrement AES
    """
    HASH_NAME = "SHA256"
    IV_LENGTH = 16
    ITERATION_COUNT = 65536
    KEY_LENGTH = 32
    SECRET_KEY = securityConfig['keysecret']
    F_SALT = securityConfig['fsalt']
    AES_MODE = AES_.MODE_CBC

    def pad(self, s):
        return s + (self.IV_LENGTH - len(s) % self.IV_LENGTH) * chr(self.IV_LENGTH - len(s) % self.IV_LENGTH)
    def unpad(self, s):
        return s[0:-ord(s[-1:])]
    def get_secret_key(self):
        return hashlib.pbkdf2_hmac(self.HASH_NAME, self.SECRET_KEY.encode(), self.F_SALT.encode(), self.ITERATION_COUNT, self.KEY_LENGTH)

    def encrypt(self, message):
        """ AES - Fonction de cryptage d'un texte 
 
        Cette methode permet de crypter un message
    
        Parameters
        ------------
            message: str
                le texte de depart qui sera crypté
        Return
        -----------
            encryptedText : str
                Le texte crypté en fonction de la clé de cryptage se trouvant dans main/hivi_init.ini > section SECURITY > attribut <keysecret> && <fsalt>. 
        """
        secret = self.get_secret_key()
        message = self.pad(message)
        iv = get_random_bytes(self.IV_LENGTH)
        cipher = AES_.new(secret, self.AES_MODE, iv)
        cipher_bytes = base64.b64encode(iv + cipher.encrypt(message.encode("utf8")))
        return bytes.decode(cipher_bytes)
    def decrypt(self, cipher_text):
        """ AES - Fonction de decryptage d'un texte dejà crypté
 
        Cette methode permet de decrypter un message dejà crypté
    
        Parameters
        ------------
            cipher_text: str
                texte dejà crypté auparavant
        Return
        -----------
            decryptedText : str
                Le texte decrypté en fonction de la clé de cryptage se trouvant dans main/hivi_init.ini > section SECURITY > attribut <keysecret> && <fsalt>. 
        """
        secret = self.get_secret_key()
        decoded = base64.b64decode(cipher_text)
        iv = decoded[:AES_.block_size]
        cipher = AES_.new(secret, self.AES_MODE, iv)
        original_bytes = self.unpad(cipher.decrypt(decoded[self.IV_LENGTH:]))
        return bytes.decode(original_bytes)


class KeyGenerator():
    def generate(self, length: int = 5):
        return AES().encrypt(RandomIdentifier(lengthStr=length))
    def decrypt(self, value):
        return AES().decrypt(value)
    def check(self, key, value):
        try:
            res: bool = (self.decrypt(key) == value)
            return res
        except ValueError:
            stack = str(traceback.format_exc())
            log.error(stack)
            return False
class CodeGenerator():
    def generate(self, length: int = 5):
        return Token().generate(RandomIdentifier(lengthStr=length))
    def check(self, key, value):
        try:
            res: bool = (self.decrypt(key) == value)
            return res
        except ValueError:
            stack = str(traceback.format_exc())
            log.error(stack)
            return False


class Token():
    """ Permet de generer un token pour l'authentification
    """
    PRIVATE_KEY = securityConfig['keysecret']
    PUBLIC_KEY = securityConfig['fsalt']
    ALGORITHMS="HS256"

    def generate(self, data: any):
        data = data
        # data = json.loads(
        #     json.dumps(data)
        # ) if type(data) in (dict, tuple, list, str, int ,float, bool) else data
        def mapForLoopObject(index, key, element, data):
            if type(element) in (str, int ,float, bool):
                return element
            elif type(element) is datetime.datetime:
                return element.strftime(dateFormat1)
            elif type(element) is datetime.time:
                return element.strftime(timeFormat1)
            elif type(element) is datetime.date:
                return element.strftime(dateFormat5)
        data = loopObject(
            data,
            map = mapForLoopObject,
        )
        data = data if type(data) == dict else {
            'data': data,
        }
        resData = jwt.encode(data, self.PRIVATE_KEY, algorithm=self.ALGORITHMS, headers={
            '_date_added': datetime.datetime.now(tz=pytz.UTC).isoformat()
        }) if data is not None else None
        if type(resData) == str:
            resData = resData.split(".")[-1] if len(resData.split(".")[-1]) > 0 else resData
            resData = RandomIdentifier(lengthStr=10, mapF= lambda data: "{data}.{token}".format(
                data = data,
                token = resData,
            ))
        return resData
    def decrypt(self, value):
        return AES().decrypt(value)