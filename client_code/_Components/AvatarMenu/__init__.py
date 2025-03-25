from anvil import *
from anvil import HtmlTemplate
from anvil.js.window import document

from ..._utils import fui, noop
from ..._utils.properties import (
  ComponentTag,
  anvil_prop,
  border_property,
  color_property,
  enabled_property,
  get_unset_value,
  get_unset_margin,
)
from ..MenuItem import MenuItem
from ._anvil_designer import AvatarMenuTemplate


class AvatarMenu(AvatarMenuTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._design_name = ""
    self._cleanup = noop
    self._menuNode = self.dom_nodes['anvil-m3-avatarMenu-items-container']
    self._buttonNode = self.dom_nodes['anvil-m3-avatarMenu-button']
    self._open = False
    self._hoverIndex = None
    self._itemIndices = set()
    self._children = None
    self._shown = False

    self.init_components(**properties)

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _setup_fui(self):
    if self._shown:
      self._cleanup()
      self._cleanup = fui.auto_update(
        self._buttonNode, self._menuNode, placement="bottom-start"
      )

  def _on_mount(self, **event_args):
    self._shown = True
    document.addEventListener('keydown', self._handle_keyboard_events)
    self._menuNode.addEventListener('click', self._child_clicked)
    self._buttonNode.addEventListener('click', self._handle_click)
    document.addEventListener('click', self._body_click)
    # We still have a reference to the dom node but we've moved it to the body
    # This gets around the fact that Anvil containers set their overflow to hidden
    document.body.append(self._menuNode)
    self._setup_fui()

  def _on_cleanup(self, **event_args):
    self._shown = False
    document.removeEventListener('keydown', self._handle_keyboard_events)
    self._menuNode.removeEventListener('click', self._child_clicked)
    document.removeEventListener('click', self._body_click)
    self._cleanup()
    # Remove the menu node we put on the body
    self._menuNode.remove()

  def _anvil_get_unset_property_values_(self):
    el = self.menu_button.dom_nodes["anvil-m3-button"]
    m = get_unset_margin(el, el, self.spacing)
    tfs = get_unset_value(
      self.menu_button.dom_nodes['anvil-m3-button-text'],
      "fontSize",
      self.button_font_size,
    )
    ifs = tfs = get_unset_value(
      self.menu_button.dom_nodes['anvil-m3-button-icon'],
      "fontSize",
      self.button_font_size,
    )
    return {"button_font_size": tfs, "icon_size": ifs, "spacing": sp}

  def _handle_click(self, event):
    if self.enabled:
      self._toggle_menu_visibility()

  menu_background_color = color_property(
    'anvil-m3-avatarMenu-items-container', 'background', 'menu_background_color'
  )
  menu_border = border_property('anvil-m3-avatarMenu-items-container', 'menu_border')
  visible = HtmlTemplate.visible
  enabled = enabled_property('anvil-m3-avatarMenu-button')

  @anvil_prop
  @property
  def user_name(self, value) -> str:
    """The name of the avatar component"""
    self.avatar.user_name = value

  @anvil_prop
  @property
  def appearance(self, value) -> str:
    """A predefined style for the avatar."""
    self.avatar.appearance = value

  @anvil_prop
  @property
  def tooltip(self, value) -> str:
    """The text to display when the mouse is hovered over this component."""
    self.avatar.tooltip = value

  @anvil_prop
  @property
  def avatar_border(self, value) -> str:
    """The border of the avatar. Can take any valid CSS border value."""
    self.avatar.border = value

  @anvil_prop
  @property
  def avatar_background_color(self, value) -> str:
    """The colour of the background of the Button."""
    self.avatar.background_color = value

  @anvil_prop
  @property
  def avatar_text_color(self, value) -> str:
    """The colour of the text on the Button."""
    self.avatar.text_color = value

  @anvil_prop
  @property
  def avatar_font_size(self, value) -> int:
    """The font size of the text displayed on the Button."""
    self.avatar.font_size = value

  @anvil_prop
  @property
  def fallback_icon(self, value) -> str:
    """The icon to display on the Button."""
    self.avatar.fallback_icon = value

  @anvil_prop
  @property
  def fallback_icon_color(self, value) -> str:
    """The colour of the icon displayed on the Button."""
    self.avatar.fallback_icon_color = value

  @anvil_prop
  @property
  def fallback_icon_size(self, value) -> int:
    """The size (pixels) of the icon displayed on this component."""
    self.avatar.fallback_icon_size = value

  @anvil_prop
  @property
  def margin(self, value) -> list:
    """The margin (pixels) of the component."""
    self.avatar.margin = value

  @anvil_prop
  @property
  def align(self, value) -> str:
    self.avatar.align = value
    self._setup_fui()

  @anvil_prop
  @property
  def avatar_font_family(self, value) -> str:
    """The font family to use for the Button"""
    self.avatar.font_family = value

  @anvil_prop
  @property
  def role(self, value) -> str:
    """A style for this component defined in CSS and added to Roles"""
    self.avatar.role = value

  @anvil_prop
  @property
  def menu_items(self, value=[]) -> list:
    """A list of components to be added to the menu."""
    for i in value:
      self.add_component(i, slot='anvil-m3-avatarMenu-slot')

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

  def _body_click(self, event):
    if self._buttonNode.contains(event.target) or self._menuNode.contains(event.target):
      return
    self._toggle_visibility(False)

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
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(
            self, "text", self.avatar.dom_nodes["anvil-m3-button-text"]
          )
        },
      },
    ]

  def _on_select_descendent(self):
    self._toggle_visibility(True)

  def _on_select_other(self):
    self._toggle_visibility(False)

  def form_show(self, **event_args):
    if anvil.designer.in_designer:
      self._design_name = anvil.designer.get_design_name(self)
      if not self.text:
        self.avatar.text = self._design_name


