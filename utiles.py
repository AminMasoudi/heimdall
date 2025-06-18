
import base64, os
import hashlib
from Crypto.Cipher import AES
from api_service import APIService, File

Random = lambda : os.urandom(AES.block_size)

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random()
        cipher = AES.new(self.key)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def encrypting(file: bytes)-> bytes:
    key = str(os.environ.get("KEY"))
    return AESCipher(key).encrypt(file)

def decrypt(file):
    key = os.environ("KEY")
    return AESCipher(key).decrypt(file)

def finder(identifier:str)->File:
    files = APIService().list()
    matching = []
    for file in files:
        if str(file.id).startswith(identifier) and len(identifier) > 2:
            matching.append(file)
        elif file.name == identifier :
            matching.append(file)
    if len(matching) == 1:
        return matching[0]
    raise FileNotFoundError("failed to find the file")

