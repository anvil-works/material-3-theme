from ._anvil_designer import Form1Template
from ..components import Button


class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.icon_button_menu_1.menu_items = [Button(text=n) for n in ["1", "2", "3"]]
