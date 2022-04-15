import numpy as np
import serial
import PyQt5
import pyqtgraph as pg
import sys  
import os
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot

# Classe da janela principal
class MainWindow(QtWidgets.QMainWindow):

    # Função que inicializa as propriedades da janela, dos botões e gráfico
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

#MainWindow

        self.setWindowTitle("Trabalho 2 - Sistema de Rega")
        # Dimensões
        self.setMinimumSize(900,500)
        self.setMaximumSize(900,500)
        # Posição no ecrã
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


#Drop down list Programas
        self.proglist = QtWidgets.QComboBox(self)
        self.proglist.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        self.proglist.setGeometry(490, 0, 50, 50)
#Labels    
        self.proglabel = QtWidgets.QLabel("Programa", self)
        self.diaslabel = QtWidgets.QLabel("Dias", self)
        self.canaislabel = QtWidgets.QLabel("Canais", self)
        self.hilabel = QtWidgets.QLabel("Início:", self)
        self.hflabel = QtWidgets.QLabel("Fim:", self)
        self.fontelabel = QtWidgets.QLabel("Fonte", self)
        self.sensoreslabel = QtWidgets.QLabel("Sensores", self)
        self.doispontosi = QtWidgets.QLabel(":", self)
        self.doispontosf = QtWidgets.QLabel(":", self)

#Posições Labels
        self.proglabel.setGeometry(375, 0, 100, 50)
        self.diaslabel.setGeometry(100, 50, 100, 50)
        self.canaislabel.setGeometry(733, 50, 100, 50)
        self.hilabel.setGeometry(330, 100, 100, 50)
        #self.hilabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.hflabel.setGeometry(330, 165, 100, 50)
        #self.hflabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter
        self.sensoreslabel.setGeometry(400, 240, 100, 50)
        self.fontelabel.setGeometry(415, 340, 100, 50)
        
#Checkboxes dias
        dianame=["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.dia = [QtWidgets.QCheckBox(dianame[i], self)for i in range(7)]
        for i in range(7):
            self.dia[i].setGeometry(75, 50*i+100, 110, 50)
        
#Checkboxes canais
        self.canais = [QtWidgets.QCheckBox(str(i+1), self)for i in range(12)]
        for i in range(6):
            self.canais[i].setGeometry(710, 50*i+100, 100, 50)
            self.canais[i+6].setGeometry(790, 50*i+100, 100, 50)

#Checkboxes sensores
        self.sensor1 = QtWidgets.QCheckBox("1", self)
        self.sensor2 = QtWidgets.QCheckBox("2", self)
        self.sensor1.setGeometry(380, 280, 100, 50)
        self.sensor2.setGeometry(480, 280, 100, 50)
        
#Selecionar Fonte
        self.fonte1 = QtWidgets.QRadioButton("Torneira", self)
        self.fonte2 = QtWidgets.QRadioButton("Bomba", self)
        self.fonte1.setGeometry(325, 380, 100, 50)
        self.fonte2.setGeometry(465, 380, 100, 50)

 #Hora inicial e final
        self.horainicial = QtWidgets.QSpinBox(self)
        self.mininicial = QtWidgets.QSpinBox(self)
        self.horafinal = QtWidgets.QSpinBox(self)
        self.minfinal = QtWidgets.QSpinBox(self)
        self.horainicial.setGeometry(400,100,65,50)
        self.mininicial.setGeometry(480,100,65,50)
        self.doispontosi.setGeometry(465,100,15,50)
        self.doispontosi.setAlignment(QtCore.Qt.AlignCenter)
        self.horafinal.setGeometry(400,165,65,50)
        self.minfinal.setGeometry(480,165,65,50)
        self.doispontosf.setGeometry(465,165,15,50)
        self.doispontosf.setAlignment(QtCore.Qt.AlignCenter)
        self.horainicial.setRange(0,23)
        self.mininicial.setRange(0,59)
        self.horafinal.setRange(0,23)
        self.minfinal.setRange(0,59)
        self.horainicial.setAlignment(QtCore.Qt.AlignCenter)
        self.horafinal.setAlignment(QtCore.Qt.AlignCenter)
        self.mininicial.setAlignment(QtCore.Qt.AlignCenter)
        self.minfinal.setAlignment(QtCore.Qt.AlignCenter)

#Botões Guardar e Ativo
        self.guardar = QtWidgets.QPushButton("Guardar",self)
        self.ativo = QtWidgets.QPushButton("OFF",self)
        self.ativo.setCheckable(True)
        self.ativo.setGeometry(680,420,70,50)
        self.guardar.setGeometry(760,420,100,50)
        self.ativo.clicked.connect(self.on_off)
        self.ativo.setStyleSheet("background-color : rgb(255,100,100)")
    def on_off(self):
# if button is checked
        if self.ativo.isChecked():
# setting background color to light-blue
            self.ativo.setStyleSheet("background-color : green")
            self.ativo.setText("ON")
# if it is unchecked
        else:
# set background color  back to light-grey
            self.ativo.setStyleSheet("background-color : rgb(255,100,100)")
            self.ativo.setText("OFF")
   
app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 14pt;}" "QComboBox{font-size: 12pt;}" "QCheckBox{font-size: 12pt;}" "QRadioButton{font-size: 12pt;}" "QSpinBox{font-size: 12pt;}" "QPushButton{font-size: 12pt;}")

main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_())
# Fechar a aplicação e sair do programa