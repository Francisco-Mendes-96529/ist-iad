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

# MainWindow
        self.setWindowTitle("Trabalho 2 - Sistema de Rega")
        # Dimensões
        self.setMinimumSize(900,500)
        self.setMaximumSize(900,500)
        # Centrar janela no ecrã
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


# Drop down list Programas
        self.progList = QtWidgets.QComboBox(self)
        self.progList.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"])
        self.progList.setGeometry(490, 0, 50, 50)
# Labels    
        self.progLabel = QtWidgets.QLabel("Programa", self)
        self.diasLabel = QtWidgets.QLabel("Dias", self)
        self.canaisLabel = QtWidgets.QLabel("Canais", self)
        self.hiLabel = QtWidgets.QLabel("Início:", self)
        self.hfLabel = QtWidgets.QLabel("Fim:", self)
        self.fonteLabel = QtWidgets.QLabel("Fonte", self)
        self.sensoresLabel = QtWidgets.QLabel("Sensores", self)
        self.doisPontosI = QtWidgets.QLabel(":", self)
        self.doisPontosF = QtWidgets.QLabel(":", self)

# Posições Labels
        self.progLabel.setGeometry(375, 0, 100, 50)
        self.diasLabel.setGeometry(100, 50, 100, 50)
        self.canaisLabel.setGeometry(733, 50, 100, 50)
        self.hiLabel.setGeometry(330, 100, 100, 50)
        self.hfLabel.setGeometry(330, 165, 100, 50)
        self.sensoresLabel.setGeometry(400, 240, 100, 50)
        self.fonteLabel.setGeometry(415, 340, 100, 50)
        
# Checkboxes dias
        diaName = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.dia = [QtWidgets.QCheckBox(diaName[i], self)for i in range(7)]
        for i in range(7):
            self.dia[i].setGeometry(75, 50*i+100, 110, 50)
        
# Checkboxes canais
        self.canais = [QtWidgets.QCheckBox(str(i+1), self)for i in range(12)]
        for i in range(6):
            self.canais[i].setGeometry(710, 50*i+100, 100, 50)
            self.canais[i+6].setGeometry(790, 50*i+100, 100, 50)

# Checkboxes sensores
        self.sensor = [QtWidgets.QCheckBox(str(i+1), self)for i in range(2)]
        self.sensor[0].setGeometry(380, 280, 100, 50)
        self.sensor[1].setGeometry(480, 280, 100, 50)
        
# Selecionar Fonte
        self.fonte1 = QtWidgets.QRadioButton("Torneira", self)
        self.fonte2 = QtWidgets.QRadioButton("Bomba", self)
        self.fonte1.setGeometry(325, 380, 100, 50)
        self.fonte2.setGeometry(465, 380, 100, 50)

# Hora inicial e final
        self.horaInicial = QtWidgets.QSpinBox(self)
        self.minInicial = QtWidgets.QSpinBox(self)
        self.horaFinal = QtWidgets.QSpinBox(self)
        self.minFinal = QtWidgets.QSpinBox(self)
        self.horaInicial.setGeometry(400,100,65,50)
        self.minInicial.setGeometry(480,100,65,50)
        self.doisPontosI.setGeometry(465,100,15,50)
        self.doisPontosI.setAlignment(QtCore.Qt.AlignCenter)
        self.horaFinal.setGeometry(400,165,65,50)
        self.minFinal.setGeometry(480,165,65,50)
        self.doisPontosF.setGeometry(465,165,15,50)
        self.doisPontosF.setAlignment(QtCore.Qt.AlignCenter)
        self.horaInicial.setRange(0,23)
        self.minInicial.setRange(0,59)
        self.horaFinal.setRange(0,23)
        self.minFinal.setRange(0,59)
        self.horaInicial.setAlignment(QtCore.Qt.AlignCenter)
        self.horaFinal.setAlignment(QtCore.Qt.AlignCenter)
        self.minInicial.setAlignment(QtCore.Qt.AlignCenter)
        self.minFinal.setAlignment(QtCore.Qt.AlignCenter)

# Botões Guardar e Ativo
        self.guardar = QtWidgets.QPushButton("Guardar",self)
        self.guardar.setGeometry(760,420,100,50)
        self.ativo = QtWidgets.QPushButton("OFF",self)
        self.ativo.setCheckable(True)
        self.ativo.setGeometry(680,420,70,50)
        self.ativo.clicked.connect(self.on_off)
        self.ativo.setStyleSheet("background-color : rgb(255,100,100)") # set background color to red
        
    def on_off(self):
        if self.ativo.isChecked():
            # setting background color to green
            self.ativo.setStyleSheet("background-color : green")
            self.ativo.setText("ON")
        else:
            # set background color back to red
            self.ativo.setStyleSheet("background-color : rgb(255,100,100)")
            self.ativo.setText("OFF")
   

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QLabel{font-size: 14pt;}" "QComboBox{font-size: 12pt;}" "QCheckBox{font-size: 12pt;}" "QRadioButton{font-size: 12pt;}" "QSpinBox{font-size: 12pt;}" "QPushButton{font-size: 12pt;}")

main = MainWindow()
main.show()  # Mostrar a janela
sys.exit(app.exec_()) # Fechar a aplicação e sair do programa