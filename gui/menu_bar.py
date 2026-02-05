from tkinter import Menu, filedialog, messagebox
from utils.constants import SUPPORTED_FORMATS, DEFAULT_SAVE_NAME


class MenuBar:
    
    """
    This class is an application menu bar which handles the file operations.
    
    """
    
    def __init__(self, root, controller):
        
        """
        This function creates the menu structure and binds the file actions.

        Parameters: root (tkinter.Tk), controller (object)
        Returns: None
        
        """
        
        self.controller = controller
        menubar = Menu(root)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        menubar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menubar)

    def open_file(self):
        
        """
        This function opens the file dialog and loads the selected image.

        Parameters: None
        Returns: None
        
        """
        
        path = filedialog.askopenfilename(filetypes=SUPPORTED_FORMATS)
        if path:
            try:
                self.controller.load_image(path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save(self):
        
        """
        This function saves the image using the default filename.

        Parameters: None
        Returns: None
        
        """
        
        try:
            self.controller.save_image(DEFAULT_SAVE_NAME)
            messagebox.showinfo("Saved", "Image saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as(self):
        
        """
        This function opens the save dialog and saves the image into chosen path.

        Parameters: None
        Returns: None
        
        """
        
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            try:
                self.controller.save_image(path)
            except Exception as e:
                messagebox.showerror("Error", str(e))
