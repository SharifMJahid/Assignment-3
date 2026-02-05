from tkinter import Label, SUNKEN, W, X, BOTTOM

class StatusBar:
    
    """
    This class provides for Bottom status bar which displays editor messages.
    
    """
    
    def __init__(self, root):
        
        
        """
        This function creates a status label and attaches to the main window.

        Parameters: root (tkinter.Tk)
        Returns: None
        
        """
        self.label = Label(root, text="No image loaded", bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(side=BOTTOM, fill=X)

    def update(self, text: str):
        
        """
        This function updates the text for the status bar.

        Parameters: text (str)
        Returns: None
        
        """
        
        self.label.config(text=text)
