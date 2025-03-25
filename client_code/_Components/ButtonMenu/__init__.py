import anvil.designer
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
from ._anvil_designer import ButtonMenuTemplate


class ButtonMenu(ButtonMenuTemplate):
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

  def _setup_fui(self):
    if self._shown:
      self._cleanup()
      self._cleanup = fui.auto_update(
        self._btnNode, self._menuNode, placement="bottom-start"
      )

  def _on_mount(self, **event_args):
    self._shown = True
    document.addEventListener('keydown', self._handle_keyboard_events)
    self._menuNode.addEventListener('click', self._child_clicked)
    self._btnNode.addEventListener('click', self._handle_click)
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
    sp = get_unset_spacing(el, el, self.spacing)
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

  menu_background_color = color_property(
    'anvil-m3-buttonMenu-items-container', 'background', 'menu_background_color'
  )
  menu_border = border_property('anvil-m3-buttonMenu-items-container', 'menu_border')
  visible = HtmlTemplate.visible

  @anvil_prop
  @property
  def text(self, value) -> str:
    """The text displayed on the Button"""
    v = value
    self.menu_button.dom_nodes['anvil-m3-button-text'].classList.toggle(
      'anvil-m3-textlessComponentText', False
    )
    if anvil.designer.in_designer and not value:
      v = self._design_name
      self.menu_button.dom_nodes['anvil-m3-button-text'].classList.toggle(
        'anvil-m3-textlessComponentText', True
      )
    self.menu_button.text = v

  @anvil_prop
  @property
  def appearance(self, value) -> str:
    """A predefined style for the Button."""
    self.menu_button.appearance = value

  @anvil_prop
  @property
  def tooltip(self, value) -> str:
    """The text to display when the mouse is hovered over this component."""
    self.menu_button.tooltip = value

  @anvil_prop
  @property
  def enabled(self, value) -> bool:
    """If True, this component allows user interaction."""
    self.menu_button.enabled = value

  @anvil_prop
  @property
  def bold(self, value) -> bool:
    """If True, the Button’s text will be bold."""
    self.menu_button.bold = value

  @anvil_prop
  @property
  def italic(self, value) -> bool:
    """If True, the Button’s text will be italic."""
    self.menu_button.italic = value

  @anvil_prop
  @property
  def underline(self, value) -> bool:
    """If True, the Button’s text will be underlined."""
    self.menu_button.underline = value

  @anvil_prop
  @property
  def button_border(self, value) -> str:
    """The border of the Button. Can take any valid CSS border value."""
    self.menu_button.border = value

  @anvil_prop
  @property
  def button_background_color(self, value) -> str:
    """The colour of the background of the Button."""
    self.menu_button.background_color = value

  @anvil_prop
  @property
  def button_text_color(self, value) -> str:
    """The colour of the text on the Button."""
    self.menu_button.text_color = value

  @anvil_prop
  @property
  def button_font_size(self, value) -> int:
    """The font size of the text displayed on the Button."""
    self.menu_button.font_size = value

  @anvil_prop
  @property
  def icon(self, value) -> str:
    """The icon to display on the Button."""
    self.menu_button.icon = value

  @anvil_prop
  @property
  def icon_color(self, value) -> str:
    """The colour of the icon displayed on the Button."""
    self.menu_button.icon_color = value

  @anvil_prop
  @property
  def icon_size(self, value) -> int:
    """The size (pixels) of the icon displayed on this component."""
    self.menu_button.icon_size = value

  @anvil_prop
  @property
  def icon_position(self, value) -> str:
    """The alignment of the icon on this component."""
    self.menu_button.icon_position = value

  @anvil_prop
  @property
  def spacing(self, value) -> list:
    """The margin and padding (pixels) of the component."""
    self.menu_button.spacing = value

  @anvil_prop
  @property
  def align(self, value) -> str:
    """The position of this component in the available space."""
    self.menu_button.dom_nodes['anvil-m3-button'].classList.toggle(
      'anvil-m3-full-width', False
    )
    self.menu_button.dom_nodes['anvil-m3-button-component'].style.removeProperty(
      'justify-content'
    )
    if value == 'full':
      self.menu_button.dom_nodes['anvil-m3-button'].classList.toggle(
        'anvil-m3-full-width', True
      )
    else:
      self.menu_button.dom_nodes[
        'anvil-m3-button-component'
      ].style.justifyContent = value
    self._setup_fui()

  @anvil_prop
  @property
  def button_font_family(self, value) -> str:
    """The font family to use for the Button"""
    self.menu_button.font_family = value

  @anvil_prop
  @property
  def role(self, value) -> str:
    """A style for this component defined in CSS and added to Roles"""
    self.menu_button.role = value

  @anvil_prop
  @property
  def menu_items(self, value=[]) -> list:
    """A list of components to be added to the menu."""
    for i in value:
      self.add_component(i, slot='anvil-m3-buttonMenu-slot')

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
    if self._btnNode.contains(event.target) or self._menuNode.contains(event.target):
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
            self, "text", self.menu_button.dom_nodes["anvil-m3-button-text"]
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
        self.menu_button.text = self._design_name

  #!componentProp(m3.ButtonMenu)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
  #!componentProp(m3.ButtonMenu)!1: {name:"appearance",type:"enum",options:["filled", "elevated", "tonal", "outlined", "text"],description:"A predefined style for the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.ButtonMenu)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.ButtonMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.ButtonMenu)!1: {name:"button_text_color",type:"color",description:"The colour of the text on the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"button_font_family",type:"string",description:"The font family to use for the Button"}
  #!componentProp(m3.ButtonMenu)!1: {name:"icon",type:"enum",description:"The icon to display on the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"text",type:"string",description:"The text displayed on the Button"}
  #!componentProp(m3.ButtonMenu)!1: {name:"button_font_size",type:"number",description:"The font size of the text displayed on the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"underline",type:"boolean",description:"If True, the Button’s text will be underlined."}
  #!componentProp(m3.ButtonMenu)!1: {name:"italic",type:"boolean",description:"If True, the Button’s text will be italic."}
  #!componentProp(m3.ButtonMenu)!1: {name:"bold",type:"boolean",description:"If True, the Button’s text will be bold."}
  #!componentProp(m3.ButtonMenu)!1: {name:"icon_color",type:"color",description:"The colour of the icon displayed on the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"menu_background_color",type:"color",description:"The colour of the menu."}
  #!componentProp(m3.ButtonMenu)!1: {name:"menu_border",type:"color",description:"The border of the menu. Can take any valid CSS border value."}
  #!componentProp(m3.ButtonMenu)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(m3.ButtonMenu)!1: {name:"button_background_color",type:"color",description:"The colour of the background of the Button."}
  #!componentProp(m3.ButtonMenu)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.ButtonMenu)!1: {name:"button_border",type:"string",description:"The border of the Button. Can take any valid CSS border value."}
  #!componentProp(m3.ButtonMenu)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.ButtonMenu)!1: {name:"icon_position",type:"enum",options:["left", "right"],description:"The alignment of the icon on this component."}
  #!componentProp(m3.ButtonMenu)!1: {name:"menu_items",type:"object",description:"A list of components to be added to the menu."}
  #!componentProp(m3.ButtonMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(m3.ButtonMenu)!1: {name: "click", description: "When the Button is clicked.", parameters:[]}


#!defClass(m3, ButtonMenu, anvil.Component)!:
