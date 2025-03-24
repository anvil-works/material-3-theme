import anvil
import anvil.designer

from ..._utils.properties import (
  border_property,
  get_unset_spacing,
  role_property,
  spacing_property,
  tooltip_property,
)
from ._anvil_designer import CenterPanelTemplate


class CenterPanel(CenterPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._props = properties
    self._tooltip_node = None
    self.init_components(**properties)

    def _anvil_get_unset_property_values_(self):
      el = self.dom_nodes["anvil-m3-center-panel"]
      sp = get_unset_spacing(el, el, self.spacing)
      return {"spacing": sp}

  visible = anvil.HtmlTemplate.visible
  border = border_property('anvil-m3-center-panel')
  role = role_property('anvil-m3-center-panel')
  spacing = spacing_property('anvil-m3-center-panel')
  tooltip = tooltip_property('anvil-m3-text-container')
