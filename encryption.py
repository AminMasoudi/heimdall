import os, hashlib
from s_box import SBOX
class AESEncryption:
    def __init__(self, key=None):
        self.__key = self.gen_key(key)
        self.__round_keys = self.round_key(self.__key)
        print(self.__round_keys)
    def gen_key(self, base_key:str=None) -> str :
        """
        ## Gen Function for AES Encryption scheme
        in this function we take an optional base_key as input and then
        returns a 128 bit key in 32 bytes 
        **Notice:**  if base_key is not given then it generates a new random key             
        """
        if base_key is None:
            key = os.urandom(16).hex()
        else:
            key = hashlib.md5(base_key.encode()).hexdigest()
        return key
    
    def round_key(self, key:str):
        """
        ## Round key function
        in this function we take a key and return 44 round key from the key
        """
        words = ["0x" + key[i*8:i*8+8] for i in range(4)] # [w0, w1, w2, w3]
        rc= 1
        for i in range(4, 44):
            previous = words[i-1]
            # print(previous)
            if i % 4 == 0:
                previous = self.__g(previous, rc=rc)
                rc << 1
            new = int(words[i-4], base=16) ^ int(previous, base=16)      
            words.append(hex(new))
        return words
        
    def __g(self, word: str, rc:int)->str:
        word = word[2:] if word.startswith("0x") else word
        word = word[2:] + word[:2]
        # TODO: sub table
        
        new_bytes = ""
        for byte_index in range(0, 4, 2):
            c_1, c_2 = word[byte_index], word[byte_index+1]
            byte  = SBOX[int(c_1, base=16)][int(c_2, base=16)] 
            new_bytes += hex(byte)[2:]

        new_bytes = hex(int(new_bytes[:2], base=16) ^ rc) + new_bytes[2:]

        return new_bytes
    
    def encrypt(self, plaintext):
        ...
        ...
    def decrypt(self, key):...
    
a = AESEncryption()
# k1 = a.round_key(a.gen_key())
a.encrypt()