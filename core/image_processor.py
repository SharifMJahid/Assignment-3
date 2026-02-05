import cv2
import numpy as np
from utils.models import Size


class ImageProcessor:
    """
    This is a helper class for doing common image edits with OpenCV.
    """

    SUPPORTED_ROTATIONS = {90, 180, 270}

    def __init__(self):
        """
        This function creates a new ImageProcessor instance with no image loaded yet.
        """
        self._original: np.ndarray | None = None
        self._current: np.ndarray | None = None

    def __repr__(self) -> str:
        """
        This function provides a short, readable summary.

        Returns:
            str: A string showing whether an image is loaded.
        """
        loaded = self._current is not None
        return f"ImageProcessor(loaded={loaded})"

    # ---- decorators ----
    @property
    def image(self) -> np.ndarray:
        """
        This function gets the current image.

        Returns:
            np.ndarray: The current edited image.

        Raises:
            ValueError: If no image has been loaded yet.
        """
        self._ensure_loaded()
        return self._current

    @classmethod
    def from_file(cls, path: str) -> "ImageProcessor":
        """
        This function create an ImageProcessor and load an image in one step.

        Parameter:
            path (str): Path to the image file.

        Returns:
            ImageProcessor: A ready-to-use instance with the image loaded.

        Raises:
            ValueError: If the path is invalid or the image can't be read.
        """
        obj = cls()
        obj.load(path)
        return obj

    def _ensure_loaded(self):
        """
        This function make sure an image is loaded before doing any edits.

        Raises:
            ValueError: If image not loaded.
        """
        if self._current is None:
            raise ValueError("No image loaded.")

    def _ensure_valid_path(self, path: str):
        """
        This function make sure the given file path looks valid.

        Parameter:
            path (str): File path to validate.

        Raises:
            ValueError: If the path is empty or not a string.
        """
        if not path or not isinstance(path, str):
            raise ValueError("Invalid file path.")

    def load(self, path: str):
        """
        This function loads an image from disk.

        Parameters:
            path (str): Path to the image file.

        Returns:
            None

        Raises:
            ValueError: If the path is invalid or the file can't be read.
        """
        self._ensure_valid_path(path)
        image = cv2.imread(path)
        if image is None:
            raise ValueError("Unsupported or corrupted image file.")
        self._original = image
        self._current = image.copy()

    def save(self, path: str):
        """
        This function saves the current working image to disk.

        Parameters:
            path (str): Output file path (including filename and extension).

        Returns:
            None

        Raises:
            ValueError: If no image is loaded, the path is invalid,
                        or OpenCV fails to write the file.
        """
        self._ensure_loaded()
        self._ensure_valid_path(path)
        if not cv2.imwrite(path, self._current):
            raise ValueError("Failed to save image.")

    def reset(self):
        """
        This function reset the working image back to the original.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded.
        """
        self._ensure_loaded()
        self._current = self._original.copy()

    def grayscale(self):
        """
        This function converts the current image to grayscale.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded.
        """
        self._ensure_loaded()
        gray = cv2.cvtColor(self._current, cv2.COLOR_BGR2GRAY)
        self._current = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def blur(self, intensity: int):
        """
        This function apply Gaussian blur to the current image.

        Parameters:
            intensity (int): Blur strength (0 means almost no blur).

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or intensity is invalid.
        """
        self._ensure_loaded()
        if not isinstance(intensity, int) or intensity < 0:
            raise ValueError("Blur intensity must be a non-negative integer.")
        k = intensity * 2 + 1
        self._current = cv2.GaussianBlur(self._current, (k, k), 0)

    def edge(self):
        """
        This function detect edges using Canny and show them as a BGR image.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded.
        """
        self._ensure_loaded()
        edges = cv2.Canny(self._current, 100, 200)
        self._current = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def brightness(self, value: int):
        """
        This function make the image brighter or darker.

        Parameters:
            value (int): Positive to brighten, negative to darken.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or value is not an integer.
        """
        self._ensure_loaded()
        if not isinstance(value, int):
            raise ValueError("Brightness value must be an integer.")
        hsv = cv2.cvtColor(self._current, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = np.clip(v.astype(np.int16) + value, 0, 255).astype(np.uint8)
        self._current = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    def contrast(self, alpha: float):
        """
        This function change the contrast of the current image.

        Parameters:
            alpha (float): Contrast factor.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or alpha is invalid.
        """
        self._ensure_loaded()
        if not isinstance(alpha, (int, float)) or alpha <= 0:
            raise ValueError("Contrast alpha must be > 0.")
        self._current = cv2.convertScaleAbs(self._current, alpha=alpha, beta=0)

    def rotate(self, angle: int):
        """
        This function rotates the image by a supported angle.

        Parameters:
            angle (int): Must be one of 90, 180, or 270.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or the angle is not supported.
        """
        self._ensure_loaded()
        if angle not in self.SUPPORTED_ROTATIONS:
            raise ValueError("Rotation angle must be 90, 180, or 270.")
        if angle == 90:
            self._current = cv2.rotate(self._current, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            self._current = cv2.rotate(self._current, cv2.ROTATE_180)
        else:
            self._current = cv2.rotate(self._current, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def flip(self, mode: str):
        """
        This function flip the image horizontally or vertically.

        Parameters:
            mode (str): "horizontal" or "vertical".

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or mode is invalid.
        """
        self._ensure_loaded()
        if mode == "horizontal":
            self._current = cv2.flip(self._current, 1)
        elif mode == "vertical":
            self._current = cv2.flip(self._current, 0)
        else:
            raise ValueError("Flip mode must be 'horizontal' or 'vertical'.")

    def resize_from_original(self, percent: int):
        """
        This function resize using the original image for better quality.

        Parameters:
            percent (int): New size in percent.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded or percent is not a positive integer.
        """
        self._ensure_loaded()
        if not isinstance(percent, int) or percent <= 0:
            raise ValueError("Resize percentage must be a positive integer.")

        orig = self._original
        h, w = orig.shape[:2]
        base = Size(w, h)
        factor = percent / 100.0
        new_w, new_h = (base * factor)

        self._current = cv2.resize(orig, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
    def reset(self):
        """
        This function reset the working image back to the original.

        Returns:
            None

        Raises:
            ValueError: If no image is loaded.
        """
        self._ensure_loaded()
        self._current = self._original.copy()
