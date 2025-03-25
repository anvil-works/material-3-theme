from ._anvil_designer import MenuContainerTemplate
from anvil import *


class MenuContainer(MenuContainerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
  def _toggle_menu_visibility(self, **event_args):
      self._toggle_visibility()

  def _toggle_visibility(self, value=None):
    classes = self._menuNode.classList
    if value is not None:
      classes.toggle('anvil-m3-buttonMenu-items-hidden', not value)
    else:
      classes.toggle('anvil-m3-buttonMenu-items-hidden')

    self._open = not classes.contains('anvil-m3-buttonMenu-items-hidden')
    if self._open:
      self._setup_fui()
      self._get_hover_index_information()
    else:
      self._cleanup()
      self._hoverIndex = None
      self._clear_hover_styles()

  def _child_clicked(self, event):
    # do the click action. The child should handle this
    self._toggle_visibility(False)
    if self.enabled:
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
