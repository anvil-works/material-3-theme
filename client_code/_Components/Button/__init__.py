import anvil.designer
import anvil.js
from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import (
  ComponentTag,
  anvil_prop,
  color_property,
  custom_bold_property,
  font_family_property,
  font_size_property,
  get_unset_spacing,
  get_unset_value,
  italic_property,
  property_with_callback,
  role_property,
  spacing_property,
  style_property,
  tooltip_property,
  underline_property,
)
from ._anvil_designer import ButtonTemplate


class Button(ButtonTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties

    self._tooltip_node = None
    self.init_components(**properties)

    self.dom_nodes['anvil-m3-button'].addEventListener("click", self._handle_click)

  def _handle_click(self, event):
    event.preventDefault()
    event.stopPropagation()
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

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(
            self, "text", self.dom_nodes['anvil-m3-button-text']
          )
        },
      }
    ]

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes["anvil-m3-button"]
    sp = get_unset_spacing(el, el, self.spacing)
    tfs = get_unset_value(
      self.dom_nodes['anvil-m3-button-text'], "fontSize", self.font_size
    )
    ifs = get_unset_value(
      self.dom_nodes['anvil-m3-button-icon'], "fontSize", self.icon_size
    )
    return {"font_size": tfs, "icon_size": ifs, "spacing": sp}

  def _update_button_look(self, value=None):
    buttonNode = self.dom_nodes['anvil-m3-button']
    textNode = self.dom_nodes['anvil-m3-button-text']

    buttonNode.classList.remove('anvil-m3-icon-padding')
    textNode.classList.remove('anvil-m3-textlessComponentText')
    buttonNode.classList.remove('anvil-m3-no-text')

    self._set_icon()
    self._set_text()

  def form_show(self, **event_args):
    self._update_button_look()

  def _set_icon(self):
    if self.icon and self.icon.startswith('mi:'):
      self.dom_nodes['anvil-m3-button-icon'].innerText = self.icon[3:]
      self.dom_nodes['anvil-m3-button-icon'].style.display = "flex"
      if self.text:
        self.dom_nodes['anvil-m3-button'].classList.add('anvil-m3-icon-padding')
      else:
        self.dom_nodes['anvil-m3-button'].classList.add('anvil-m3-no-text')
    else:
      self.dom_nodes['anvil-m3-button-icon'].innerText = ""
      self.dom_nodes['anvil-m3-button-icon'].style.display = "none"

  def _set_text(self):
    if self.text:
      self.dom_nodes['anvil-m3-button-text'].innerText = str(self.text if self.text is not None else "")
    else:
      if not self.icon:
        if anvil.designer.in_designer:
          self.dom_nodes[
            'anvil-m3-button-text'
          ].innerText = anvil.designer.get_design_name(self)
          self.dom_nodes['anvil-m3-button-text'].classList.add(
            'anvil-m3-textlessComponentText'
          )
        else:
          self.dom_nodes['anvil-m3-button-text'].innerText = "Button"
      else:
        self.dom_nodes['anvil-m3-button-text'].innerText = ""

  role = role_property('anvil-m3-button')
  text = property_with_callback("text", _update_button_look)
  icon = property_with_callback("icon", _update_button_look)
  text_color = color_property('anvil-m3-button-text', 'color', 'text_color')
  font_family = font_family_property('anvil-m3-button-text')
  font_size = font_size_property('anvil-m3-button-text')
  underline = underline_property('anvil-m3-button-text')
  italic = italic_property('anvil-m3-button-text')
  bold = custom_bold_property('anvil-m3-button-text')
  icon_color = color_property('anvil-m3-button-icon', 'color', 'icon_color')
  icon_size = font_size_property('anvil-m3-button-icon', 'icon_size')
  background_color = color_property(
    'anvil-m3-button', 'backgroundColor', 'background_color'
  )
  spacing = spacing_property('anvil-m3-button')
  border = style_property('anvil-m3-button', 'border', 'border')
  tooltip = tooltip_property('anvil-m3-button')
  visible = HtmlTemplate.visible

  @anvil_prop
  @property
  def align(self, value) -> str:
    """The position of this component in the available space."""
    self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-full-width', False)
    if value == 'full':
      self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-full-width', True)
    else:
      self.dom_nodes['anvil-m3-button-component'].style.justifyContent = value

  @anvil_prop
  @property
  def icon_align(self, value) -> str:
    """The alignment of the icon on this component."""
    self.dom_nodes['anvil-m3-button'].classList.toggle(
      'anvil-m3-right-icon', value == 'right'
    )

  @anvil_prop
  @property
  def enabled(self, value) -> bool:
    """If True, this component allows user interaction."""
    if value:
      self.dom_nodes['anvil-m3-button'].removeAttribute("disabled")
    else:
      self.dom_nodes['anvil-m3-button'].setAttribute("disabled", " ")

  @anvil_prop
  @property
  def appearance(self, value) -> str:
    """A predefined style for this component."""
    button = self.dom_nodes['anvil-m3-button']
    button.classList.remove('anvil-m3-elevated')
    button.classList.remove('anvil-m3-filled')
    button.classList.remove('anvil-m3-tonal')
    button.classList.remove('anvil-m3-outlined')
    if value and value != 'text':
      button.classList.add(f"anvil-m3-{value}")

  #!componentProp(m3.Button)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
  #!componentProp(m3.Button)!1: {name:"appearance",type:"enum",options:["filled", "elevated", "tonal", "outlined", "text"],description:"A predefined style for this component."}
  #!componentProp(m3.Button)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.Button)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.Button)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.Button)!1: {name:"text_color",type:"color",description:"The colour of the text on the component."}
  #!componentProp(m3.Button)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(m3.Button)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
  #!componentProp(m3.Button)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(m3.Button)!1: {name:"font_size",type:"number",description:"The font size of the text displayed on this component."}
  #!componentProp(m3.Button)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(m3.Button)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(m3.Button)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(m3.Button)!1: {name:"icon_color",type:"color",description:"The colour of the icon displayed on this component."}
  #!componentProp(m3.Button)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(m3.Button)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(m3.Button)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.Button)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(m3.Button)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.Button)!1: {name:"icon_align",type:"enum",options:["left", "right"],description:"The alignment of the icon on this component."}
  #!componentProp(m3.Button)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(m3.Button)!1: {name: "click", description: "When the component is clicked.", parameters:[]}


#!defClass(m3, Button, anvil.Component)!:
