import os, hashlib
from s_box import SBOX
class AESEncryption:
    def __init__(self, key=None):
        self.__key = self.gen_key(key)
        self.__round_keys = self.round_key(self.__key)

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
            if i % 4 == 0:
                previous = self.__g(previous, rc=rc)
                rc << 1
            new = int(words[i-4], base=16) ^ int(previous, base=16)      
            words.append(new.to_bytes(4).hex())
        return words
        
    def __g(self, word: str, rc:int)->str:
        word = word[2:] if word.startswith("0x") else word
        word = word[2:] + word[:2]
        # TODO: sub table
        
        new_bytes = ""
        for byte_index in range(0, 4, 2):
            new_bytes += self.__sub_byte(word[byte_index: byte_index+2])

        new_bytes = (int(new_bytes[:2], base=16) ^ rc).to_bytes().hex() + new_bytes[2:]

        return new_bytes
    
    def encrypt(self, plaintext:bytes)->str:
        # padding
        padding_size = 16 - ((len(plaintext)) % 16)
        plaintext = plaintext + (padding_size * padding_size.to_bytes())
        # spilt
        blocks = [plaintext[i*16:i*16+16] for i in range(len(plaintext)//16)]
        # encrypt blocks
        blocks = list(map(lambda block: self.encrypt_block(block) ,blocks))
        # join cipher blocks
        blocks = ''.join(blocks)
        return blocks
        # encrypt
        
    def encrypt_block(self, block: bytes) -> str: 
        # create table
        table = [''.join([hex(block[j])[2:] for j in range(4*i, 4*i+4)]) for i in range(4)]
        table = self.__add_round_key(table, self.__round_keys[:4])
        for round in range(1, 11):
            table = self.__sub_bytes(table)
            table = self.__shift_rows(table)
            if round != 10:
                table = self.__mix_columns(table)
            table = self.__add_round_key(table, self.__round_keys[round*4: round*4 + 4])
        block = ''.join(table)
        return block

    def __sub_bytes(self, table:list[str])->list[str]:
        for column_index in range(4):
            new_col = ''
            for i in range(4):
                new_col += self.__sub_byte(table[column_index][i*2: i*2+2])
            table[column_index] = new_col
        return table

    def __sub_byte(self, word:str)->str:
        if word.startswith('0x'): word = word[2:]
        c_1, c_2 = word[0], word[1]
        byte  = SBOX[int(c_1, base=16)][int(c_2, base=16)] 
        byte  = byte.to_bytes().hex()
        return byte

    def __add_round_key(self, table:list[str], keys:list[str]) -> list[str]:
        for i in range(4):
            r = int(table[i], base=16) ^ int(keys[i], base=16)
            table[i] = r.to_bytes(4).hex()
        return table
            
        
    def __shift_rows(self, table:list[str])->list[str]:
        new_table = []
        for counter in range(4):
            string = "".join(
                [table[(i + counter) % 4][2*i: 2*i+2] for i in range(0, 4)]
                )
            new_table.append(string)
        return new_table
    
    def __inv_shift_rows(self, table:list[str])-> list[str]:
        new_table = []
        for counter in range(4):
            string = "".join(
                [table[(i + counter) % 4][2*j: 2*j+2] for j, i in enumerate(range(0, -4, -1))]
            )
            new_table.append(string)
        return new_table

    def __gmul(self, a, b):
        """Galois Field (256) Multiplication of two Bytes"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            high_bit = a & 0x80
            a = (a << 1) & 0xFF
            if high_bit:
                a ^= 0x1B
            b >>= 1
        return p

    def __mix_columns(self, table:list[str])->list[str]:
        table = [[int(c[2*i:2*i+2], base=16) for i in range(4)] for c in table]
        new_table = []
        for c in table:
            col = []
            for r in range(4):
                val: int = (
                    self.__gmul(2, c[r]) 
                    ^ self.__gmul(3 , c[(r +1)%4]) 
                    ^ c[(r  + 2)%4] 
                    ^ c[(r+3)%4])
                
                col.append(val.to_bytes().hex())
            new_table.append(col)
        table = ["".join(c) for c in new_table]
        return table

    def __inv_mix_columns(self, table:list[str])->list[str]:
        table = [[int(c[2*i:2*i+2], base=16) for i in range(4)] for c in table]
        new_table = []
        for c in table:
            col = []
            for r in range(4):
                val: int = (
                    self.__gmul(  0xe, c[r]) 
                    ^ self.__gmul(0xb , c[(r +1)%4]) 
                    ^ self.__gmul(0xd, c[(r  + 2)%4]) 
                    ^ self.__gmul(0x9, c[(r+3)%4])
                )
                col.append(val.to_bytes().hex())
            new_table.append(col)
        table = ["".join(c) for c in new_table]
        return table
    
    def decrypt(self, key):...

    
# a = AESEncryption(key="amin2323")
# print(a.encrypt(b'hello world! 123'))
# 5315b6eb8d7d26e1dc601f683334933daa02146b5e51cb44984abf095e3c1e3f

