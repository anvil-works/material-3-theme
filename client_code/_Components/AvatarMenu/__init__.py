from anvil import *

from ..._utils import fui, noop
from ..._utils.properties import (
  ComponentTag,
  anvil_prop,
  border_property,
  color_property,
  get_unset_spacing,
  get_unset_value,
)
from ..MenuItem import MenuItem
from ._anvil_designer import AvatarMenuTemplate


class AvatarMenu(AvatarMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
