from ._anvil_designer import AvatarTemplate
from anvil import *

from ..._utils.properties import (
  anvil_prop
)

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

    
  def _handle_click(self, event):
    self.raise_event(
      "click",
      event=event,
      keys={
        "shift": event.shiftKey,
        "alt": event.altKey,
        "ctrl": event.ctrlKey,
        "meta": event.metaKey,
      },
    )
    # Any code you write here will run before the form opens.

  @anvil_prop
  @property
  def fallback_icon(self, value) -> str:
    """The icon to display on this component."""
    fallback_icon = self.dom_nodes['anvil-m3-avatar-icon']
    fallback_icon.style.display = "none"
    if value:
      fallback_icon.className = ""
      fallback_icon.classList.add("material-symbols-outlined")
      fallback_icon.innerText = value[3:]
      if not self.image and self.name:
        fallback_icon.style.display = "block"

  @anvil_prop
  @property
  def image(self, value):
    image = self.dom_nodes['anvil-m3-avatar-image']
    print(value)
    image.src = value

  @anvil_prop
  @property
  def name(self, value):
    initials_div = self.dom_nodes['anvil-m3-avatar-initials']
    names = name.split()
    initials = ""
    for n in names:
      initials += 
    
