from ._anvil_designer import Form1Template
import anvil
from ..components import Button


class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.icon_button_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]
        self.button_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]

    @anvil.handle("interactive_card_1", "click")
    def interactive_card_1_click(self, **event_args):
        """This method is called when the component is clicked"""
        anvil.alert("Card Click!")
