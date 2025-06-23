
import os
from api_service import APIService, File
from encryption import AESEncryption


def decrypt(file):
    key = os.environ("KEY")
    aes = AESEncryption(key)
    return aes.decrypt(file)

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