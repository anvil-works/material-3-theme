from ._anvil_designer import FocusMethodTestingTemplate
import anvil
from ..components import Button


class FocusMethodTesting(FocusMethodTestingTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.icon_button_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]
        self.button_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]
        self.avatar_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]

    @anvil.handle("interactive_card_1", "click")
    def interactive_card_1_click(self, **event_args):
        """This method is called when the component is clicked"""
        anvil.alert("Card Click!")

    @anvil.handle("focus_button", "click")
    def focus_button_click(self, **event_args):
        """This method is called to test focus methods."""
        getattr(self, self.focused_element.text.strip()).focus()
