import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout , QDoubleSpinBox, QHBoxLayout
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon
from PySide2.QtGui import QFont
import numpy as np

FONT = QFont("Times New Roman", 12 , QFont.Bold)
MIN_RANGE = -10000
MAX_RANGE = 10000
# replacement expressions for math functions
replacementExpressions = {
    'sin': 'np.sin',
    'cos': 'np.cos',
    'tan': 'np.tan',
    'asin': 'np.arcsin',
    'acos': 'np.arccos',
    'atan': 'np.arctan',
    'sinh': 'np.sinh',
    'cosh': 'np.cosh',
    'tanh': 'np.tanh',
    'asinh': 'np.arcsinh',
    'acosh': 'np.arccosh',
    'atanh': 'np.arctanh',
    'log': 'np.log',
    'log10': 'np.log10',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    'pi': 'np.pi',
    'e': 'np.e',
    '^': '**',
}
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setWindowGeometry()
        # set the window icon
        self.setIcon()
        # Create the input widgets
        self.setInputWidgets()
        # Create the plot button
        self.setPlotButton()
        # Create a Matplotlib figure and add it to the layout
        self.figure = plt.figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.canvas.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.setLayout()
        self.statusBar().showMessage("Ready...")
        self.statusBar().setFont(FONT)
        self.statusBar().setStyleSheet("color: green")
        self.setContentsMargins(0, 10, 0, 10)
    # set input widgets
    def setInputWidgets(self):
        
        # Create input widgets
        self.function_label = QLabel("f(x):")
        self.function_label.setFont(FONT)
        self.function_input = QLineEdit()
        self.min_label = QLabel("x min:")
        self.min_label.setFont(FONT)
        self.min_input = QDoubleSpinBox()
        self.min_input.setRange(MIN_RANGE, MAX_RANGE)
        self.max_label = QLabel("x max:")
        self.max_label.setFont(FONT)
        self.max_input = QDoubleSpinBox()
        self.max_input.setRange(MIN_RANGE, MAX_RANGE)
    # set layout
    def setLayout(self):
        
        # Create a central widget and a vertical layout for it
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vertical_layout = QVBoxLayout()
        central_widget.setLayout(vertical_layout)
        
        # Add input widgets to the layout
        horizontal_layout_function_box = QHBoxLayout()
        horizontal_layout_function_box.addWidget(self.function_label)
        horizontal_layout_function_box.addWidget(self.function_input)
        horizontal_layout_function_box.setContentsMargins(0, 10, 0, 10)
        vertical_layout.addLayout(horizontal_layout_function_box)
        horizontal_layout_min_box = QHBoxLayout()
        horizontal_layout_min_box.addWidget(self.min_label)
        horizontal_layout_min_box.addWidget(self.min_input)
        horizontal_layout_max_box = QHBoxLayout()
        horizontal_layout_max_box.addWidget(self.max_label)
        horizontal_layout_max_box.addWidget(self.max_input)
        horizontal_layout_min_max_box = QHBoxLayout()
        horizontal_layout_min_max_box.addLayout(horizontal_layout_min_box)
        horizontal_layout_min_max_box.addLayout(horizontal_layout_max_box)
        vertical_layout.addLayout(horizontal_layout_min_max_box)
        
        # Add the plot button to the layout
        vertical_layout.addWidget(self.plot_button)
        
        # Add the toolbar to the layout
        vertical_layout.addWidget(self.toolbar)
        
        # Add the plot figure to the layout
        vertical_layout.addWidget(self.canvas)
    # set the window icon
    def setIcon(self):
        appIcon = QIcon("Icon.png")
        self.setWindowIcon(appIcon)
    # set Button
    def setPlotButton(self):
        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot)
    # set the window Geometry
    def setWindowGeometry(self):
        self.setGeometry(700,700,700,700)
        self.setMinimumHeight(500)
        self.setMaximumHeight(1000)
        self.setMinimumWidth(500)
        self.setMaximumWidth(1000)
    @Slot()
    def plot(self):
        error = False
        # Get the user inputs
        f_x = self.function_input.text()
        x_min = self.min_input.text()
        x_max = self.max_input.text()

        # Validate the user inputs
        # Check if the function is empty or x min is empty or x max is empty
        if f_x == "" or x_min == "" or x_max == "":
            self.statusBar().showMessage("Invalid input the function or x min or x max is empty")
            self.statusBar().setStyleSheet("color: red")
            error = True
            self.figure.clear()
            return
        try:
            x_min = float(x_min)
            x_max = float(x_max)
        except:
            self.statusBar().showMessage("x min and x max must be numbers")
            self.statusBar().setStyleSheet("color: red")
            error = True
            self.figure.clear()
            return
        if x_min >= x_max:
            self.statusBar().showMessage("x min must be less than x max")
            self.statusBar().setStyleSheet("color: red")
            self.figure.clear()
            return
        # evaluate the user function
        x_array_val ,y_array_values = self.evaluateFunction(f_x, x_min, x_max)
        # Check if the function is valid
        if x_array_val == "invalid" and y_array_values == "invalid" :
            self.figure.clear()
            return
        
        self.statusBar().showMessage("Ready...")
        self.statusBar().setStyleSheet("color: green")
        # Clear the previous figure
        
        self.figure.clear()
        # Add a subplot to the figure and plot the function
        ax = self.figure.add_subplot(111)
        ax.plot(x_array_val, y_array_values)
        ax.set_title(f"Function Plot: {f_x}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Draw the plot
        self.canvas.draw()
    # evaluate the function
    def evaluateFunction(self, f_x, x_min, x_max):
        
        # Replace the math functions with numpy functions
        f_x = f_x.replace(" ", "")
        f_x = f_x.lower()
        for key, value in replacementExpressions.items():
            f_x = f_x.replace(key, value)
        # Create a list of x values and evaluate the function for each x value
        x_array_val = []
        y_array_val = []
        x = x_min
        while x <= x_max:
            try:
                y = eval(f_x)
                y_array_val.append(y)
                x_array_val.append(x)
            except:
                self.statusBar().showMessage("Invalid function")
                self.statusBar().setStyleSheet("color: red")
                return "invalid","invalid"
            x += 0.01
        return x_array_val, y_array_val

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())