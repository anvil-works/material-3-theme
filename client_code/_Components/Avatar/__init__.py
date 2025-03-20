from anvil import *

from ..._utils.properties import (
  anvil_prop,
  border_property,
  color_property,
  get_unset_margin,
  get_unset_value,
  margin_property,
  style_property,
  tooltip_property,
)
from ._anvil_designer import AvatarTemplate


class Avatar(AvatarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self.initials_div = self.dom_nodes['anvil-m3-avatar-initials']
    self.fallback_icon_div = self.dom_nodes['anvil-m3-avatar-icon']
    self.image_div = self.dom_nodes['anvil-m3-avatar-image']
    self.avatar_div = self.dom_nodes['anvil-m3-avatar']
    self.init_components(**properties)

  margin = margin_property('anvil-m3-avatar')
  align = style_property('anvil-m3-avatar-container', 'justifyContent', 'align')
  visible = HtmlTemplate.visible
  border = border_property('anvil-m3-avatar')
  tooltip = tooltip_property('anvil-m3-iconbutton-component')
  fallback_icon_color = color_property('anvil-m3-avatar-icon', 'color', 'fallback_icon_color')
  background_color = color_property(
    'anvil-m3-avatar', 'backgroundColor', 'background_color'
  )
  text_color = color_property('anvil-m3-avatar-initials', 'color', 'text_color')

  @anvil_prop
  @property
  def fallback_icon(self, value) -> str:
    """The icon to display on this component."""
    if self.image or self.name:
      self.fallback_icon_div.style.display = "none"
    else:
      self.fallback_icon_div.style.display = "block"
      self.fallback_icon_div.className = ""
      self.fallback_icon_div.classList.add("material-symbols-outlined")
      self.fallback_icon_div.innerText = value[3:]

  @anvil_prop
  @property
  def image(self, value):
    if value: 
      self.image_div.style.display = "block"
      self.image_div.src = value
      self.initials_div.style.display = "none"
      self.fallback_icon_div.style.display = "none"
    else:
      self.image_div.style.display = "none"
      if self.name:
        self.initials_div.style.display = "block"
        self.fallback_icon_div.style.display = "none"
      else:
        self.fallback_icon_div.style.display = "block"
        self.initials_div.style.display = "none"

  @anvil_prop
  @property
  def name(self, value) -> str:
    if self.image: 
      self.image_div.style.display = "block"
      self.initials_div.style.display = "none"
    elif value:
      self.initials_div.style.display = "block"
      self.fallback_icon_div.style.display = "none"
      self.image_div.style.display = "none"
      names = value.split()
      initials = ""
      for n in names:
        initials += n[0]
      self.initials_div.innerText = initials
    elif not value:
      self.fallback_icon_div.style.display = "block"
      self.initials_div.style.display = "none"

  @anvil_prop
  @property
  def size(self, value):
    if value:
      self.avatar_div.style.height = f'{value}px'
      self.image_div.style.height = f'{value}px'
      self.avatar_div.style.width = f'{value}px'
      self.image_div.style.width = f'{value}px'
    else:
      self.avatar_div.style.height = '40px'
      self.image_div.style.height = '40px'
      self.avatar_div.style.width = '40px'
      self.image_div.style.width = '40px'
      
  @anvil_prop
  @property
  def appearance(self, value) -> str:
    for c in ['anvil-m3-avatar-filled', 'anvil-m3-avatar-tonal', 'anvil-m3-avatar-outlined']:
      self.avatar_div.classList.remove(c)
    self.avatar_div.classList.add(f"anvil-m3-avatar-{value}")

  def _anvil_get_unset_property_values_(self):
    sz = get_unset_value(
      self.avatar_div, "height", self.size
    )
    m = get_unset_margin(self.avatar_div, self.margin)
    return {"size": sz, "margin": m}


  #!componentProp(m3.Avatar)!1: {name:"align",type:"enum",description:"The position of this component in the available space."}
  #!componentProp(m3.Avatar)!1: {name:"appearance",type:"enum",options:["filled", "tonal", "outlined"],description:"A predefined style for this component."}
  #!componentProp(m3.Avatar)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.Avatar)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.Avatar)!1: {name:"fallback_icon",type:"enum",description:"The icon to display if no image or name is provided."}
  #!componentProp(m3.Avatar)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.Avatar)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(m3.Avatar)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!componentProp(m3.Avatar)!1: {name:"fallback_icon_color",type:"color",description:"The colour of the icon displayed on this component."}
  #!componentProp(m3.Avatar)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(m3.Avatar)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}


    
#!defClass(m3,Avatar,anvil.Component)!:
