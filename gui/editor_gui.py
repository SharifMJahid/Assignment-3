from tkinter import Frame, filedialog, messagebox, simpledialog
from core.image_processor import ImageProcessor
from core.history_manager import HistoryManager
from gui.image_canvas import ImageCanvas
from gui.control_panel import ControlPanel
from gui.status_bar import StatusBar
from gui.menu_bar import MenuBar
from gui.top_toolbar import TopToolbar


class ImageEditorGUI:
    
    """
    This is the main GUI controller which connects UI components with image processing logic.
    
    """

    def __init__(self, root):
        
        """
        This is to initialize editor, UI layout, and core components.
        
        Parameters: root (tkinter.Tk)
        Returns: None
        
        """
        
        self.processor = ImageProcessor()
        self.history = HistoryManager()

        MenuBar(root, self)

        main = Frame(root)
        main.pack(fill="both", expand=True)
        
        self.top_toolbar  = TopToolbar(main,self)

        self.canvas = ImageCanvas(main)
        self.canvas.on_upload_click = self.open_file_dialog

        self.controls = ControlPanel(main, self)
        self.status = StatusBar(root)

        self.current_scale = 100

    def open_file_dialog(self):
        
        """
        This function opens file picker and load the selected image.

        Parameters: None
        Returns: None
        
        """
        path = filedialog.askopenfilename()
        if path:
            self.load_image(path)

    def load_image(self, path):
        
        """
        This function loads an image, reset the history, and refresh the UI.

        Parameters: path (str)
        Returns: None
        
        """
        self.processor.load(path)
        self.history.clear()
        self.current_scale = 100
        self.canvas.set_zoom(100)
        self.top_toolbar.set_zoom(100)
        self.update_ui()
        
    def save_image(self, path):
        
        """
        This function saves current image to disk.

        Parameters: path (str)
        Returns: None
        
        """
        self.processor.save(path)

    def update_ui(self):
        
        """
        This function refreshes canvas display and the status information.

        Parameters: None
        Returns: None
        
        """
        img = self.processor.image
        self.canvas.update(img)
        h, w = img.shape[:2]
        self.status.update(f"Image Loaded | {w} x {h} | Zoom: {self.current_scale}%")

    def apply(self, func, *args):
        
        """
        This function saves the state, execute processing function, and update the UI.

        Parameters: func (callable), *args (tuple)
        Returns: None
        
        """
        # Polymorphism: apply() accepts any callable with different behaviors ✅
        self.history.save(self.processor.image, self.current_scale)
        func(*args)
        self.update_ui()

    # delegates
    def grayscale(self): 
        
        """
        This function applies the grayscale filter if the image exists.

        Parameters: None
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.grayscale)

    def edge(self): 
        
        """
        This function applies the edge detection filter if image exists.

        Parameters: None
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.edge)
        
    def brightness(self, v): 
        
        """
        This function adjusts the brightness level.

        Parameters: v (int)
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.brightness, v)
        
    def contrast(self, a):
        
        """
        This function adjusts the contrast level.

        Parameters: a (float)
        Returns: None
        
        """ 
        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.contrast, a)
        
    def rotate(self, a): 
        
        """
        This function rotates the image by given angle.

        Parameters: a (int)
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.rotate, a)
        
    def flip(self, m): 
        
        """
        This function flips the image horizontally or vertically.

        Parameters: m (str)
        Returns: None
        
        """

        
        if not self.validate_image_available():
            return
        
        self.apply(self.processor.flip, m)

    def resize(self, percent: int):
        
        """
        This function changes zoom scale without changing the original image.

        Parameters: percent (int)
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        self.history.save(self.processor.image, self.current_scale)
        self.current_scale = percent        
        self.canvas.set_zoom(percent)         
        # Sync sliders
        self.top_toolbar.set_zoom(percent)

        self.status.update(f"Zoom: {percent}%")

    def undo(self):
        
        """
        This function restores the previous state from the history.

        Parameters: None
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        
        state = self.history.undo(self.processor.image, self.current_scale)
        if state:
            image, scale = state
            self.processor._current = image
            self.current_scale = scale
            self.top_toolbar.set_zoom(scale)
            self.canvas.set_zoom(scale)
            self.update_ui()

    def redo(self):
        
        """
        This function reapplies previously undone state of the image.

        Parameters: None
        Returns: None
        
        """
        if not self.validate_image_available():
            return
        state = self.history.redo(self.processor.image, self.current_scale)
        if state:
            image, scale = state
            self.processor._current = image
            self.current_scale = scale
            self.top_toolbar.set_zoom(scale)
            self.canvas.set_zoom(scale)
            self.update_ui()
            
    def reset_image(self):
        
        """
        This function resets the image to original state and clear the history.

        Parameters: None
        Returns: None
        
        """
        if not self.validate_image_available():
            return
        self.processor.reset()   
        self.history.clear()        
        self.current_scale = 100     
        self.top_toolbar.slider.set(100) 
        self.top_toolbar.set_zoom(100)
        self.canvas.set_zoom(100)
        self.update_ui()      

    def blur(self):
        
        """
        This function prompts the blur intensity and applies the blur filter.

        Parameters: None
        Returns: None
        
        """
        
        if not self.validate_image_available():
            return
        value = simpledialog.askinteger("Blur", "Intensity (1–20):", minvalue=1, maxvalue=20)
        if value:
            self.apply(self.processor.blur, value)
    
    def validate_image_available(self):
        
        """
        THis function checks if the image is loaded before processing.

        Parameters: None
        Returns: bool
        
        """
        if self.processor._original is None:
            messagebox.showinfo("No image", "Load an image first.")
            return False
        return True
        
        
