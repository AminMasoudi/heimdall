# Encryption with AES

in this project we use a symmetric encryption called: AES. why we did choose Symmetric scheme is simple: there is exactly one owner for each file who can encrypt or decrypt the file. and among the different encryption schema like 3-DES or ... i choose AES.(why? i dont know.)


[نسخه فارسی](./README.fa.md)
  

## Overview of AES:

AES is a block cipher with block length of 128, 192 or 256 bits. encryption consists of multiple rounds of processing: 10 for 128 bit block length, 12 for 192 and 14 for 256 bit. for ease of explanation we keep the default on 128 bit AES.

### History

### Components

- State Array
we have a block of 128 bits or 16 bytes. so we think of a 128 bit block as a consisting of a 4\*4 array of bytes(called **State Array**) like this:


$$
\begin
{pmatrix}
    byte_0 & byte_4 & byte_8 & byte_{12}
\\\ byte_1 & byte_5 & byte_9 & byte_{13}
\\\ byte_2 & byte_6 & byte_{10} & byte_{14}
\\\ byte_3 & byte_7 & byte_{11} & byte_{15}
\end{pmatrix}
$$


- Word
	an array of $byte_{i} byte_{i+1} byte_{i+2} byte_{i+3}$ which creates an array of 4 bytes

- Key
	a 128 bit key consists of 4 *word* as follows: $[w_0, w_1, w_2, w_3]$ and we expand our key to $[w_0...w_{43}]$

- SBOX
	a one-to-one function that takes a byte $b$ an returns a $\hat{b}$ 

## Key

expanding key:
```
Algorithm key_expanding(K[0...3])
rc = 0x01
for i from 4 to 44:
	if i mod 4 == 0:
		append (K[i-4] xor g(k[i-1]), rc) to K
		rc = rc * 2
	else:
		append (K[i-4] xor k[i-1]) to K
```

g function:
```
Algorithm g(k: 4bytes, rc: byte):
k = 1 byte circullar shift to right of k
k = subsititute k with SBOX
k = k xor (rc, 0x00, 0x00, 0x00)
return k
```

## Encription
