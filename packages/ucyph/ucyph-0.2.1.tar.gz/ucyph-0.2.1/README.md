# ucyph
Encrypt and Decrypt text files from the command line using historical ciphers. 

## Installation
```bash
pip install ucyph
```

## Usage

All commands will require a **usage code** and a **text file** to encrypt/decrypt.
The **usage code** is a number that corresponds to a cipher([usage codes can be found here](#usage-codes)).
The **text file** is the file that will be encrypted/decrypted.

In addition to encrypting files, you can also use the application in **interactive mode**. To activate interactive mode, simply run the command ```ucyph``` without any arguments or with the ```-i``` flag. You will be prompted to enter a **usage code**, **text file**, and **key**(if applicable).
Interactive mode allows users to encrypt/decrypt text in the command line without having to use files.

### Examples:

#### Interactive Mode
```shell
ucyph -i
```

#### Encrypting/Decrypting Files
This command calls the ```Vigenere``` cipher with a **key** of 'password', and encrypts the text from **hello.txt** in place as an output file is not specified.
```shell
ucyph 5 hello.txt -k 'password'
```

To decrypt the text, simply add ```-d``` flag to the end of the command:
```shell
ucyph 5 hello.txt -k 'password' -d
```

This command calls the ```Playfair``` cipher with a **key** of 'password', and writes the encrypted text from **hello.txt** into **output.txt**.
```shell

ucyph 11 hello.txt -o output.txt -k password
```
Now, to decrypt the text from **output.txt**, simply add ```-d``` flag to the end of the command(note that an output file is not specified):
```shell
ucyph 11 output.txt -k password -d
```

## Usage Codes
| Cipher   | Usage Code  | Requires Key |
|----------|-------------|--------------|
| Caesar   | 3           | No           |
| Vigenere | 5           | Yes          |
| Playfair | 11          | Yes          |
| Rot-13   | 13          | No           |
| Rot-47   | 47          | No           |

## Cipher Descriptions:

### Caesar Cipher
"One of the simplest and most widely known encryption techniques. It is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet. For example, with a left shift of 3, D would be replaced by A, E would become B, and so on. The method is named after Julius Caesar, who used it in his private correspondence." - [Wikipedia article on Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher)

### Vigenere Cipher
"A method of encrypting alphabetic text where each letter of the plaintext is encoded with a different Caesar cipher, whose increment is determined by the corresponding letter of another text, the key.

For example, if the plaintext is **attacking tonight** and the key is **OCULORHINOLARINGOLOGY**, then

- the first letter a of the plaintext is shifted by 14 positions in the alphabet (because the first letter O of the key is the 14th letter of the alphabet, counting from 0), yielding o;
- the second letter t is shifted by 2 (because the second letter C of the key means 2) yielding v;
- the third letter t is shifted by 20 (U) yielding n, with wrap-around;
and so on; yielding the message **ovnlqbpvt eoeqtnh**. If the recipient of the message knows the key, they can recover the plaintext by reversing this process." - [Wikipedia article on Vigenere Cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)

### Playfair Cipher
" a manual symmetric encryption technique and was the first literal digram substitution cipher. The scheme was invented in 1854 by Charles Wheatstone, but bears the name of Lord Playfair for promoting its use.

The technique encrypts pairs of letters (bigrams or digrams), instead of single letters as in the simple substitution cipher and rather more complex Vigenère cipher systems then in use. The Playfair is thus significantly harder to break since the frequency analysis used for simple substitution ciphers does not work with it." - [Wikipedia article on Playfair Cipher](https://en.wikipedia.org/wiki/Playfair_cipher)

### Rot-13 Cipher
"ROT13 ("rotate by 13 places") is a simple letter substitution cipher that replaces a letter with the 13th letter after it, in the alphabet. ROT13 is a special case of the Caesar cipher which was developed in ancient Rome." - [Wikipedia article on Rot-13 Cipher](https://en.wikipedia.org/wiki/ROT13)

### Rot-47 Cipher
"ROT47 is a derivative of ROT13 which, in addition to scrambling the basic letters, also treats numbers and common symbols. The transformation is done by the same algorithm as for ROT13, except that characters are rotated by 47 places, rather than 13." - [Wikipedia article on Rot-47 Cipher](https://en.wikipedia.org/wiki/ROT13#Variants)