import os, hashlib

class AESEncryption:
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
        words = [key[i*8:i*8+8] for i in range(4)] # [w0, w1, w2, w3]
        for i in range(4, 44):
            previous = words[i-1]
            # print(previous)
            if i % 4 == 0:
                previous = self.__g(previous)
            new = int(words[i-4], base=16) ^ int(previous, base=16)      
            words.append(hex(new))
        return words
        
    def __g(self, word: str)->str:
        word = word[2:] if word.startswith("0x") else word
        word = word[2:] + word[:2]
        # TODO: sub table
        # TODO: RCj
        return word
    
    def encrypt(self, plaintext, key=None):
        ...
    def decrypt(self, key):...
    
a = AESEncryption()
k2 = a.round_key(a.gen_key("amin2323"))
# k1 = a.round_key(a.gen_key())
print(k2, sep="\n")