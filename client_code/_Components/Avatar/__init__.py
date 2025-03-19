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
    self.initials_div = self.dom_nodes['anvil-m3-avatar-initials']
    self.fallback_icon_div = self.dom_nodes['anvil-m3-avatar-icon']
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
    self.fallback_icon_div.style.display = "none"
    if value:
      self.fallback_icon_div.className = ""
      self.fallback_icon_div.classList.add("material-symbols-outlined")
      self.fallback_icon_div.innerText = value[3:]
      if not self.image and not self.name:
        self.fallback_icon_div.style.display = "block"

  @anvil_prop
  @property
  def image(self, value):
    image = self.dom_nodes['anvil-m3-avatar-image']
    if value: 
      image.style.display = "block"
      image.src = value
      self.initials_div.style.display = "none"
      self.fallback_icon_div.display = "none"
    else:
      image.style.display = "none"


  @anvil_prop
  @property
  def name(self, value):
    if value and not self.image:
      self.initials_div.style.display = "block"
    self.initials_div.style.display = "none"
    names = value.split()
    initials = ""
    for n in names:
      initials += n[0]
    self.initials_div.innerText = initials
    if not self.image:
      
    
