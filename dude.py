import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel
from PyQt5.QtWidgets import QTabWidget, QLineEdit, QFormLayout, QMainWindow
from PyQt5 import uic
import sqlite3
from random import randint


def classic_levenshtein(string_1, string_2):
    len_1 = len(string_1)
    len_2 = len(string_2)
    cost = 0
    if len_1 and len_2 and string_1[0] != string_2[0]:
        cost = 1
    if len_1 == 0:
        return len_2
    elif len_2 == 0:
        return len_1
    else:
        return min(
            classic_levenshtein(string_1[1:], string_2) + 1,
            classic_levenshtein(string_1, string_2[1:]) + 1,
            classic_levenshtein(string_1[1:], string_2[1:]) + cost,
        )


class Wordery(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('qtfile1.ui', self)
        self.pushButton1.clicked.connect(self.dobav)
        self.pushButton2.clicked.connect(self.findword)
        self.pushButton4.clicked.connect(self.victorine)
        self.pushButton41.clicked.connect(self.check)
        self.con = sqlite3.connect("words.db")
        self.otv1, self.otv2 = None, None
        cur = self.con.cursor()
        self.englist = cur.execute('Select engwords from Slova').fetchall()
        self.ruslist = cur.execute('Select ruswords from Slova').fetchall()
        for q in range(len(self.englist)):
            self.englist[q], self.ruslist[q] = self.englist[q][0].lower(), self.ruslist[q][0].lower()

    def dobav(self):
        rus = self.lineEdit1.text().lower()
        eng = self.lineEdit12.text().lower()
        cur = self.con.cursor()
        cur.execute('INSERT INTO Slova(engwords,ruswords) VALUES(' + "'" + eng + "'" + ',' + "'" + rus + "'" + ')')
        self.con.commit()

    def findword(self):
        cur = self.con.cursor()
        if 191 <= ord(self.lineEdit2.text()[0]) <= 255:
            cur = self.con.cursor()
            engword = cur.execute('Select engwords from Slova where ruswords='
                                  + "'" + str(self.lineEdit2.text().lower()) + "'").fetchone()
            if engword:
                self.label_23.setText(engword[0])
            else:
                neuspis = []
                for r in range(len(self.englist)):
                    neuspis.append(classic_levenshtein(str(self.ruslist), str(self.englist[r])))
                a = min(neuspis)
                self.label_23.setText('Может вы имели в виду ' + self.ruslist[neuspis.index(a)])
            cur.close()
        else:
            rusword = cur.execute('Select ruswords from Slova where engwords='
                                  + "'" + str(self.lineEdit2.text()) + "'").fetchone()
            if rusword:
                self.label_23.setText(rusword[0])
            else:
                neuspis = []
                for r in range(len(self.ruslist)):
                    neuspis.append(classic_levenshtein(str(self.englist), str(self.ruslist[r])))
                a = min(neuspis)
                self.label_23.setText('Может вы имели в виду ' + self.englist[neuspis.index(a)])
        self.label_23.repaint()
        cur.close()

    def victorine(self):
        for q in range(len(self.englist)):
            self.englist[q], self.ruslist[q] = self.englist[q], self.ruslist[q]
        r = randint(0, len(self.englist) - 1)
        self.otv1 = self.englist[r]
        self.label42.setText(self.otv1)
        self.label44.setText('')
        self.label42.repaint()
        self.label44.repaint()

    def check(self):
        if self.lineEdit4.text().lower() in self.ruslist:
            self.otv2 = self.englist[self.ruslist.index(self.lineEdit4.text().lower())]
            if self.otv1.upper() == self.otv2.upper():
                self.label44.setText('Верно!')
            else:
                self.label44.setText('Неправильно')
        else:
            self.label44.setText('Не из словаря')
        self.label44.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Wordery()
    ex.show()
    sys.exit(app.exec())
