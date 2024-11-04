from ._anvil_designer import ButtonTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from ...Functions import color_property, role_property, tooltip_property, custom_bold_property, font_family_property, font_size_property, style_property, property_with_callback, underline_property, bold_property, italic_property, margin_property 
from anvil import HtmlTemplate
import anvil.designer

class Button(ButtonTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._text = properties.get('text', '')
    self._tooltip_node = None
    self.init_components(**properties)
    
    self._handle_click = self._handle_click
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-button'].addEventListener("click", self._handle_click)
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-button'].removeEventListener("click", self._handle_click)

  def _handle_click(self, event):
    event.preventDefault()
    if self.enabled:
      keys = {'shift': event.shiftKey, 'alt': event.altKey, 'ctrl': event.ctrlKey, 'meta': event.metaKey}
      self.raise_event("click", keys=keys)

  def _anvil_get_interactions_(self):
    return [{
      "type": "whole_component",
      "title": "Edit text",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-button-text'])
      }
    }]

  def _set_align(self, value):
    self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-full-width', False)
    if value == 'full':
      self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-full-width', True)
    else:
      self.dom_nodes['anvil-m3-button-component'].style.justifyContent = value
      
  def _set_icon(self):
    if self.icon:
      self.dom_nodes['anvil-m3-button-icon'].innerText = self.icon
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
      self.dom_nodes['anvil-m3-button-text'].innerText = self.text
    else:
      if not self.icon:
        if anvil.designer.in_designer:
          self.dom_nodes['anvil-m3-button-text'].innerText = anvil.designer.get_design_name(self)
          self.dom_nodes['anvil-m3-button-text'].classList.add('anvil-m3-textlessComponentText')
        else: 
          self.dom_nodes['anvil-m3-button-text'].innerText = "Button"
      else:
        self.dom_nodes['anvil-m3-button-text'].innerText = ""
      
  def _update_button_look(self, value = None):
    buttonNode = self.dom_nodes['anvil-m3-button']
    iconNode = self.dom_nodes['anvil-m3-button-icon']
    textNode = self.dom_nodes['anvil-m3-button-text']

    buttonNode.classList.remove('anvil-m3-icon-padding')
    textNode.classList.remove('anvil-m3-textlessComponentText')
    buttonNode.classList.remove('anvil-m3-no-text')
    
    self._set_icon()
    self._set_text()

  def _set_enabled(self, value):
    if value:
      self.dom_nodes['anvil-m3-button'].removeAttribute("disabled")
    else:
      self.dom_nodes['anvil-m3-button'].setAttribute("disabled", " ")
      
  def _set_appearance(self, value):
    button = self.dom_nodes['anvil-m3-button']
    button.classList.remove('anvil-m3-elevated')
    button.classList.remove('anvil-m3-filled')
    button.classList.remove('anvil-m3-tonal')
    button.classList.remove('anvil-m3-outlined')
    if value and value != 'text':
      button.classList.add(f"anvil-m3-{value}")
      
  def _set_icon_position(self, value):
    self.dom_nodes['anvil-m3-button'].classList.toggle('anvil-m3-right-icon', value == 'right')
      
  def form_show(self, **event_args):
    self._update_button_look()
    print("")

  
  align = property_with_callback('align', _set_align)
  role = role_property('anvil-m3-button')
  appearance = property_with_callback("appearance", _set_appearance)
  enabled = property_with_callback("enabled", _set_enabled)
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
  background_color = color_property('anvil-m3-button', 'backgroundColor', 'background_color')
  margin = margin_property('anvil-m3-button-component')
  border = style_property('anvil-m3-button', 'border', 'border')
  tooltip = tooltip_property('anvil-m3-button')
  icon_position = property_with_callback('icon_position', _set_icon_position)
  visible = HtmlTemplate.visible

  #!componentProp(material_3.Button)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."} 
  #!componentProp(material_3.Button)!1: {name:"appearance",type:"enum",options:["filled", "elevated", "tonal", "outlined", "text"],description:"A predefined style for this component."}  
  #!componentProp(material_3.Button)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.Button)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(material_3.Button)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"} 
  #!componentProp(material_3.Button)!1: {name:"text_color",type:"color",description:"The colour of the text on the component."} 
  #!componentProp(material_3.Button)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(material_3.Button)!1: {name:"icon",type:"enum",description:"The icon to display on this component."} 
  #!componentProp(material_3.Button)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(material_3.Button)!1: {name:"font_size",type:"number",description:"The font size of the text displayed on this component."}
  #!componentProp(material_3.Button)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(material_3.Button)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(material_3.Button)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(material_3.Button)!1: {name:"icon_color",type:"color",description:"The colour of the icon displayed on this component."}
  #!componentProp(material_3.Button)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(material_3.Button)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(material_3.Button)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!componentProp(material_3.Button)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(material_3.Button)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.Button)!1: {name:"icon_position",type:"enum",options:["left", "right"],description:"The alignment of the icon on this component."}
  #!componentProp(material_3.Button)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(material_3.Button)!1: {name: "click", description: "When the component is clicked.", parameters:[]}

#!defClass(material_3, Button, anvil.Component)!:
