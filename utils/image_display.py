import cv2
from PIL import Image, ImageTk


class ImageDisplay:
    """
    This class is responsible for displaying images in the Tkinter GUI.
    """

    @staticmethod
    def cv_to_tk(image):
        """
        This function converts an OpenCV image into a Tkinter compatible PhotoImage.

        Parameters:
            image: An OpenCV image represented as a NumPy array (BGR format).

        Returns:
            A Tkinter PhotoImage object if an image is provided,
            otherwise None.
        """
        if image is None:
            return None

        # Convert from OpenCV BGR format to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert NumPy array to a Tkinter Photoimage
        return ImageTk.PhotoImage(Image.fromarray(rgb))
