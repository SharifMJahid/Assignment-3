class BaseComponent:
    """
    This class is for all GUI components in the application.
    """

    def __init__(self, controller):
        """
        This function initializes the base GUI component.

        Parameters:
            controller: The main controller object.
        """
        self.controller = controller

    def __repr__(self) -> str:
        """
        This function returns a readable string representation of the component.
        """
        return f"{self.__class__.__name__}(controller={self.controller.__class__.__name__})"


class ClickableMixin:
    """
    This class adds click handling functionality to a component.
    """

    def set_on_click(self, callback):
        """
        This function assigns a callback function to be executed when the component is clicked.

        Parameters:
            callback: A function or method that will be executed when a click event occurs.
        """
        self.on_click = callback
