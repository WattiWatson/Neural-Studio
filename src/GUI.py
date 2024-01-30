'''
    Placeholder GUI but at least gives us something
'''

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QLabel, QPushButton
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neural Network Trainer")
        self.resize(1200, 800)

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create the sliders
        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        self.slider1.setMaximum(8)
        self.slider1.valueChanged.connect(self.slider1_changed)
        self.slider1.setMaximumWidth(400)

        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.slider2.setMaximum(8)
        self.slider2.valueChanged.connect(self.slider2_changed)
        self.slider2.setMaximumWidth(400)

        # Create the labels
        self.label1 = QLabel("Number of Neurons: 0")
        self.label2 = QLabel("Number of Hidden Layers: 0")

        # Create the button
        self.button = QPushButton("Train")
        self.button.clicked.connect(self.button_clicked)
        self.button.setMaximumWidth(200)

        # Create a QHBoxLayout for the sliders and button
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label1)
        hlayout.addWidget(self.slider1)
        hlayout.addWidget(self.label2)
        hlayout.addWidget(self.slider2)
        hlayout.addWidget(self.button)
        hlayout.addStretch(1)

        # Add a stretch factor to the layout
        layout.addStretch(1)

        # Add the QHBoxLayout to the QVBoxLayout
        layout.addLayout(hlayout)

        # Create a QWidget and set the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the MainWindow
        self.setCentralWidget(widget)

    def slider1_changed(self, value):
        self.label1.setText(f"Number of Neurons: {value}")

    def slider2_changed(self, value):
        self.label2.setText(f"Number of Hidden Layers: {value}")

    def button_clicked(self):
        print("Train button clicked")
