from ._anvil_designer import NavigationLinkTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from ...Functions import color_property, role_property, tooltip_property, href_property, innerHTML_property, font_family_property, font_size_property, margin_property, italic_property, bold_property, underline_property
import anvil.designer

#Currently, material_icon works and not icon (because they can't both work at the same time)
class NavigationLink(NavigationLinkTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._tooltip_node = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)
    
  def _on_mount(self, **event_args):
    self.dom_nodes['anvil-m3-navigation-link'].addEventListener("click", self._handle_click)
    
  def _on_cleanup(self, **event_args):
    self.dom_nodes['anvil-m3-navigation-link'].removeEventListener("click", self._handle_click)
    
    if anvil.designer.in_designer:
      anvil.designer.register_interaction(self, self.dom_nodes['anvil-m3-navigation-link'], 'dblclick', lambda x: anvil.designer.start_editing_form(self.navigate_to))

  def _handle_click(self, event):
    self.raise_event("click", event=event)
    if self.navigate_to:
      open_form(self.navigate_to)
      self.selected = True

  def _anvil_get_interactions_(self):
    return [{
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(self, "text", self.dom_nodes['anvil-m3-navigation-link-text'])
        }
      }]

  #!componentEvent(material_3.NavigationLink)!1: {name: "click", description: "When the NavigationLink is clicked."}
  #!componentEvent(material_3.NavigationLink)!1: {name: "show", description: "When the NavigationLink is shown on the screen."}
  #!componentEvent(material_3.NavigationLink)!1: {name: "hide", description: "When the NavigationLink is removed from the screen."}

  #!componentProp(material_3.NavigationLink)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"text",type:"string",description:"The text displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(material_3.NavigationLink)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(material_3.NavigationLink)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(material_3.NavigationLink)!1: {name:"text_color",type:"color",description:"The color of the text on the component."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!componentProp(material_3.NavigationLink)!1: {name:"url",type:"string",description:"TThe target URL of the link. Can be set to a URL string or to a Media object."}
  #!componentProp(material_3.NavigationLink)!1: {name:"material_icon",type:"enum",description:"The icon to display on this component."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"selected",type:"boolean",description:"If True, the component is in the selected state."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"badge",type:"boolean",description:"If True, display a notification badge on the icon."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"badge_count",type:"number",description:"The number to display on the badge."} 
  #!componentProp(material_3.NavigationLink)!1: {name:"navigate_to",type:"form",description:"The Form to navigate to when the link is clicked."} 
  
  visible = HtmlTemplate.visible
  text = innerHTML_property('anvil-m3-navigation-link-text')
  role = role_property('anvil-m3-navigation-link')
  italic = italic_property('anvil-m3-navigation-link-text')
  bold = bold_property('anvil-m3-navigation-link-text')
  underline = underline_property('anvil-m3-navigation-link-text')
  text_color = color_property('anvil-m3-navigation-link-text', 'color', 'text_color')
  icon_color = color_property('anvil-m3-navigation-link-icon', 'color', 'icon_color')
  font_family = font_family_property('anvil-m3-navigation-link-text')
  font_size = font_size_property('anvil-m3-navigation-link-text', 'font_size')
  icon_size = font_size_property('anvil-m3-navigation-link-icon', 'icon_size')
  tooltip = tooltip_property('anvil-m3-navigation-link-container')
  margin = margin_property('anvil-m3-navigation-link-container')

  @property
  def url(self):
    return self._props.get('url')

  @url.setter
  def url(self, value):
    if value:
      self._props['url'] = value
      self.dom_nodes['anvil-m3-navigation-link'].href = value
    else:
      self.dom_nodes['anvil-m3-navigation-link'].href = 'javascript:void(0)'

  @property
  def material_icon(self):
    return self._material_icon

  @material_icon.setter
  def material_icon(self, value):
    link_icon = self.dom_nodes['anvil-m3-navigation-link-icon']
    self._material_icon = value
    if value:
      link_icon.className = ""
      link_icon.classList.add("material-symbols-outlined")
      link_icon.innerText = value

  @property
  def selected(self):
    return self._selected

  @selected.setter
  def selected(self, value):
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add('anvil-m3-navigation-link-selected')
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove('anvil-m3-navigation-link-selected')
    self._selected = value

  @property
  def badge(self):
    return self._badge

  @badge.setter
  def badge(self, value):
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add('anvil-m3-has-badge')
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove('anvil-m3-has-badge')
    self._badge = value

  @property
  def badge_count(self):
    return self._badge_count

  @badge_count.setter
  def badge_count(self, value):
    if value and self.badge:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-icon-badge'].classList.add("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.add("anvil-m3-large-badge")
    else:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-icon-badge'].classList.remove("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.remove("anvil-m3-large-badge")
    self._badge_count = value

  @property
  def navigate_to(self):
    return self._navigate_to

  @navigate_to.setter
  def navigate_to(self, value):
    self._navigate_to = value

#!defClass(material_3, NavigationLink, anvil.Component)!:
