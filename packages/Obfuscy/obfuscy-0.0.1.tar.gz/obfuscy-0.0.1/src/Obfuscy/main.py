"""
A python package for obfuscating / "encrypting" strings.
"""

_charmap = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.',',','!','?',]

def _wrap_around(Input: int, min_value: int, max_value: int):
    range_size = max_value - min_value
    wrapped_Input = (Input - min_value) % range_size + min_value
    return wrapped_Input

def _generate_int_from_string(Input:str):
    stringTotal = 0
    for char in Input.lower():
        if char in _charmap:
            charIndex = int([index for index, value in enumerate(_charmap) if value == char][0])
        else:
            charIndex = 0
        stringTotal += charIndex
    return stringTotal

def _custom_encryption_str(Input:str,Key:str):
    numericKey = _generate_int_from_string(Key)
    encryptedString = ""
    for char in Input.lower():
        if char in _charmap:
            charIndex = int([index for index, value in enumerate(_charmap) if value == char][0])
        else:
            charIndex = 0
        encryptedString += _charmap[_wrap_around(charIndex+numericKey,0, len(_charmap))]
        numericKey += charIndex
    return encryptedString

def _custom_decryption_str(Input:str, Key:str):
    numericKey =_generate_int_from_string(Key)
    decryptedString = ""
    for char in Input.lower():
        if char in _charmap:
            charIndex = int([index for index, value in enumerate(_charmap) if value == char][0])
        else:
            charIndex = 0
        decryptedString += _charmap[_wrap_around(charIndex-numericKey, 0, len(_charmap))]
        numericKey += int([index for index, value in enumerate(_charmap) if value == decryptedString[-1]][0])
    return decryptedString

def encrypt_str(Input:str, Key:str = "", Method:int = 0):
    """
    Main encryption function.

    Methods:
    0: Custom encryption:
    This is a custom-made encryption algorythm that uses a key to encrypt the specified input.
    :param Input: String that is processed and returned in an encrypted form
    :type Input: str

    :param Key: Key that is used in some algorithms, and needed to decrypt the string
    :type Key: str

    :param Method: Encryption method used to encrypt the string
    :type Method: int

    :return: The string, encrypted using the specified key
    :rtype: str
    """
    match Method:
        case 0:
            return _custom_encryption(Input, Key)

def decrypt_str(Input:str, Key:str, Method:int=0):
    """
    Main decryption function.

    Methods:
    0: Custom decryption:
    This is a custom-made decryption algorythm that uses a key to decrypt the specified input.
    :param Input: String that is processed and returned in a decrypted form
    :type Input: str

    :param Key: Key that is used in some algorithms, and needed to decrypt the string
    :type Key: str

    :param Method: Decryption method used to encrypt the string
    :type Method: int

    :return: The string, decrypted using the specified key
    :rtype: str
    """
    match Method:
        case 0:
            return _custom_decryption(Input, Key)