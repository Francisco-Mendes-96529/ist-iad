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
        self.setMinimumSize(1100,500)
        self.setMaximumSize(1100,500)
        # Posição no ecrã
        self.move(400,200)

#Drop down list Programas
        self.proglist = QtWidgets.QComboBox(self)
        self.proglist.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        self.proglist.setGeometry(100, 0, 100, 50)
#Labels    
        self.proglabel = QtWidgets.QLabel("Programa", self)
        self.diaslabel = QtWidgets.QLabel("Dias", self)
        self.canaislabel = QtWidgets.QLabel("Canais", self)
        self.hilabel = QtWidgets.QLabel("Hora inicial", self)
        self.hflabel = QtWidgets.QLabel("Hora final", self)
        self.fontelabel = QtWidgets.QLabel("Fonte", self)
        self.sensoreslabel = QtWidgets.QLabel("Sensores", self)
        
#Posições Labels
        self.proglabel.setGeometry(0, 0, 100, 50)
        self.diaslabel.setGeometry(0, 50, 100, 50)
        self.canaislabel.setGeometry(0, 100, 100, 50)
        self.hilabel.setGeometry(0, 150, 100, 50)
        self.hflabel.setGeometry(0, 200, 100, 50)
        self.fontelabel.setGeometry(0, 250, 100, 50)
        self.sensoreslabel.setGeometry(0, 300, 100, 50)
        
#Checkboxes dias
        
        self.dia = [QtWidgets.QCheckBox("ola", self)for i in range(7)]
        for i in range(7):
            self.dia[i].setGeometry(100, 50*i+50, 100, 50)
        self.dia0 = QtWidgets.QCheckBox("Domingo", self)
        self.dia1 = QtWidgets.QCheckBox("Segunda", self)
        self.dia2 = QtWidgets.QCheckBox("Terça", self)
        self.dia3 = QtWidgets.QCheckBox("Quarta", self)
        self.dia4 = QtWidgets.QCheckBox("Quinta", self)
        self.dia5 = QtWidgets.QCheckBox("Sexta", self)
        self.dia6 = QtWidgets.QCheckBox("Sábado", self)
        
#Checkboxes canais
        self.canais = [QtWidgets.QCheckBox(str(i+1), self)for i in range(12)]
        for i in range(6):
            self.canais[i].setGeometry(200, 50*i+50, 100, 50)
            self.canais[i+6].setGeometry(300, 50*i+50, 100, 50)

#Checkboxes sensores
        self.sensor1 = QtWidgets.QCheckBox("1", self)
        self.sensor2 = QtWidgets.QCheckBox("2", self)
        self.sensor1.setGeometry(400, 100, 100, 50)
        self.sensor2.setGeometry(400, 150, 100, 50)
        
#Selecionar Fonte
        self.fonte1 = QtWidgets.QRadioButton("Torneira", self)
        self.fonte2 = QtWidgets.QRadioButton("Bomba", self)
        self.fonte1.setGeometry(400, 200, 100, 50)
        self.fonte2.setGeometry(400, 250, 100, 50)
        

app = QtWidgets.QApplication(sys.argv)
main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_())
# Fechar a aplicação e sair do programa
