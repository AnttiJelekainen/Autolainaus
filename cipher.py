# MODUULI SALAUSAVAINTEN JA FERNET-SALAUKSEEN JA SEN PURKAMISEEN
# ===============================================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
from cryptography.fernet import Fernet

def newKey() -> str:
    """Creates a new key for encrypting and decrypting messages

    Returns:
        str: a key in byte form
    """
    key = Fernet.generate_key()
    return key

def createCipher(key: str) -> object:
    """Creates a new chipher ie. ecrypting machine

    Args:
        key (str): A fernet generated key

    Returns:
        object: The chipher object to use to for encrypt or decrypt
    """
    cipher = Fernet(key)
    return cipher

def encrypt(cipher: object, plainText: str) -> str:
    """Encrypts a message using Fernet algorithm

    Args:
        cipher (object): Fernet ciphering engine
        plainText (str): Text to be encrypted

    Returns:
        _type_: encrypted text in byte format
    """
    cryptoText = cipher.encrypt(plainText)
    return cryptoText

def decrypt(cipher:object, cryptoText:str, byteMode:bool=False):
    """Decrypts a message

    Args:
        cipher (object): Decrypting engine
        cryptoText (str): Encrypted text to be decrypted
        byteMode (bool, optional): If return value will be in byte form. Defaults to False.

    Returns:
        str: message in plain text 
    """
    if byteMode == True:
        plainText = cipher.decrypt(cryptoText)
    else:
        plainText = cipher.decrypt(cryptoText).decode()
    return plainText

# TODO: Lisää jossain vaiheessa funktiot, jotka ottavat parametriksi vain avaimen ja tekstin

if __name__ == "__main__":
    
    secretKey = newKey()
    print(secretKey)
