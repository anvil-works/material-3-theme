import anvil
import anvil.designer
from anvil.property_utils import set_element_spacing

from ..._utils.properties import (
  anvil_prop,
  border_property,
  color_property,
  font_family_property,
  get_unset_spacing,
  get_unset_value,
  inline_editing,
  italic_property,
  role_property,
  tooltip_property,
)
from ._anvil_designer import HeadingTemplate


class Heading(HeadingTemplate):
  def __init__(self, **properties):
    self.tag = anvil.ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self._set_designer_text_placeholder, self._start_inline_editing = inline_editing(
      self,
      self.dom_nodes['anvil-m3-heading-container'],
      self._set_text,
      get_node=lambda: self.dom_nodes[f'anvil-m3-heading-{self.style}'],
    )
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

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
    full_el = self.dom_nodes["anvil-m3-heading-container"]
    sp = get_unset_spacing(full_el, full_el, self.spacing)
    if self.style == "display":
      h = self.dom_nodes['anvil-m3-heading-display']
    elif self.style == "headline":
      h = self.dom_nodes['anvil-m3-heading-headline']
    elif self.style == "title":
      h = self.dom_nodes['anvil-m3-heading-title']
    fs = get_unset_value(h, "fontSize", self.font_size)
    ifs = get_unset_value(
      self.dom_nodes['anvil-m3-heading-icon'], "fontSize", self.icon_size
    )
    return {"spacing": sp, "font_size": fs, "icon_size": ifs}

  def _set_text(self, value):
    self.dom_nodes['anvil-m3-heading-display'].innerText = str(value if value is not None else "")
    self.dom_nodes['anvil-m3-heading-headline'].innerText = str(value if value is not None else "")
    self.dom_nodes['anvil-m3-heading-title'].innerText = str(value if value is not None else "")

  #!componentEvent(m3.Heading)!1: {name: "show", description: "When the Heading is shown on the screen."}
  #!componentEvent(m3.Heading)!1: {name: "hide", description: "When the Heading is removed from the screen."}

  #!componentProp(m3.Heading)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.Heading)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(m3.Heading)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(m3.Heading)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(m3.Heading)!1: {name:"text_color",type:"color",description:"The color of the text on the component."}
  #!componentProp(m3.Heading)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(m3.Heading)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
  #!componentProp(m3.Heading)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.Heading)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.Heading)!1: {name:"align",type:"enum",options:['left', 'right', 'center', 'justify'], description:"The position of this component in the available space."}
  #!componentProp(m3.Heading)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(m3.Heading)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(m3.Heading)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(m3.Heading)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(m3.Heading)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(m3.Heading)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
  #!componentProp(m3.Heading)!1: {name:"style",type:"enum",options:['display', 'headline', 'title'],description:"Role of the heading component: display, headline or title."}
  #!componentProp(m3.Heading)!1: {name:"scale",type:"enum",options:['small', 'medium', 'large'],description:"The size of the heading component."}
  #!componentProp(m3.Heading)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.Heading)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(m3.Heading)!1: {name:"line_height",type:"string",description:"The line height of this component."}

  visible = anvil.HtmlTemplate.visible
  italic = italic_property('anvil-m3-heading-container')
  border = border_property('anvil-m3-heading-container')
  font_family = font_family_property('anvil-m3-heading-container')
  text_color = color_property('anvil-m3-heading-container', 'color', 'text_color')
  icon_color = color_property('anvil-m3-heading-icon', 'color', 'icon_color')
  background_color = color_property(
    'anvil-m3-heading-container', 'backgroundColor', 'background_color'
  )
  tooltip = tooltip_property('anvil-m3-heading-container')
  role = role_property('anvil-m3-heading-container')

  @anvil_prop
  @property
  def align(self, value) -> str:
    """The position of this component in the available space."""
    if value == 'justify':
      self.dom_nodes['anvil-m3-heading-container'].style.justifyContent = 'left'
    else:
      self.dom_nodes['anvil-m3-heading-container'].style.justifyContent = value
    self.dom_nodes['anvil-m3-heading-container'].style.textAlign = value

  @anvil_prop
  @property
  def font_size(self, value) -> int:
    """The font size of text displayed on this component."""
    if value:
      self.dom_nodes['anvil-m3-heading-display'].style.fontSize = f'{value}px'
      self.dom_nodes['anvil-m3-heading-headline'].style.fontSize = f'{value}px'
      self.dom_nodes['anvil-m3-heading-title'].style.fontSize = f'{value}px'
      self.dom_nodes['anvil-m3-heading-container'].style.fontSize = f'{value}px'
    else:
      self.dom_nodes['anvil-m3-heading-display'].style.fontSize = ''
      self.dom_nodes['anvil-m3-heading-headline'].style.fontSize = ''
      self.dom_nodes['anvil-m3-heading-title'].style.fontSize = ''
      self.dom_nodes['anvil-m3-heading-container'].style.fontSize = ''

  @anvil_prop
  @property
  def icon_size(self, value) -> float:
    """The size (pixels) of the icon displayed on this component."""
    if value:
      value = f'{value}px'
    self.dom_nodes['anvil-m3-heading-icon'].style.fontSize = value

  @anvil_prop
  @property
  def underline(self, value) -> bool:
    """If True, this component’s text will be underlined."""
    if value:
      self.dom_nodes['anvil-m3-heading-display'].style.textDecoration = 'underline'
      self.dom_nodes['anvil-m3-heading-headline'].style.textDecoration = 'underline'
      self.dom_nodes['anvil-m3-heading-title'].style.textDecoration = 'underline'
    else:
      self.dom_nodes['anvil-m3-heading-display'].style.textDecoration = 'none'
      self.dom_nodes['anvil-m3-heading-headline'].style.textDecoration = 'none'
      self.dom_nodes['anvil-m3-heading-title'].style.textDecoration = 'none'

  @anvil_prop
  @property
  def bold(self, value) -> bool:
    """If True, this component’s text will be bold."""
    if value:
      self.dom_nodes['anvil-m3-heading-display'].style.fontWeight = 'bold'
      self.dom_nodes['anvil-m3-heading-headline'].style.fontWeight = 'bold'
      self.dom_nodes['anvil-m3-heading-title'].style.fontWeight = 'bold'
    else:
      self.dom_nodes['anvil-m3-heading-display'].style.fontWeight = 'normal'
      self.dom_nodes['anvil-m3-heading-headline'].style.fontWeight = 'normal'
      self.dom_nodes['anvil-m3-heading-title'].style.fontWeight = 'normal'

  @anvil_prop
  @property
  def text(self, value) -> str:
    """The text displayed on this component"""
    self._set_text(value)
    self._set_designer_text_placeholder()

  @anvil_prop
  @property
  def icon(self, value) -> str:
    """The icon to display on this component."""
    if value:
      self.dom_nodes['anvil-m3-heading-icon'].style.marginRight = "8px"
    else:
      self.dom_nodes['anvil-m3-heading-icon'].style.marginRight = ""
    self.dom_nodes['anvil-m3-heading-icon'].innerText = value[3:]

  @anvil_prop
  @property
  def style(self, value) -> str:
    """Role of the heading component: display, headline or title."""
    display = self.dom_nodes['anvil-m3-heading-display']
    headline = self.dom_nodes['anvil-m3-heading-headline']
    title = self.dom_nodes['anvil-m3-heading-title']
    self.dom_nodes['anvil-m3-heading-container'].classList.remove(
      'anvil-m3-heading-display', 'anvil-m3-heading-headline', 'anvil-m3-heading-title'
    )
    self.dom_nodes['anvil-m3-heading-container'].classList.add(
      f'anvil-m3-heading-{value}'
    )
    if value == 'display':
      display.style.display = 'block'
      headline.style.display = 'none'
      title.style.display = 'none'
    elif value == 'headline':
      display.style.display = 'none'
      headline.style.display = 'block'
      title.style.display = 'none'
    elif value == 'title':
      display.style.display = 'none'
      headline.style.display = 'none'
      title.style.display = 'block'

  @anvil_prop
  @property
  def scale(self, value):
    self.dom_nodes['anvil-m3-heading-display'].classList.remove(
      'anvil-m3-heading-large', 'anvil-m3-heading-medium', 'anvil-m3-heading-small'
    )
    self.dom_nodes['anvil-m3-heading-headline'].classList.remove(
      'anvil-m3-heading-large', 'anvil-m3-heading-medium', 'anvil-m3-heading-small'
    )
    self.dom_nodes['anvil-m3-heading-title'].classList.remove(
      'anvil-m3-heading-large', 'anvil-m3-heading-medium', 'anvil-m3-heading-small'
    )
    self.dom_nodes['anvil-m3-heading-container'].classList.remove(
      'anvil-m3-heading-large', 'anvil-m3-heading-medium', 'anvil-m3-heading-small'
    )
    self.dom_nodes['anvil-m3-heading-display'].classList.add(
      f'anvil-m3-heading-{value}'
    )
    self.dom_nodes['anvil-m3-heading-headline'].classList.add(
      f'anvil-m3-heading-{value}'
    )
    self.dom_nodes['anvil-m3-heading-title'].classList.add(f'anvil-m3-heading-{value}')
    self.dom_nodes['anvil-m3-heading-container'].classList.add(
      f'anvil-m3-heading-{value}'
    )

  @anvil_prop
  @property
  def spacing(self, value):
    set_element_spacing(self.dom_nodes['anvil-m3-heading-container'], value)

  @anvil_prop
  @property
  def line_height(self, value):
    self.dom_nodes['anvil-m3-heading-display'].style.lineHeight = value
    self.dom_nodes['anvil-m3-heading-headline'].style.lineHeight = value
    self.dom_nodes['anvil-m3-heading-title'].style.lineHeight = value
    self.dom_nodes['anvil-m3-heading-container'].style.lineHeight = {value}


#!defClass(m3, Heading, anvil.Component)!:
