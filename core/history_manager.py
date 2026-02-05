class HistoryManager:
    """
    This class keeps an undo or redo history for image modification.
    """
    def __init__(self):
        """
        This function initialize empty undo and redo lists.
        """
        self._undo = []
        self._redo = []

    def __len__(self) -> int:
        """
        This function gives the number of available undo steps.

        Returns:
            int: How many undo states are currently available.
        """
        return len(self._undo)

    def __repr__(self) -> str:
        """
        This function return a readable summary of the current history counts.

        Returns:
            str: A string showing how many undo and redo states are stored.
        """
        return f"HistoryManager(undo={len(self._undo)}, redo={len(self._redo)})"

    def save(self, image, scale: int):
        """
        this function saves the current state into history.

        Parameters:
            image: Current image to store.
            scale (int): Current scale or zoom level for the image.
        """
        self._undo.append((image.copy(), scale))
        self._redo.clear()

    def undo(self, current_image, current_scale: int):
        """
        this function revert to the most recent saved change.

        Parameters:
            current_image: Current image .
            current_scale (int): The current scale/zoom level.

        Returns:
            tuple | None: The previous state as (image_copy, scale),
            or None if there is nothing to undo.
        """
        if not self._undo:
            return None
        self._redo.append((current_image.copy(), current_scale))
        return self._undo.pop()

    def redo(self, current_image, current_scale: int):
        """
        This function redo the most recently undone change.

        Parameters:
            current_image: current image.
            current_scale (int): The current scale/zoom level.

        Returns:
            tuple | None: The next state as (image_copy, scale),
            or None if there is nothing to redo.
        """
        if not self._redo:
            return None
        self._undo.append((current_image.copy(), current_scale))
        return self._redo.pop()

    def clear(self):
        """
        This function clear all undo and redo history.
        """
        self._undo.clear()
        self._redo.clear()
