# Coding:utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.setWindowTitle('Учим мятежные стихи')
        self.setStyleSheet("background-color: rgb(150, 250, 250)")
        self.stiharr = [[]]  # массив с массивами (блоками) строк стиха
        self.currblocknum = 0  # номер текущего блока в массиве
        self.currlinenum = -1  # номер текущей строки в блоке
        self.linedist = 5  # расстояние в пикселях 
        # массив для лабелей со строками стиха
        self.stihlabs = []
        for i in range(28):
            self.stihlabs.append(QLabel(self))
            self.stihlabs[-1].resize(700, 20)
            self.stihlabs[-1].move(50, self.linedist + i * (self.linedist + 20))
            self.stihlabs[-1].setFont(QFont('Ariel', 12))
        # кнопка выбора файла
        self.openbtn = QPushButton(self)
        self.openbtn.resize(50, 50)
        self.openbtn.setFont(QFont('Arial', 15))
        self.openbtn.setText('📂')
        self.openbtn.move(740, 740)
        self.openbtn.clicked.connect(self.openStih)
        # стрелка к левому блоку
        self.rightbtn = QPushButton(self)
        self.rightbtn.resize(30, 700)
        self.rightbtn.move(760, 20)
        self.rightbtn.setText('=>')
        self.rightbtn.clicked.connect(self.changeBlock)
        # стрелка к правому блоку
        self.leftbtn = QPushButton(self)
        self.leftbtn.resize(30, 700)
        self.leftbtn.move(10, 20)
        self.leftbtn.setText('<=')
        self.leftbtn.clicked.connect(self.changeBlock)
        # эдит для ввода номера блока
        self.blockedit = QLineEdit(self)
        self.blockedit.resize(100, 50)
        self.blockedit.setFont(QFont('Ariel', 20))
        self.blockedit.move(10, 740)
        self.blockedit.hide()
        # лабел "/ кол-во блоков"
        self.fromblockslab = QLabel(self)
        self.fromblockslab.resize(100, 50)
        self.fromblockslab.setFont(self.blockedit.font())
        self.fromblockslab.move(self.blockedit.x() + self.blockedit.width() + 10, 740)
        self.fromblockslab.hide()
        # кнопка "перейти"
        self.gobtn = QPushButton(self)
        self.gobtn.resize(200, 50)
        self.gobtn.move(self.fromblockslab.x() + self.fromblockslab.width() + 10, 740)
        self.gobtn.setText('ПЕРЕЙТИ')
        self.gobtn.setFont(self.blockedit.font())
        self.gobtn.hide()
        
    def openStih(self):
        '''открытие файла со стихом и запись его в массив'''
        self.stiharr = [[]]
        for lab in self.stihlabs:  # убираем текст
            lab.setText('')
        try:
            with open(QFileDialog().getOpenFileName(self, "выберете файл со стихом", '', 'текстовой документ(*.txt)')[0], mode='r',  encoding="utf-8") as f:
                for line in f.readlines():
                    if line.count(' ') + line.count('\n') + line.count('*') == len(line):
                        self.stiharr.append([])
                    else:
                        self.stiharr[-1].append(line)
            self.currblocknum = 0
            self.currlinenum = len(self.stiharr[0]) 
            for i in range(len(self.stiharr[0])):  # установка первого блока
                self.stihlabs[i].setText(self.stiharr[0][i])
            self.blockedit.show()
            self.blockedit.setText(str(self.currblocknum + 1))
            self.fromblockslab.show()
            self.fromblockslab.setText('/' + str(len(self.stiharr)))
            self.gobtn.clicked.connect(self.changeBlock)
            self.gobtn.show()
        except:
            #print('error in the opening')
            self.stiharr = [[]]
        
    def changeBlock(self):
        '''переход к следующему/предыдущему/указанному блоку текста'''
        if self.currblocknum < len(self.stiharr) - 1 and self.sender() == self.rightbtn:  # к следующему
            self.currblocknum += 1
        if self.currblocknum > 0 and self.sender() == self.leftbtn:  # к предыдущему
            self.currblocknum -= 1
        if self.sender() == self.gobtn and self.blockedit.text().isdigit() and\
           int(self.blockedit.text()) > 0 and int(self.blockedit.text()) <= len(self.stiharr):
            self.currblocknum = int(self.blockedit.text()) - 1
        self.blockedit.setText(str(self.currblocknum + 1))
        self.currlinenum = len(self.stiharr[self.currblocknum])
        for lab in self.stihlabs:  # убираем текст
            lab.setText('')
        for i in range(len(self.stiharr[self.currblocknum])):  # показываем текст
            self.stihlabs[i].setText(self.stiharr[self.currblocknum][i])
    
    # events
            
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Left and self.currlinenum >= 1:
            self.stihlabs[self.currlinenum - 1].setText('')
            self.currlinenum -= 1
        if event.key() == Qt.Key_Right and self.currlinenum < len(self.stiharr[self.currblocknum]):
            self.currlinenum += 1
            self.stihlabs[self.currlinenum - 1].setText(self.stiharr[self.currblocknum][self.currlinenum - 1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MW()
    mw.show()
    sys.exit(app.exec_())