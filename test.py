import sys
import pytest
from PySide2.QtWidgets import QApplication
from function_plotter import MainWindow
from PySide2.QtCore import Qt

@pytest.fixture
def window(qtbot):
    # Create an instance of the MainWindow class
    window = MainWindow()
    # Add the MainWindow instance to the QtBot for testing
    qtbot.addWidget(window)
    # Return the MainWindow instance for testing
    return window

def test_window_title(window):
    """Test that the Window has the correct title."""
    assert window.windowTitle() == "Function Plotter"

def test_window_widgets(window):
    """Test that the Window has the correct labels."""
    assert window.function_label.text() == "f(x):"
    assert window.min_label.text() == "x min:"
    assert window.max_label.text() == "x max:"
    assert window.plot_button.text() == "Plot"

def test_window_plot(qtbot, window):
    """Test that the plot button works correctly."""
    # Set the input values
    window.function_input.setText("x**2")
    window.min_input.setValue(-5)
    window.max_input.setValue(5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the plot was created
    assert window.figure.axes[0].lines[0].get_ydata().tolist()[0] == 25.0
    
def test_window_plot_error(qtbot, window):
    """Test that the plot button works correctly."""
    # Set the input values
    window.function_input.setText("x**2")
    window.min_input.setValue(5)
    window.max_input.setValue(-5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the plot was created
    assert window.statusBar().currentMessage() == "x min must be less than x max"

def test_window_statusbar(qtbot, window):
    """Test that the status bar is green when ready."""
    # Set the input values
    window.function_input.setText("x**2")
    window.min_input.setValue(-5)
    window.max_input.setValue(5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the status bar is green
    assert window.statusBar().styleSheet() == "color: green"
    assert window.statusBar().currentMessage() == "Ready..."

def test_window_statusbar_error(qtbot, window):
    """Test that the status bar is red when there is an error."""
    # Set the input values
    window.function_input.setText("x**2")
    window.min_input.setValue(5)
    window.max_input.setValue(-5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the status bar is red
    assert window.statusBar().styleSheet() == "color: red"
    assert window.statusBar().currentMessage() == "x min must be less than x max"

def test_window_statusbar_invalid_function_error(qtbot, window):
    """Test that the status bar is red when there is an error. and the function is invalid"""
    # set the input values
    window.function_input.setText("2x")
    window.min_input.setValue(-5)
    window.max_input.setValue(5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the status bar is red
    assert window.statusBar().styleSheet() == "color: red"
    assert window.statusBar().currentMessage() == "Invalid function"

def test_window_plot_title(qtbot, window):
    """Test that plot title."""
    # Set the input values
    window.function_input.setText("sin(x) + 5")
    window.min_input.setValue(-5)
    window.max_input.setValue(5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the plot title is np.sin(x)
    assert window.figure.axes[0].get_title() == "Function Plot: sin(x) + 5"
    
def test_window_replacement_expression(qtbot, window):
    """Test that the replacement_expression work correctly."""
    # Set the input values
    window.function_input.setText("x^2")
    window.min_input.setValue(-5)
    window.max_input.setValue(5)
    # Click the plot button
    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    # Check that the status bar is green
    assert window.statusBar().styleSheet() == "color: green"
    assert window.statusBar().currentMessage() == "Ready..."
    assert window.figure.axes[0].lines[0].get_ydata().tolist()[0] == 25.0