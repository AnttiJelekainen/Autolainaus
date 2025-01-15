# LABORATORIOETIKETTISOVELLUKSEN PÄÄIKKUNAN
# LUOMINEN Labra_ui.py TIEDOSTON PERUSTEELLA
# =========================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------

import os  # Polkumääritykset
import sys  # Käynnistysargumentit
import json # JSON-muunnokset

from PySide6 import QtWidgets
from saveSettings_ui import Ui_MainWindow  # Käännetyn käyttöliittymän luokka

import cipher # DIY moduuli salaukseen, käyttää Fernet-salausta

# Määritellään luokka, joka perii Qmainwindow- ja Ui_MainWindow-luokan


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """A class for creating main window for the application"""

    # Määritellään olionmuodostin ja kutsutaan yliluokkien muodostimia
    def __init__(self):
        super().__init__()

        # Luodaan käyttöliittymä konvertoidun tiedoston perusteella MainWindown ui-ominaisuudeksi. Tämä suojaa lopun MainWindow-olion ylikirjoitukselta.
        self.ui = Ui_MainWindow()

        # Kutsutaan käyttöliittymän muodostusmetodia setupUi
        self.ui.setupUi(self)

        # Salausavain luottamuksellisten asetusten kryptaamiseen
        # Avainta ei saa vaihtaa ohjelman käyttöönoton jälkeen!
        # Avain on luotu cipher.py
        self.secretKey = b'd5EJq-OqhgbU1XtSpj48xcdGDdsVxY8_YX8lnfEXPW8='
        self.cryptoEngine = cipher.createCipher(self.secretKey)

        # Luetaan asetustiedosto Python-sanakirjaksi
        self.currentSettings = {}

        # Tarkistetaan ensin, että asetustiedosto on olemassa
        try:
            with open('settings.json', 'rt') as settingsFile:
                jsonData = settingsFile.read()
                self.currentSettings = json.loads(jsonData)

            self.ui.serverLineEdit.setText(self.currentSettings['server'])
            self.ui.portLineEdit.setText(self.currentSettings['port'])
            self.ui.databaseLineEdit.setText(self.currentSettings['database'])
            self.ui.userLineEdit.setText(self.currentSettings['userName'])
            self.ui.passwordLineEdit.setText(self.currentSettings['password'])
        except Exception as e:
            self.openWarning()

        # OHJELMOIDUT SIGNAALIT
        # ---------------------

        # Kun Tallenna-painiketta on klikattu, kutsutaan saveToJsonFile-metodia
        self.ui.savePushButton.clicked.connect(self.saveToJsonFile)


    # OHJELMOIDUT SLOTIT
    # -------------------

    # Tallennetaan käyttöliittymään syötetyt asetukset tiedostoon
    def saveToJsonFile(self):

        # Luetaan käyttöliittymästä tiedot paikallisiin muuttujiin
        server = self.ui.serverLineEdit.text()
        port = self.ui.portLineEdit.text()
        database = self.ui.databaseLineEdit.text()
        userName = self.ui.userLineEdit.text()

        # Muutetaan merkkijono tavumuotoon (byte, merkistö UTF-8)
        plainTextPassword = bytes(self.ui.passwordLineEdit.text(), 'utf-8')

        # Salataan ja muunnetaan tavalliseksi merkkijonoksi, jotta JSON-tallennus onnistuu
        encryptedPassword = str(cipher.encrypt(self.cryptoEngine, plainTextPassword))


        # Muodosteteaan muuttujista Python-sanakirja
        settingsDictionary = {
            'server': server,
            'port': port,
            'database': database,
            'userName': userName,
            'password': encryptedPassword
        }

        # Muunnetaan sanakirja JSON-muotoon
        jsonData = json.dumps(settingsDictionary)

        # Avataan asetustiedosto ja kirjoitetaan asetukset
        with open('settings.json', 'wt') as settingsFile:
            settingsFile.write(jsonData)

    # Viivakoodin muodostus ja barcodeLabel:n päivitys

    def updateBarcodeLabel(self):
        """Updates the barcode label and sets ssnLineEdit to uppercase
        """
        # Tarkistetaan, että henkilötunnus on oikein muodostettu
        # Luetaan käyttöliittymästä henkilötunnus
        # uiSsn = self.ui.ssnLineEdit.text().upper()
        # ssnToCheck = identityCheck2.NationalSSN(
        #     uiSsn)  # Luodaan henkilötunnusobjekti
        # # Päivitetään myös syöyttökenttä isoihin kirjaimiin
        # self.ui.ssnLineEdit.setText(uiSsn)

        # # Jos se on oikein, luodaan viivakoodi ja päivitetään tilarivi
        # if ssnToCheck.isValidSsn():
        #     barcode128 = barcode.Code128B(uiSsn)  # Luodaan viivakoodi-olio
        #     # Lisätään alku- ja loppumerkki sekä varmistusssumma
        #     barCodeToPrint = barcode128.buildBarcode()
        #     # Päivitetään käyttöliittymän barcodeLabel
        #     self.ui.barcodeLabel.setText(barCodeToPrint)
        #     age = ssnToCheck.calculateAge()  # Lasketaan ikä
        #     ssnToCheck.getGender()  # Kutsutaan sukupuolen selvitys metodia
        #     gender = ssnToCheck.gender.lower()
        #     textToShow = f'Asiakas on {age}-vuotias {gender}'
        #     self.updateStatusbar(textToShow)

        # # Jos se on muodostettu väärin näytetään virheilmoitus MessageBox-ikkunassa
        # else:
        #     self.errorTitle = 'Henkilötunnus virheellinen'
        #     self.errorText = ssnToCheck.errorMessage
        #     self.openErrorMsgBox(self.errorTitle, self.errorText)
        #     self.ui.ssnLineEdit.setFocus()  # Palautetaan kursori takaisin elementtiin

    def beautifyElement(self, element):
        """Beautifies contents of an element

        Args:
            element (QtWidged): The element to be beautified
        """
        elementText = element.text()  # Luettaan elementin teksti
        elementText = elementText.strip()  # Poistetaan välit alusta ja lopusta
        elementText = elementText.title()  # Muutetaan isot alkukirjaimet
        element.setText(elementText)  # Päivitetään elementin teksti

    # Aktivoidaan tulostuspainike
    def enablePrintButton(self):
        """Enables the print button if all inputs are occupied with values
        """
        if self.ui.ssnLineEdit.text != '' or self.ui.firstNameLineEdit.text != '' or self.ui.lastNameLineEdit != '':
            self.ui.printPushButton.setEnabled(True)

    # Virheilmoitusikkuna
    def openErrorMsgBox(self, errorTitle, errorText):
        """Opens a message box alertig about an error

        Args:
            errorTitle (_type_): Title of the message box
            errorText (_type_): What kind of error occurs
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setWindowTitle(errorTitle)
        msgBox.setText(errorText)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # sound.shortBeep()
        msgBox.exec()

    # Tilarivinpäivitysrutiini
    def updateStatusbar(self, textToShow, timeToShow=-1):
        """Updates the statusbar

        Args:
            textToShow (str): A text to show on status bar
            timeToShow (int, optional): Duration in ms. -1 is infinite and its default
        """
        self.ui.statusbar.showMessage(textToShow, timeToShow)

    # Avataan MessageBox

    def openWarning(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowTitle('Puuttuvat asetukset')
        msgBox.setText('Asetuksia ei ole tehty, syötä tietokannan asetukset')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


if __name__ == "__main__":

    # Luodaan sovellus, jossa on käyttöjärjestelmästä riippumaton ulkonäkö (Fusion)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    # Luodaan objekti pääikkunalle ja tehdään siitä näkyvä
    window = MainWindow()
    window.show()

    # Käynnistetään sovellus ja tapahtumienkäsittelijä
    app.exec()
