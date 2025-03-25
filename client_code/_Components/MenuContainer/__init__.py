from ..MenuItem import MenuItem
from ._anvil_designer import MenuContainerTemplate
from anvil import *
from ..._utils.properties import (
  color_property,
  border_property

)


class MenuContainer(MenuContainerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._props = properties
    self.init_components(**properties)

  background_color = color_property(
    'anvil-m3-menuContainer-items-container', 'background', 'background_color'
  )
  border = border_property('anvil-m3-menuContainer-items-container', 'border')

    
  def _toggle_menu_visibility(self, **event_args):
      self._toggle_visibility()

  def _toggle_visibility(self, value=None):
    classes = self.dom_nodes['anvil-m3-menuContainer-items-container'].classList
    if value is not None:
      classes.toggle('anvil-m3-menuContainer-items-hidden', not value)
    else:
      classes.toggle('anvil-m3-menuContainer-items-hidden')

    self._open = not classes.contains('anvil-m3-menuContainer-items-hidden')
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

  def _get_hover_index_information(self):
    self._children = self.get_components()[:-1]
    for i in range(0, len(self._children)):
      if isinstance(self._children[i], MenuItem):
        self._itemIndices.add(i)

  def _handle_keyboard_events(self, event):
    if not self._open:
      return
    action_keys = set(["ArrowUp", "ArrowDown", "Tab", "Escape", " ", "Enter"])
    if event.key not in action_keys:
      return
    if event.key in ["ArrowUp", "ArrowDown"]:
      self._iterate_hover(event.key == "ArrowDown")
      event.preventDefault()
      return
    hover = (
      self._hoverIndex
    )  # holding value for situations like alerts, where it awaits
    self._toggle_visibility(False)

    def attemptSelect():
      event.preventDefault()
      if hover is not None:
        self._children[hover].raise_event(
          "click",
          event=event,
          keys={
            "shift": event.shiftKey,
            "alt": event.altKey,
            "ctrl": event.ctrlKey,
            "meta": event.metaKey,
          },
        )

    if event.key == " ":  # " " indicates the space key
      attemptSelect()
    if event.key == "Enter":
      attemptSelect()

  def _iterate_hover(self, inc=True):
    if inc:
      if self._hoverIndex is None or self._hoverIndex is (len(self._children) - 1):
        self._hoverIndex = -1
      while True:
        self._hoverIndex += 1
        if self._hoverIndex in self._itemIndices:
          break
    else:
      if self._hoverIndex is None or self._hoverIndex == 0:
        self._hoverIndex = len(self._children)
      while True:
        self._hoverIndex -= 1
        if self._hoverIndex in self._itemIndices:
          break
    self._children[self._hoverIndex].dom_nodes[
      'anvil-m3-menuItem-container'
    ].scrollIntoView({'block': 'nearest'})
    self._update_hover_styles()

  def _clear_hover_styles(self):
    if self._children is not None:
      for child in self._children:
        if isinstance(child, MenuItem):
          child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle(
            'anvil-m3-menuItem-container-keyboardHover', False
          )

  def _update_hover_styles(self):
    self._clear_hover_styles()
    self._children[self._hoverIndex].dom_nodes[
      'anvil-m3-menuItem-container'
    ].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "designer_events",
        "callbacks": {
          "onSelectDescendent": self._on_select_descendent,
          "onSelectOther": self._on_select_other,
        },
      },
    ]

  def _on_select_descendent(self):
    self._toggle_visibility(True)

  def _on_select_other(self):
    self._toggle_visibility(False)
