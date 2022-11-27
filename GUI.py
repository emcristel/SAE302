import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton


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
        ok = QPushButton("Ok")
        quit = QPushButton("Quitter")


        grid.addWidget(self.lab, 0, 0, 1, 2)
        grid.addWidget(self.text, 1, 0, 1, 2)
        grid.addWidget(self.prenom, 2, 0)
        grid.addWidget(ok, 3, 0, 1, 2)
        grid.addWidget(quit, 4, 0, 1, 2)


        ok.clicked.connect(self.__actionOk)
        quit.clicked.connect(self.__actionQuitter)
        self.setWindowTitle("Ma fenêtre")

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