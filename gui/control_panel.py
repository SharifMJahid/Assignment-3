from tkinter import Frame, Button, Label, LabelFrame, messagebox
from utils.base_component import BaseComponent, ClickableMixin
from utils.constants import (
    BORDER_COLOR,
    BTN_BG,
    BTN_HOVER,
    DANGER_COLOR,
    INFO_COLOR,
    PANEL_BG,
)


class ControlPanel(ClickableMixin, BaseComponent):
    
    """
    This UI panel contains buttons that trigger image editing actions by the controller.
     
    """

    SECTION_COLORS = {
        "Basic Filters": "#E3F2FD",   # soft blue
        "Adjustments": "#FFF3E0",     # soft orange
        "Transform": "#F3E5F5",       # soft purple
    }

    def __init__(self, parent, controller):
        
        """
        This creates control panel layout and bind buttons to controller actions.

        Parameters: parent (tkinter.Widget), controller (object)
        Returns: None
        """
        super().__init__(controller)

        # Main panel frame
        frame = Frame(parent, width=260, bg=PANEL_BG,
                      highlightbackground=BORDER_COLOR, highlightthickness=1)
        frame.pack(side="right", fill="y", padx=10)
        frame.pack_propagate(False)

        # ===== Create sections =====
        basic_box = self._make_section(frame, "Basic Filters")
        adjust_box = self._make_section(frame, "Adjustments")
        transform_box = self._make_section(frame, "Transform")

        # ===== BASIC FILTERS =====
        self._fill_section(basic_box, [
            ("Grayscale", controller.grayscale, "Converts image to black and white."),
            ("Blur", controller.blur, "Smooths the image to reduce noise."),
            ("Edge", controller.edge, "Detects edges in the image."),
        ])

        # ===== ADJUSTMENTS =====
        self._fill_section(adjust_box, [
            ("Bright -", lambda: controller.brightness(-30), "Decreases brightness."),
            ("Bright +", lambda: controller.brightness(30), "Increases brightness."),
            ("Contrast -", lambda: controller.contrast(0.8), "Reduces contrast."),
            ("Contrast +", lambda: controller.contrast(1.2), "Increases contrast."),
        ])

        # ===== TRANSFORM =====
        self._fill_section(transform_box, [
            ("Rotate 90", lambda: controller.rotate(90), "Rotates image 90 degrees."),
            ("Rotate 180", lambda: controller.rotate(180), "Rotates image upside down."),
            ("Rotate 270", lambda: controller.rotate(270), "Rotates image 270 degrees."),
            ("Flip H", lambda: controller.flip("horizontal"), "Flips image horizontally."),
            ("Flip V", lambda: controller.flip("vertical"), "Flips image vertically."),
        ])

        # Reset button
        Button(frame, text="Reset",
               command=controller.reset_image,
               width=18, bg=DANGER_COLOR, fg="white", relief="flat")\
            .pack(pady=15)

    # ===== Create section container =====
    def _make_section(self, parent, title: str):
        
        """
        This creates a labeled section container.

        Parameters: parent (tkinter.Widget), title (str)
        Returns: tkinter.LabelFrame
        """
        bg = self.SECTION_COLORS.get(title, "white")
        box = LabelFrame(parent, text=title, padx=6, pady=6, bg=bg)
        box.pack(fill="x", pady=6, padx=6)
        return box

    # ===== Fill section with buttons =====
    def _fill_section(self, box, actions):
        
        """
        This function adds an action buttons with info popups in a section.

        Parameters: box (tkinter.LabelFrame), actions (list[tuple[str, callable, str]])
        Returns: None
        """
        for text, cmd, desc in actions:
            row_frame = Frame(box, bg=box["bg"])
            row_frame.pack(fill="x", pady=2)

            btn = Button(row_frame, text=text, command=cmd, width=18,
                         relief="flat", bg=BTN_BG,
                         activebackground=BTN_HOVER, cursor="hand2")
            btn.pack(side="left", padx=4)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_BG))

            info_btn = Button(
                row_frame,
                text="i",
                width=2,
                relief="flat",
                bg=BTN_BG,
                fg=INFO_COLOR,
                cursor="hand2",
                command=lambda d=desc, t=text: messagebox.showinfo(t, d)
            )
            info_btn.pack(side="left")
