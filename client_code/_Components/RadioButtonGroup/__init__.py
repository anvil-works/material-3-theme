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

class RadioButtonGroup(RadioButtonGroupTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._group_name = gen_id()
    self.init_components(**properties)

  # properties
  def _set_orientation(self, value):
    # change flex direction
    pass
  orientation = property_with_callback("orientation", _set_orientation)
  def _set_items(self, value):
    # rerending all radiobutton items, if tuple with extra special stuff might have to rerender special stuff
    pass
  items = property_with_callback("items", _set_items)
  def _set_selected_item(self, item):
    # find the radio button assocatd with this item and set checked to true
    pass
  selected_item = property_with_callback("selected_item", _set_selected_item)

  
  # def _set_selected_value(self, value):
  #     if (value is None and self.allow_none) or (value in self.items):
  #       if value is None and self.allow_none:
  #         self._hoverIndex = None
  #       if isinstance(value, tuple):
  #         self.selection_field.dom_nodes['anvil-m3-textfield'].value = value[0]
  #       else:
  #         self.selection_field.dom_nodes['anvil-m3-textfield'].value = value
  #     else:
  #       self.selection_field.dom_nodes['anvil-m3-textfield'].value = "<Invalid value>"
  #   selected_value = property_with_callback("selected_value", _set_selected_value)

  def form_show(self, **event_args):
    self.renderItems()

  def renderItems(self):
    for item in self.items:
      rb = RadioButton()
      rb.text = item[0] if isinstance(item, tuple) else item
      if isinstance(item, tuple): 
        rb.text = item[0]
        rb.value = item[1]
        if len(item) > 2:
          if isinstance(item[2], object):
            for prop_name, val in item[2].items():
              if hasattr(rb, prop_name):
                setattr(rb, prop_name, val)
                
        # todo: check if there's an item 2 and all the props
      else:
        rb.text = item
        rb.value = item
      
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