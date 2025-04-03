import anvil
import anvil.designer

from ..._utils.properties import (
  anvil_prop,
  bold_property,
  border_property,
  color_property,
  font_family_property,
  font_size_property,
  get_unset_spacing,
  get_unset_value,
  inline_editing,
  italic_property,
  role_property,
  spacing_property,
  tooltip_property,
  underline_property,
)
from ._anvil_designer import TextTemplate


class Text(TextTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.tag = anvil.ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self._set_designer_text_placeholder, self._start_inline_editing = inline_editing(
      self, self.dom_nodes['anvil-m3-text'], self._set_text
    )
    self.init_components(**properties)

  def _set_text(self, value):
    self.dom_nodes['anvil-m3-text'].innerText = str(value if value is not None else "")

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {"execute": self._start_inline_editing},
      }
    ]

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes["anvil-m3-text-container"]
    sp = get_unset_spacing(el, el, self.spacing)
    tfs = get_unset_value(self.dom_nodes['anvil-m3-text'], "fontSize", self.font_size)
    ifs = get_unset_value(
      self.dom_nodes['anvil-m3-text-icon'], "fontSize", self.icon_size
    )
    return {"font_size": tfs, "icon_size": ifs, "spacing": sp}

  #!componentEvent(m3.Text)!1: {name: "show", description: "When the Text is shown on the screen."}
  #!componentEvent(m3.Text)!1: {name: "hide", description: "When the Text is removed from the screen."}

  #!componentProp(m3.Text)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.Text)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(m3.Text)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(m3.Text)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(m3.Text)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(m3.Text)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(m3.Text)!1: {name:"text_color",type:"color",description:"The color of the text on the component."}
  #!componentProp(m3.Text)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(m3.Text)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
  #!componentProp(m3.Text)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(m3.Text)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(m3.Text)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.Text)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.Text)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.Text)!1: {name:"align",type:"enum",options:['left', 'right', 'center', 'justify'], description:"The position of this component in the available space."}
  #!componentProp(m3.Text)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(m3.Text)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
  #!componentProp(m3.Text)!1: {name:"line_height",type:"string",description:"The line height of this component."}
  #!componentProp(m3.Text)!1: {name:"material_icon",type:"enum",description:"The icon to display on this component."}
  #!componentProp(m3.Text)!1: {name:"style",type:"enum",options:['display', 'headline', 'title'],description:"Role of the text component: display, headline or title."}
  #!componentProp(m3.Text)!1: {name:"scale",type:"enum",options:['small', 'medium', 'large'],description:"The size of the text component."}
  #!componentProp(m3.Text)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  visible = anvil.HtmlTemplate.visible
  underline = underline_property('anvil-m3-text')
  italic = italic_property('anvil-m3-text')
  bold = bold_property('anvil-m3-text')
  border = border_property('anvil-m3-text-container')
  font_family = font_family_property('anvil-m3-text', 'font_family')
  text_color = color_property('anvil-m3-text-container', 'color', 'text_color')
  icon_color = color_property('anvil-m3-text-icon', 'color', 'icon_color')
  background_color = color_property(
    'anvil-m3-text-container', 'backgroundColor', 'background_color'
  )
  icon_size = font_size_property('anvil-m3-text-icon', 'icon_size')
  spacing = spacing_property('anvil-m3-text-container')
  tooltip = tooltip_property('anvil-m3-text-container')
  role = role_property('anvil-m3-text-container')

  @anvil_prop
  @property
  def text(self, value) -> str:
    """The text displayed on this component"""
    self._set_text(value)
    self._set_designer_text_placeholder()

  @anvil_prop
  @property
  def align(self, value) -> str:
    """The position of this component in the available space."""
    if value == 'justify':
      self.dom_nodes['anvil-m3-text-container'].style.justifyContent = 'left'
    else:
      self.dom_nodes['anvil-m3-text-container'].style.justifyContent = value
    self.dom_nodes['anvil-m3-text'].style.textAlign = value

  @anvil_prop
  @property
  def font_size(self, value) -> float:
    """The font size of text displayed on this component."""
    if value:
      value = f'{value}px'
    self.dom_nodes['anvil-m3-text'].style.fontSize = value
    self.dom_nodes['anvil-m3-text-container'].style.fontSize = value

  @anvil_prop
  @property
  def line_height(self, value) -> str:
    """The line height of this component."""
    self.dom_nodes['anvil-m3-text-container'].style.lineHeight = value
    self.dom_nodes['anvil-m3-text'].style.lineHeight = value

  @anvil_prop
  @property
  def icon(self, value) -> str:
    """The icon to display on this component."""
    if value:
      self.dom_nodes['anvil-m3-text-icon'].style.marginRight = "8px"
    else:
      self.dom_nodes['anvil-m3-text-icon'].style.marginRight = ""
    self.dom_nodes['anvil-m3-text-icon'].innerText = value[3:]

  @anvil_prop
  @property
  def style(self, value) -> str:
    """Role of the text component: display, headline or title."""
    self.dom_nodes['anvil-m3-text'].classList.remove(
      'anvil-m3-text-label', 'anvil-m3-text-body'
    )
    self.dom_nodes['anvil-m3-text'].classList.add(f'anvil-m3-text-{value}')
    self.dom_nodes['anvil-m3-text-container'].classList.remove(
      'anvil-m3-text-label', 'anvil-m3-text-body'
    )
    self.dom_nodes['anvil-m3-text-container'].classList.add(f'anvil-m3-text-{value}')

  @anvil_prop
  @property
  def scale(self, value) -> str:
    """The size of the text component."""
    self.dom_nodes['anvil-m3-text'].classList.remove(
      'anvil-m3-text-large', 'anvil-m3-text-medium', 'anvil-m3-text-small'
    )
    self.dom_nodes['anvil-m3-text-container'].classList.remove(
      'anvil-m3-text-large', 'anvil-m3-text-medium', 'anvil-m3-text-small'
    )
    self.dom_nodes['anvil-m3-text'].classList.add(f'anvil-m3-text-{value}')
    self.dom_nodes['anvil-m3-text-container'].classList.add(f'anvil-m3-text-{value}')


#!defClass(m3, Text, anvil.Component)!:
