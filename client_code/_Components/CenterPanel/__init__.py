import anvil
import anvil.designer

from ..._utils.properties import (
  get_unset_spacing,
  spacing_property,
)
from ._anvil_designer import CenterPanelTemplate


class CenterPanel(CenterPanelTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self._props = properties
        self.init_components(**properties)
    
        def _anvil_get_unset_property_values_(self):
            el = self.dom_nodes["anvil-m3-center-panel"]
            sp = get_unset_spacing(el, el, self.spacing)
            return {"spacing": sp}
    
        spacing = spacing_property('anvil-m3-center-panel')
