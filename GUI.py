import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.lab = QLabel("Saisir votre nom")
        self.text = QLineEdit("")
        self.prenom = QLabel("")
        self.choix = QComboBox()
        self.choix.addItem("OS")
        self.choix.addItem("RAM")
        self.choix.addItem("CPU")
        self.choix.addItem("IP")
        self.choix.addItem("Name")
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")


        grid.addWidget(self.lab, 0, 0, 1, 2)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(self.choix, 1, 2, 1, 2)
        grid.addWidget(self.prenom, 2, 0)
        grid.addWidget(ok, 3, 0, 1, 4)
        grid.addWidget(quit, 4, 0, 1, 4)


        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)
        self.setWindowTitle("Mon Application")

    def __actionOk(self):
        leprenom=self.text.text()
        self.prenom.setText(f"Bonjour {leprenom} !")

    def __actionQuitter(self):
        QCoreApplication.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()