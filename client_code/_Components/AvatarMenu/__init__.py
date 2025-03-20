from anvil import *
from anvil import HtmlTemplate
from anvil.js import get_dom_node
from anvil.js.window import document

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
    self.tag = ComponentTag()
    self._props = properties
    self._design_name = ""
    self._cleanup = noop
    self._menuNode = self.dom_nodes['anvil-m3-buttonMenu-items-container']
    self._btnNode = get_dom_node(self.menu_button).querySelector("button")
    self._open = False
    self._hoverIndex = None
    self._itemIndices = set()
    self._children = None
    self._shown = False

    self.init_components(**properties)

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
