# Tiedoston käsittely: Avaaminen ja sulkeminen
# ============================================

# KIRJASTOT JA MODUULIT
# ---------------------

import json
from cryptography import fernet # Symmetrinen salaustyökalu

# # Avataan tiedosto lukua varten
# settingsFile = open("settings.txt", "rt")
# fileContent = settingsFile.read() # Luetaan tiedosto
# print(fileContent) # Tulostetaan se

# # Avataan kirjoitusta varten
# settingFile2 = open('settings.txt', 'wt')
# uudetAsetukset = 'Asetukset\nPalvelin: 10.66.0.3\n'
# settingFile2.write('Tyhjät asetukset: ') # Kirjoitetaan uudet tiedot
# settingFile2.close() # Suljettava kirjoituksen jälkeen

# # Avataan uudelleenkirjoituksen jälkeen
# settingFile3 = open('settings.txt', 'rt')
# print(settingFile3.read())

# asetukset = {} # Luodaan muuttuja sanakirjaa varten, tyhjä dict

# # Luetaan tiedosto with-rakenteen avulla. Tiedosto suljetaan ja muisti tyhjennetään operaation päätteeksi
# with open('settings.txt', 'rt') as settingsFile4:
#     rawData = settingsFile4.read() # Luetaan tiedosto tekstinä
#     asetukset = json.loads(rawData) # Muunnetaan json muotoinen teksti Python-sanakirjaksi

# print(f'Tietokanta on: {asetukset["Tietokanta"]}')
# print(f'Se sijaitsee palvelimella {asetukset['Palvelin']}')

# asetuksetDict = {
#     'server': 'autolaina.raseko.fi', 
#     'port': 5432,
#     'database': 'autolainaus',
#     'userName': 'postgres',
#     'password': 'Q2werty'
#     }

# asetuksetJson = json.dumps(asetuksetDict)
# print(asetuksetJson)

# # Kirjoitetaan asetustiedostoon ja luodaan se, jos ei ole jo olemassa
# with open('asetukset.json', 'wt') as settingsFile7:
#     settingsFile7.write(asetuksetJson)

# with open('settings.txt', 'at') as settingsFile5:
#     settingsFile5.write('\nskeema: public')

# with open('settings.txt', 'rt') as settingsFile6:
#     print(settingsFile6.read())

# Luodaan oikean mittainen salausavain
chipherKey = fernet.Fernet.generate_key()

# Määritellään salausalgoritmi käyttämään luotua avainta
chipher = fernet.Fernet(chipherKey)

# Määritellään teksti tavuiksi (8bit)
plainPassword = b'Q2werty7'

encryptedPassword = chipher.encrypt(plainPassword)

print(f'Salatussa muodossa: {encryptedPassword.decode()}')

# Puretaan salaus
decryptedPassword = chipher.decrypt(encryptedPassword).decode()

print(f'Salaus purettuna on: {decryptedPassword}')
