# LABORATORIOETIKETTISOVELLUKSEN PÄÄIKKUNAN
# LUOMINEN Labra_ui.py TIEDOSTON PERUSTEELLA
# =========================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------

import os # Polkumääritykset
import sys # Käynnistysargumentit

from PySide6 import QtWidgets
from labra_ui import Ui_MainWindow # Käännetyn käyttöliittymän luokka

import identityCheck2 # Henkilötunnuksen tarkistukseen liittyvät työkalut
import barcode # Viivakoodin muodostukseen tarvittavat rutiinit
from avtools import sound # Äänitoiminnot

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

        # OHJELMOIDUT SIGNAALIT
        # ---------------------

        # Kun poistutaan ssnLineEdit-elementistä suoritetaan barcodeLabel-elementin päivitys
        # HUOM! Jos poistutaan Enter-näppäimellä virheilmoitus aukeaa kahdesti
        #TODO: Etsi tähän korjaus
        self.ui.ssnLineEdit.editingFinished.connect(self.updateBarcodeLabel)

        # Siistitään etunimi- ja sukunimielementit poistuttaessa
        self.ui.firstNameLineEdit.editingFinished.connect(lambda: self.beautifyElement(self.ui.firstNameLineEdit))
        self.ui.lastNameLineEdit.editingFinished.connect(lambda: self.beautifyElement(self.ui.lastNameLineEdit))

        # Aktivoidaan tulostuspainiken sen jälkeen kun etikettin määrä on säädetty
        self.ui.amountSpinBox.valueChanged.connect(self.enablePrintButton)

    

    # OHJELMOIDUT SLOTIT
    #-------------------


    # Viivakoodin muodostus ja barcodeLabel:n päivitys
    def updateBarcodeLabel(self):
        """Updates the barcode label and sets ssnLineEdit to uppercase
        """
        # Tarkistetaan, että henkilötunnus on oikein muodostettu
        uiSsn = self.ui.ssnLineEdit.text().upper() # Luetaan käyttöliittymästä henkilötunnus
        ssnToCheck = identityCheck2.NationalSSN(uiSsn) # Luodaan henkilötunnusobjekti
        self.ui.ssnLineEdit.setText(uiSsn) # Päivitetään myös syöyttökenttä isoihin kirjaimiin

        # Jos se on oikein, luodaan viivakoodi ja päivitetään tilarivi
        if ssnToCheck.isValidSsn():
            barcode128 = barcode.Code128B(uiSsn) # Luodaan viivakoodi-olio
            barCodeToPrint = barcode128.buildBarcode() # Lisätään alku- ja loppumerkki sekä varmistusssumma
            self.ui.barcodeLabel.setText(barCodeToPrint) # Päivitetään käyttöliittymän barcodeLabel
            age = ssnToCheck.calculateAge() # Lasketaan ikä
            ssnToCheck.getGender() # Kutsutaan sukupuolen selvitys metodia
            gender = ssnToCheck.gender.lower()
            textToShow = f'Asiakas on {age}-vuotias {gender}'
            self.updateStatusbar(textToShow)


        # Jos se on muodostettu väärin näytetään virheilmoitus MessageBox-ikkunassa
        else:
            self.errorTitle = 'Henkilötunnus virheellinen'
            self.errorText = ssnToCheck.errorMessage
            self.openErrorMsgBox(self.errorTitle, self.errorText)
            self.ui.ssnLineEdit.setFocus() # Palautetaan kursori takaisin elementtiin

    def beautifyElement(self, element):
        """Beautifies contents of an element

        Args:
            element (QtWidged): The element to be beautified
        """
        elementText = element.text() # Luettaan elementin teksti
        elementText = elementText.strip() # Poistetaan välit alusta ja lopusta
        elementText = elementText.title() # Muutetaan isot alkukirjaimet
        element.setText(elementText) # Päivitetään elementin teksti
        
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
        sound.shortBeep()
        msgBox.exec()

    # Tilarivinpäivitysrutiini
    def updateStatusbar(self, textToShow, timeToShow=-1):
        """Updates the statusbar

        Args:
            textToShow (str): A text to show on status bar
            timeToShow (int, optional): Duration in ms. -1 is infinite and its default
        """
        self.ui.statusbar.showMessage(textToShow, timeToShow)

if __name__ == "__main__":

    # Luodaan sovellus, jossa on käyttöjärjestelmästä riippumaton ulkonäkö (Fusion)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    # Luodaan objekti pääikkunalle ja tehdään siitä näkyvä
    window = MainWindow()
    window.show()

    # Käynnistetään sovellus ja tapahtumienkäsittelijä
    app.exec()
