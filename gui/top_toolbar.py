from tkinter import Frame, Button, Label, Scale, HORIZONTAL
from utils.constants import BORDER_COLOR, BTN_BG, DANGER_COLOR, PRIMARY_COLOR, TOOL_BAR_BG


class TopToolbar:
    
    """
    This is a class which provides top toolbar its undo/redo controls and image zoom adjustment.
    
    """
    
    def __init__(self, parent, controller):
        
        """
        This function creates a toolbar layout and binds the controls to controller actions.

        Parameters: parent (tkinter.Widget), controller (object)
        Returns: None
        
        """

        # ===== Main toolbar frame =====
        self.frame = Frame(
            parent,
            bg=TOOL_BAR_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )
        self.frame.pack(side="top", fill="x")

        # ===== LEFT GROUP (Undo / Redo) =====
        left_group = Frame(self.frame, bg=TOOL_BAR_BG)
        left_group.pack(side="left", padx=15)

        Button(left_group, text="Undo", command=controller.undo, width=6)\
            .pack(side="left", padx=5, pady=5)

        Button(left_group, text="Redo", command=controller.redo, width=6)\
            .pack(side="left", padx=5)

        # ===== SPACER (push resize section right) =====
        Frame(self.frame, bg=TOOL_BAR_BG).pack(side="left", expand=True)

        # ===== RIGHT GROUP (Resize section) =====
        right_group = Frame(self.frame, bg=TOOL_BAR_BG)
        right_group.pack(side="right", padx=15)

        # Zoom % label (LEFT of slider)
        self.zoom_label = Label(
            right_group,
            text="100%",
            bg=TOOL_BAR_BG,
            font=("Segoe UI", 9)
        )
        self.zoom_label.pack(side="left", padx=(0, 5))

        # Zoom slider
        self.slider = Scale(
            right_group,
            from_=10,
            to=200,
            orient=HORIZONTAL,
            length=150,
            bg=BTN_BG,
            sliderlength=18,
            bd=0,
            relief="flat",
            showvalue=0,
            command=self._on_slide
        )
        self.slider.set(100)
        self.slider.pack(side="left", padx=(0, 10), pady=5)

        # Apply resize button
        Button(
            right_group,
            text="Apply Resize",
            command=lambda: controller.resize(self.slider.get()),
            width=12,
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat"
        ).pack(side="left", padx=(0, 8))
        
    # ===== CONTROLLER SYNC METHOD =====
    def set_zoom(self, value: int):
        
        """
        This function updates the slider and labels it to reflect current zoom level.

        Parameters: value (int)
        Returns: None
        
        """
        
        self.slider.set(value)
        self.zoom_label.config(text=f"{value}%")

    # ===== SLIDER LIVE UPDATE =====
    def _on_slide(self, val):
        
        """
        This function updates the zoom label when the slider moves.

        Parameters: val (str | float)
        Returns: None
        
        """
        
        self.zoom_label.config(text=f"{int(float(val))}%")
