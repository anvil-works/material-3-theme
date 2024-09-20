from ._anvil_designer import RadioButtonGroupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Functions import (
  property_with_callback,
  checked_property,
  role_property,
  tooltip_property,
  name_property,
  innerText_property,
  enabled_property,
  style_property,
  underline_property,
  italic_property,
  border_property,
  bold_property,
  font_size_property,
  color_property,
  theme_color_to_css,
  value_property,
  font_family_property,
  margin_property,
)
from ...utils import gen_id
from RadioButton import RadioButton
from anvil.designer import in_designer

class RadioButtonGroup(RadioButtonGroupTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._group_name = gen_id()
    self._items = []
    self.init_components(**properties)

  # properties
  def _set_orientation(self, value):
    self.dom_nodes['anvil-m3-radiobuttongroup-container'].style = f"flex-direction: {'row' if value == 'horizontal' else 'column'};"
  orientation = property_with_callback("orientation", _set_orientation)
  def _set_items(self, value):
    for item in value:
      self._items.append(item) if isinstance(item, tuple) else self._items.append((item, item))
    self.renderItems()
  items = property_with_callback("items", _set_items)
  def _set_selected_item(self, item):
    print(item)
    pass
  selected_item = property_with_callback("selected_item", _set_selected_item)

  def form_show(self, **event_args):
    self.renderItems()

  def renderItems(self):
    self.clear(slot="anvil-m3-radiobuttongroup-slot")
    if in_designer:
      if len(self._items) == 0:
        for _ in range(2):
          placeholder = RadioButton()
          placeholder.text = "radio_button"
          placeholder.visible = False
          placeholder.enabled = False
          self.add_component(placeholder, slot="anvil-m3-radiobuttongroup-slot")          
    for item in self._items:
      rb = RadioButton()
      rb.text = item[0]
      rb.value = item[1]
      if len(item) > 2:
        print(item[2])
        if isinstance(item[2], object):
          for prop_name, val in item[2].items():
            if hasattr(rb, prop_name):
              setattr(rb, prop_name, val)
      rb.group_name = self._group_name
      def _handle_select_rb(value = item, **e):
        self.selected_item = value
        self.raise_event("change")
      rb.add_event_handler('change', _handle_select_rb)
      self.add_component(rb, slot="anvil-m3-radiobuttongroup-slot")




# <div anvil-name="anvil-m3-radiobuttongroup-component" style="display:flex">
#   <div anvil-name="anvil-m3-radiobuttongroup-container" class="anvil-m3-radiobuttongroup-container" anvil-slot="anvil-m3-radiobuttongroup-slot" anvil-slot-internal>
#   </div>
# </div>