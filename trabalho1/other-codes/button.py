import sys
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot

# Greetings
@pyqtSlot()
def say_hello():
    print("Button clicked, Hello!")
    
# Create the Qt Application
app = QApplication(sys.argv)

# Create a button
button = QPushButton("Click me")

# Connect the button to the function
button.clicked.connect(say_hello)

# Show the button
button.show()
# Run the main Qt loop
app.exec_()