import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon

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
        self.setLayout()
        
    # create the input widgets
    def setInputWidgets(self):
        # Create input widgets
        self.function_label = QLabel("f(x):")
        self.function_input = QLineEdit()
        self.min_label = QLabel("x min:")
        self.min_input = QLineEdit()
        self.max_label = QLabel("x max:")
        self.max_input = QLineEdit()
    # set layout
    def setLayout(self):
        # Create a central widget and a vertical layout for it
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vertical_layout = QVBoxLayout()
        central_widget.setLayout(vertical_layout)
        
        # Add input widgets to the layout
        vertical_layout.addWidget(self.function_label)
        vertical_layout.addWidget(self.function_input)
        vertical_layout.addWidget(self.min_label)
        vertical_layout.addWidget(self.min_input)
        vertical_layout.addWidget(self.max_label)
        vertical_layout.addWidget(self.max_input)
        # Add the plot button to the layout
        vertical_layout.addWidget(self.plot_button)
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
        # Get the user inputs
        f_x = self.function_input.text()
        x_min = self.min_input.text()
        x_max = self.max_input.text()

        # Validate the user inputs
        # Check if the function is empty or x min is empty or x max is empty
        if f_x == "" or x_min == "" or x_max == "":
            self.statusBar().showMessage("Invalid input the function or x min or x max is empty")
            return
        try:
            x_min = float(x_min)
            x_max = float(x_max)
        except:
            self.statusBar().showMessage("x min and x max must be numbers")
            return
        if x_min >= x_max:
            self.statusBar().showMessage("x min must be less than x max")
        
        # evaluate the user function
        x_array_val ,y_array_values = self.evaluateFunction(f_x, x_min, x_max)
        # Check if the function is valid
        if x_array_val == "invalid" and y_array_values == "invalid":
            return
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
                return "invalid","invalid"
            x += 0.01
        return x_array_val, y_array_val

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())