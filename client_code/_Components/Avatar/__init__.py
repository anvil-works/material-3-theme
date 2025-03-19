from ._anvil_designer import AvatarTemplate
from anvil import *


class Avatar(AvatarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self.init_components(**properties)

    self.dom_nodes['anvil-m3-avatar'].addEventListener(
      "click", self._handle_click
    )

    # Any code you write here will run before the form opens.
