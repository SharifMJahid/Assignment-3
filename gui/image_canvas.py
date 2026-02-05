import cv2
from tkinter import Canvas
from utils.image_display import ImageDisplay
from utils.constants import BORDER_COLOR, DARK_BG, PLACE_HOLDER_TEXT, PRIMARY_COLOR, SUBTLE_TEXT, TEXT_FONT


class BaseCanvas:
    
    """
    This class is an abstract canvas base class defining render contract.
    
    """
    def _render(self):
        
        """
        This function renders the canvas content.

        Parameters: None
        Returns: None
        
        """
        raise NotImplementedError


class ImageCanvas(BaseCanvas):
    
    """
    This class is a Canvas responsible for displaying and scaling images.
    
    """

    def __init__(self, parent):
        
        """
        This initializes drawing canvas and bind the resize handling together.

        Parameters: parent (tkinter.Widget)
        Returns: None
        
        """

        self.canvas = Canvas(
            parent,
            bg=DARK_BG,
            highlightthickness=2,
            highlightbackground=BORDER_COLOR
        )
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tk_image = None
        self.cv_image = None
        self.on_upload_click = None
        self.zoom_percent = 100
        self.canvas.bind("<Configure>", self._on_resize)

    def update(self, image):
        
        """
        This function sets current image and triggers the re-render.

        Parameters: image (numpy.ndarray)
        Returns: None
        
        """
        self.cv_image = image
        self._render()

    def _on_resize(self, event):
        
        """
        This function re-renders the image when canvas size changes.

        Parameters: event (tkinter.Event)
        Returns: None
        
        """
        
        self._render()

    def _render(self):
        
        """
        This function draws the image scaled to fit with the canvas with zoom applied.

        Parameters: None
        Returns: None
        
        """
        
        self.canvas.delete("all")
    
        if self.cv_image is None:
            self._render_placeholder()
            return
    
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
    
        img_h, img_w = self.cv_image.shape[:2]
    
        # --- FIT TO SCREEN BASE SCALE ---
        fit_scale = min(canvas_w / img_w, canvas_h / img_h)
    
        # --- APPLY ZOOM ---
        zoom_scale = self.zoom_percent / 100
        scale = fit_scale * zoom_scale
    
        new_w = max(1, int(img_w * scale))
        new_h = max(1, int(img_h * scale))
    
        interpolation = cv2.INTER_LINEAR if scale > 1 else cv2.INTER_AREA
        resized = cv2.resize(self.cv_image, (new_w, new_h), interpolation=interpolation)
    
        self.tk_image = ImageDisplay.cv_to_tk(resized)
    
        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2
        self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)

    def _render_placeholder(self):
        
        
        """
        This function displays the upload placeholder when no image is loaded.

        Parameters: None
        Returns: None
        
        """
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            return

        center_y = h // 2
        gap = 18

        icon_id = self.canvas.create_text(
            w // 2, center_y - gap - 24,
            text="📤",
            font=(TEXT_FONT, 32),
            fill=PRIMARY_COLOR
        )

        text_id = self.canvas.create_text(
            w // 2, center_y + gap,
            text=PLACE_HOLDER_TEXT,
            font=(TEXT_FONT, 12),
            fill=SUBTLE_TEXT,
            justify="center"
        )

        for item in (icon_id, text_id):
            self.canvas.tag_bind(item, "<Button-1>", lambda e: self.on_upload_click() if self.on_upload_click else None)

    def set_zoom(self, percent: int):
        
        """
        This function updates the zoom percentage and re-renders the image.

        Parameters: percent (int)
        Returns: None
        
        """
        
        self.zoom_percent = percent
        if self.cv_image is not None:
            self._render()