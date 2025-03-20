from anvil import *

from ..._utils.properties import anvil_prop, get_unset_value, margin_property, style_property, get_unset_margin
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
      

    
