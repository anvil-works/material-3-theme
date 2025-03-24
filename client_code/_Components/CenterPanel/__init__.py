from ._anvil_designer import CenterPanelTemplate
from anvil import *

from ..._utils.properties import (
  spacing_property,
)


class CenterPanel(CenterPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
