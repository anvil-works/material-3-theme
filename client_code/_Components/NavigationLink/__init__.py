import anvil.designer
import anvil.js
from anvil import *

from ..._utils.properties import (
  anvil_prop,
  bold_property,
  color_property,
  font_family_property,
  font_size_property,
  get_unset_spacing,
  get_unset_value,
  innerText_property,
  italic_property,
  role_property,
  simple_prop,
  spacing_property,
  tooltip_property,
  underline_property,
)
from ._anvil_designer import NavigationLinkTemplate


class NavigationLink(NavigationLinkTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dom_nodes['anvil-m3-navigation-link'].addEventListener(
      "click", self._handle_click
    )
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_cleanup(self, **event_args):
    if anvil.designer.in_designer:
      anvil.designer.register_interaction(
        self,
        self.dom_nodes['anvil-m3-navigation-link'],
        'dblclick',
        lambda x: anvil.designer.start_editing_form(self.navigate_to),
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
    if self.navigate_to:
      open_form(self.navigate_to)
      self.selected = True

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(
            self, "text", self.dom_nodes['anvil-m3-navigation-link-text']
          )
        },
      }
    ]

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes["anvil-m3-navigation-link-container"]
    sp = get_unset_spacing(el, el, self.spacing)
    tfs = get_unset_value(
      self.dom_nodes['anvil-m3-navigation-link-text'], "fontSize", self.font_size
    )
    ifs = get_unset_value(
      self.dom_nodes['anvil-m3-navigation-link-icon'], "fontSize", self.icon_size
    )
    return {"font_size": tfs, "icon_size": ifs, "spacing": sp}

  #!componentEvent(m3.NavigationLink)!1: {name: "click", description: "When the NavigationLink is clicked."}
  #!componentEvent(m3.NavigationLink)!1: {name: "show", description: "When the NavigationLink is shown on the screen."}
  #!componentEvent(m3.NavigationLink)!1: {name: "hide", description: "When the NavigationLink is removed from the screen."}

  #!componentProp(m3.NavigationLink)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.NavigationLink)!1: {name:"text",type:"string",description:"The text displayed on this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
  #!componentProp(m3.NavigationLink)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(m3.NavigationLink)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(m3.NavigationLink)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(m3.NavigationLink)!1: {name:"text_color",type:"color",description:"The color of the text on the component."}
  #!componentProp(m3.NavigationLink)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.NavigationLink)!1: {name:"url",type:"string",description:"TThe target URL of the link. Can be set to a URL string or to a Media object."}
  #!componentProp(m3.NavigationLink)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
  #!componentProp(m3.NavigationLink)!1: {name:"selected",type:"boolean",description:"If True, the component is in the selected state."}
  #!componentProp(m3.NavigationLink)!1: {name:"badge",type:"boolean",description:"If True, display a notification badge on the icon."}
  #!componentProp(m3.NavigationLink)!1: {name:"badge_count",type:"number",description:"The number to display on the badge."}
  #!componentProp(m3.NavigationLink)!1: {name:"navigate_to",type:"form",description:"The Form to navigate to when the link is clicked."}
  #!componentProp(m3.NavigationLink)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(m3.NavigationLink)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}

  visible = HtmlTemplate.visible
  text = innerText_property('anvil-m3-navigation-link-text')
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
  spacing = spacing_property('anvil-m3-navigation-link-container')
  background_color = color_property(
    'anvil-m3-navigation-link-container', 'backgroundColor', 'background_color'
  )
  navigate_to = simple_prop("navigate_to")

  @anvil_prop
  @property
  def url(self, value) -> str:
    """TThe target URL of the link. Can be set to a URL string or to a Media object."""
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].href = value
    else:
      self.dom_nodes['anvil-m3-navigation-link'].href = 'javascript:void(0)'

  @anvil_prop
  @property
  def icon(self, value) -> str:
    """The icon to display on this component."""
    link_icon = self.dom_nodes['anvil-m3-navigation-link-icon']
    if value:
      link_icon.className = ""
      link_icon.classList.add("material-symbols-outlined")
      link_icon.innerText = value[3:]

  @anvil_prop
  @property
  def selected(self, value) -> bool:
    """If True, the component is in the selected state."""
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add(
        'anvil-m3-navigation-link-selected'
      )
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove(
        'anvil-m3-navigation-link-selected'
      )

  @anvil_prop
  @property
  def badge(self, value) -> bool:
    """If True, display a notification badge on the icon."""
    if value:
      self.dom_nodes['anvil-m3-navigation-link'].classList.add('anvil-m3-has-badge')
    else:
      self.dom_nodes['anvil-m3-navigation-link'].classList.remove('anvil-m3-has-badge')

  @anvil_prop
  @property
  def badge_count(self, value) -> bool:
    """If True, display a notification badge on the icon."""
    if value and self.badge:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-icon-badge'].classList.add("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = value
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.add(
        "anvil-m3-large-badge"
      )
    else:
      self.dom_nodes['anvil-m3-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-icon-badge'].classList.remove("anvil-m3-large-badge")
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].innerHTML = ""
      self.dom_nodes['anvil-m3-navigation-drawer-icon-badge'].classList.remove(
        "anvil-m3-large-badge"
      )


#!defClass(m3, NavigationLink, anvil.Component)!:
