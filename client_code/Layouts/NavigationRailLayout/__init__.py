from anvil import *
from anvil.js import window

from ..._utils.properties import (
  anvil_prop,
  color_property,
  padding_property,
  theme_color_to_css,
)
from ._anvil_designer import NavigationRailLayoutTemplate


class NavigationRailLayout(NavigationRailLayoutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self._props = properties
    self.app_bar = self.dom_nodes['anvil-m3-top-app-bar']
    self.nav_drawer_open_btn = self.dom_nodes['anvil-m3-drawer-open-btn']
    self.nav_rail = self.dom_nodes['anvil-m3-navigation-rail']
    self.nav_drawer_scrim = self.dom_nodes['anvil-m3-navigation-drawer-scrim']
    self.sidesheet_scrim = self.dom_nodes['anvil-m3-sidesheet-scrim']
    self.sidesheet = self.dom_nodes['anvil-m3-sidesheet']
    self.content = self.dom_nodes['anvil-m3-content']
    self.sidesheet_previous_state = False
    self.zero_width_timeout = None
    self.shown_timeout = None
    self.init_components(**properties)

    window.document.addEventListener('scroll', self._add_scroll_class)
    self.nav_drawer_open_btn.addEventListener('click', self.open_nav_drawer)
    self.nav_drawer_scrim.addEventListener('click', self.hide_nav_drawer)

  #!defMethod(_)!2: "Open the navigation drawer." ["open_nav_drawer"]
  def open_nav_drawer(self, e=None):
    window.clearTimeout(self.zero_width_timeout)
    window.clearTimeout(self.shown_timeout)
    self.nav_rail.style.width = '360px'
    self.nav_rail.style.left = "0px"
    self.nav_rail.classList.add('anvil-m3-shown')
    self.nav_drawer_scrim.animate(
      [{'opacity': '0'}, {'opacity': '1'}], {'duration': 250, 'iterations': 1}
    )

  #!defMethod(_)!2: "Hide the navigation drawer." ["hide_nav_drawer"]
  def hide_nav_drawer(self, e=None):
    self.nav_rail.style.left = "-101%"
    self.nav_drawer_scrim.animate(
      [{'opacity': '1'}, {'opacity': '0'}], {'duration': 250, 'iterations': 1}
    )
    self.zero_width_timeout = window.setTimeout(
      lambda: self.nav_rail.style.setProperty('width', '0px'), 250
    )
    self.shown_timeout = window.setTimeout(
      lambda: self.nav_rail.classList.remove('anvil-m3-shown'), 245
    )

  #!defMethod(_)!2: "Add components to the navigation rail." ["add_to_nav_rail"]
  def add_to_nav_rail(self, component):
    self.slots['nav_rail_slot'].add_component(component)

  def _add_scroll_class(self, e):
    if self.app_bar.classList.contains('anvil-m3-scrolled'):
      if window.scrollY == 0:
        self.app_bar.classList.remove('anvil-m3-scrolled')
    else:
      self.app_bar.classList.add('anvil-m3-scrolled')

  def _open_sidesheet(self):
    if self.sidesheet_previous_state:
      self.sidesheet.classList.add('anvil-m3-display-block')
      window.setTimeout(lambda: self.sidesheet.classList.add('anvil-m3-open'), 1)
      self.sidesheet_scrim.classList.add('anvil-m3-sidesheet-open')
      self.content.classList.add('anvil-m3-transition-width')
      window.setTimeout(
        lambda: self.content.classList.add('anvil-m3-sidesheet-open'), 5
      )
      self.sidesheet_scrim.animate(
        [{'opacity': '0'}, {'opacity': '1'}], {'duration': 250, 'iterations': 1}
      )
    else:
      self.sidesheet_scrim.classList.add('anvil-m3-sidesheet-open')
      self.sidesheet_scrim.style.opacity = 1
      self.sidesheet.classList.add('anvil-m3-display-block')
      self.sidesheet.classList.add('anvil-m3-open')
      self.content.classList.add('anvil-m3-sidesheet-open')
      self.sidesheet_previous_state = True

  def _close_sidesheet(self):
    self.content.classList.add('anvil-m3-transition-width')
    self.sidesheet_scrim.animate(
      [{'opacity': '1'}, {'opacity': '0'}], {'duration': 250, 'iterations': 1}
    )
    window.setTimeout(
      lambda: self.sidesheet_scrim.classList.remove('anvil-m3-sidesheet-open'), 245
    )
    self.sidesheet.classList.remove('anvil-m3-open')
    self.content.classList.remove('anvil-m3-sidesheet-open')
    window.setTimeout(
      lambda: self.content.classList.remove('anvil-m3-sidesheet-open'), 245
    )
    window.setTimeout(
      lambda: self.sidesheet.classList.remove('anvil-m3-display-block'), 245
    )

  def _icon_button_1_click(self, **event_args):
    self.show_sidesheet = False

  #!componentEvent(m3.NavigationRailLayout)!1: {name: "show", description: "When the Form is shown on the screen."}
  #!componentEvent(m3.NavigationRailLayout)!1: {name: "hide", description: "When the Form is removed from the screen."}
  #!componentEvent(m3.NavigationRailLayout)!1: {name: "refreshing_data_bindings", description: "When refresh_data_bindings is called."}

  #!componentProp(m3.NavigationRailLayout)!1: {name:"navigation_rail_color",type:"color",description:"The color of the navigation rail on Forms using this Layout."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"background_color",type:"color",description:"The background color of Forms using this Layout."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"text_color",type:"color",description:"The default color of the text on Forms using this Layout."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"navigation_rail_collapse_to",type:"enum",options:["bottom_app_bar","modal_navigation_drawer"],description:"The way the side navigation will collapse on mobile."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"navigation_rail_vertical_align",type:"enum",options:["top", "center", "bottom"], description:"The vertical position of the content in the navigation rail."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"show_sidesheet",type:"boolean",description:"If True, the sidesheet will be shown on Forms using this Layout."}
  #!componentProp(m3.NavigationRailLayout)!1: {name:"content_padding",type:"padding",description:"The padding (pixels) around the content of the page."}

  navigation_rail_color = color_property(
    'anvil-m3-navigation-rail', 'backgroundColor', 'navigation_rail_color'
  )
  content_padding = padding_property('anvil-m3-content')

  @anvil_prop
  @property
  def background_color(self, value) -> str:
    """The background color of Forms using this Layout."""
    if value:
      value = theme_color_to_css(value)
    window.document.body.style.backgroundColor = value

  @anvil_prop
  @property
  def text_color(self, value) -> str:
    """The default color of the text on Forms using this Layout."""
    if value:
      value = theme_color_to_css(value)
    window.document.body.style.color = value

  @anvil_prop
  @property
  def navigation_rail_collapse_to(self, value) -> str:
    """The way the side navigation will collapse on mobile."""
    value = value.lower().replace('_', '-')
    for c in ['anvil-m3-bottom-app-bar', 'anvil-m3-modal-navigation-drawer']:
      self.nav_rail.classList.remove(c)
      self.content.classList.remove(c)
    self.nav_rail.classList.add(f"anvil-m3-{value}")
    self.content.classList.add(f"anvil-m3-{value}")

  @anvil_prop
  @property
  def navigation_rail_vertical_align(self, value) -> str:
    """The vertical position of the content in the navigation rail."""
    value = value.lower()
    for c in ['anvil-m3-align-top', 'anvil-m3-align-center', 'anvil-m3-align-bottom']:
      self.nav_rail.classList.remove(c)
    self.nav_rail.classList.add(f"anvil-m3-align-{value}")

  @property
  def show_sidesheet(self):
    return self._show_sidesheet

  @show_sidesheet.setter
  def show_sidesheet(self, value):
    self._show_sidesheet = value
    if value:
      self._open_sidesheet()
    else:
      self._close_sidesheet()


#!defClass(m3, NavigationRailLayout, anvil.Component)!:
