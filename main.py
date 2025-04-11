import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFormLayout, QComboBox
from PyQt5.QtCore import Qt
from currencies import currencies

class ExchangeRates(QWidget):
    def __init__(self):
        super().__init__()
        ### amount of money to convert ###
        self.amount_label = QLabel("Amount:", self)
        self.amount_input = QLineEdit(self)

        ### currency to be converted ###
        self.from_currency_label = QLabel("From:", self)
        self.from_currency_input = QComboBox(self)
        # fill the currency types in 'from'
        for key, value in currencies.items():
            self.from_currency_input.addItem(f"{key} - {value}")

        ### desired conversion currency ###
        self.to_currency_label = QLabel("To:", self)
        self.to_currency_input = QComboBox(self)
        # fill the currency types in 'to'
        for key, value in currencies.items():
            self.to_currency_input.addItem(f"{key} - {value}")

        ### convert button ###
        self.convert_button = QPushButton("Convert", self)

        ### result of the conversion ###
        self.amount_converted = QLabel(self)

        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Exchange Rates")

        layout = QFormLayout()

        layout.addRow(self.amount_label, self.amount_input)
        layout.addRow(self.from_currency_label, self.from_currency_input)
        layout.addRow(self.to_currency_label, self.to_currency_input)
        layout.addRow(self.convert_button)
        layout.addRow(self.amount_converted)

        self.setLayout(layout)

        self.amount_converted.setAlignment(Qt.AlignCenter)

        self.amount_label.setObjectName("amount_label")
        self.amount_input.setObjectName("amount_input")
        self.from_currency_label.setObjectName("from_currency_label")
        self.from_currency_input.setObjectName("from_currency_input")
        self.to_currency_label.setObjectName("to_currency_label")
        self.to_currency_input.setObjectName("to_currency_input")
        self.convert_button.setObjectName("convert_button")
        self.amount_converted.setObjectName("amount_converted")
        
        self.setStyleSheet("""  
            QLabel, QComboBox, QPushButton{ 
                font-family: Calibri; 
            } 
            QLabel#amount_label{
                font-size: 20px;
            }
            QLineEdit#amount_input{
                font-size: 20px;
            }
            QLabel#from_currency_label{
                font-size: 20px;
            }
            QComboBox#from_currency_input{
                font-size: 20px;
            }
            QLabel#to_currency_label{
                font-size: 20px;
            }
            QComboBox#to_currency_input{
                font-size: 20px;
            }
            QPushButton#convert_button{
                font-size: 20px;
                font-weight: bold;
            }
            QLabel#amount_converted{
                font-size: 20px;
                font-weight: bold;
            }
        """)

        self.convert_button.clicked.connect(self.get_currency)

    def get_currency(self):
        api_key = "c31fa038cb93469bd402283a"
        amount = self.amount_input.text()
        from_currency = self.from_currency_input.currentText()[:3]
        to_currency = self.to_currency_input.currentText()[:3]
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"

        response = requests.get(url)
        data = response.json()

        if data["result"] == 'success':
            self.display_conversion(data, from_currency, to_currency, amount)
        elif data["result"] == 'error':
            self.display_error(data["error-type"])
            
    def display_error(self, message):
        self.amount_converted.setText(message)

    def display_conversion(self, data, from_currency, to_currency, amount):
        currency_value = data["conversion_rates"][to_currency]
        total = int(amount) * currency_value
        self.amount_converted.setText(f"{amount} {from_currency} = {total:.2f} {to_currency}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    exchange_rates_app = ExchangeRates()
    exchange_rates_app.show()
    sys.exit(app.exec_())