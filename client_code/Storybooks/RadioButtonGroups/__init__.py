from ._anvil_designer import RadioButtonGroupsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RadioButtonGroups(RadioButtonGroupsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.radio_button_group_2.items = [("First Option", 0), ("Second Option", 1), ("Third Option", 2), ("Fourth Option", 3)]
    self.radio_button_3.value = ("tuple option", 100)

    # Any code you write here will run before the form opens.

  def radio_button_group_1_change(self, **event_args):
    self.text_4.text = self.radio_button_group_1.selected_item

  def radio_button_group_2_change(self, **event_args):
    self.text_5.text = self.radio_button_group_2.selected_item[1]

  def update_text(self, **event_args):
    self.text_3.text = self.radio_button_1.get_group_value()
    
