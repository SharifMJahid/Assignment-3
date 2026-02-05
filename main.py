from tkinter import Tk
from gui.editor_gui import ImageEditorGUI
from utils.constants import WINDOW_TITLE, WINDOW_SIZE

"""
This file is an application entry point which initializes the main window and launches the Image Editor GUI.

This script sets up the root Tkinter window by using predefined constants and it also creates the main GUI controller, and starts the event loop.

"""

if __name__ == "__main__":
    
    """
    This function starts the application and run the Tkinter main event loop for the entire program to operate.
    
    """
    
    root = Tk()
    root.title(WINDOW_TITLE)
    root.geometry(WINDOW_SIZE)
    ImageEditorGUI(root)
    root.mainloop()
