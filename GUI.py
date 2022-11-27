import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
import platform
import cpuinfo

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
        self.info = QLabel("")
        self.choix = QComboBox()
        self.choix.addItem("OS")
        self.choix.addItem("RAM")
        self.choix.addItem("CPU")
        self.choix.addItem("IP")
        self.choix.addItem("Name")
        self.ok = QPushButton("Ok")
        self.quit = QPushButton("Quitter")
        self.aide =QPushButton("?")


        grid.addWidget(self.lab, 0, 0, 1, 2)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(self.choix, 1, 2, 1, 2)
        grid.addWidget(self.prenom, 2, 0)
        grid.addWidget(self.info, 2,2)
        grid.addWidget(self.ok, 3, 0, 1, 4)
        grid.addWidget(self.quit, 4, 0, 1, 4)
        grid.addWidget(self.aide,5, 4)


        self.ok.clicked.connect(self.__actionOk)
        self.quit.clicked.connect(self.__actionQuitter)
        self.aide.clicked.connect(self.__actionAide)
        self.setWindowTitle("Mon Application")


    def __actionOk(self):
        leprenom=self.text.text()
        self.prenom.setText(f"Bonjour {leprenom} !")
        try:
            if self.choix.currentText() == "OS":
                os= platform.platform()
                self.info.setText(f"Operating system: {os}")
            elif self.choix.currentText() == "CPU":
                my_cpuinfo = cpuinfo.get_cpu_info()
                self.info.setText(f"CPU: {my_cpuinfo}")
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Entrez un nombre")

    def __actionQuitter(self):
        QCoreApplication.exit(0)

    def __actionAide(self):
        QMessageBox.information(self, "Aide","Choisissez une information du pc, de la vm que vous voullez récupérer (l'os, le nom, l'ip, ...).")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()