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
  def icon(self, value) -> str:
    """The icon to display on this component."""
    link_icon = self.dom_nodes['anvil-m3-navigation-link-icon']
    if value:
      link_icon.className = ""
      link_icon.classList.add("material-symbols-outlined")
      link_icon.innerText = value[3:]
