from anvil import *
from anvil import HtmlTemplate
from anvil.js.window import document

from ..._utils import noop
from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    border_property,
    color_property,
    enabled_property,
    get_unset_margin,
    get_unset_value,
)
from ..MenuMixin import MenuMixin
from ._anvil_designer import AvatarMenuTemplate


class AvatarMenu(MenuMixin, AvatarMenuTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._menu_node = self.dom_nodes['anvil-m3-avatarMenu-items-container']
        self._button_node = self.dom_nodes['anvil-m3-avatarMenu-button']
        
        MenuMixin.__init__(self._button_node, self._menu_node)
        
        self._design_name = ""
        
        self.init_components(**properties)
    
        self.add_event_handler("x-anvil-page-added", self._on_mount)
        self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    def _on_mount(self, **event_args):
        self._button_node.addEventListener('click', self._handle_click)

    def _on_cleanup(self, **event_args):
        self._button_node.removeEventListener('click', self._handle_click)

    def _anvil_get_unset_property_values_(self):
        el = self.avatar.dom_nodes["anvil-m3-avatar"]
        m = get_unset_margin(el, self.margin)
        tfs = get_unset_value(
            self.avatar.dom_nodes['anvil-m3-avatar-initials'],
            "fontSize",
            self.avatar_font_size,
            )
        ifs = get_unset_value(
            self.avatar.dom_nodes['anvil-m3-avatar-icon'],
            "fontSize",
            self.fallback_icon_size,
            )
        return {"button_font_size": tfs, "icon_size": ifs, "margin": m}

    def _call_handle_keyboard_events(self, event):
        self._handle_keyboard_events(event)

    def _handle_click(self, event):
        if self.enabled:
            self._toggle_visibility()

    menu_background_color = color_property(
        'anvil-m3-avatarMenu-items-container', 'background', 'menu_background_color'
    )
    menu_border = border_property('anvil-m3-avatarMenu-items-container', 'menu_border')
    visible = HtmlTemplate.visible
    enabled = enabled_property('anvil-m3-avatarMenu-button')
  
    @anvil_prop
    @property
    def image(self, value) -> str:
        """The name of the avatar component"""
        self.avatar.image = value
    
    @anvil_prop
    @property
    def user_name(self, value) -> str:
        """The name of the avatar component"""
        self.avatar.user_name = value
    
    @anvil_prop
    @property
    def appearance(self, value) -> str:
        """A predefined style for the avatar."""
        self.avatar.appearance = value

    @anvil_prop
    @property
    def tooltip(self, value) -> str:
        """The text to display when the mouse is hovered over this component."""
        self.avatar.tooltip = value
    
    @anvil_prop
    @property
    def avatar_border(self, value) -> str:
        """The border of the avatar. Can take any valid CSS border value."""
        self.avatar.border = value
    
    @anvil_prop
    @property
    def avatar_background_color(self, value) -> str:
        """The colour of the background of the Button."""
        self.avatar.background_color = value

    @anvil_prop
    @property
    def avatar_text_color(self, value) -> str:
        """The colour of the text on the Button."""
        self.avatar.text_color = value
    
    @anvil_prop
    @property
    def avatar_font_size(self, value) -> int:
        """The font size of the text displayed on the Button."""
        self.avatar.font_size = value
    
    @anvil_prop
    @property
    def fallback_icon(self, value) -> str:
        """The icon to display on the Button."""
        self.avatar.fallback_icon = value

    @anvil_prop
    @property
    def fallback_icon_color(self, value) -> str:
        """The colour of the icon displayed on the Button."""
        self.avatar.fallback_icon_color = value
    
    @anvil_prop
    @property
    def fallback_icon_size(self, value) -> int:
        """The size (pixels) of the icon displayed on this component."""
        self.avatar.fallback_icon_size = value
    
    @anvil_prop
    @property
    def margin(self, value) -> list:
        """The margin (pixels) of the component."""
        self.avatar.margin = value

    @anvil_prop
    @property
    def align(self, value) -> str:
        self.dom_nodes['anvil-m3-avatarMenu-container'].style.justifyContent = value
        self._setup_fui()
    
    @anvil_prop
    @property
    def avatar_font_family(self, value) -> str:
        """The font family to use for the Button"""
        self.avatar.font_family = value

    @anvil_prop
    @property
    def role(self, value) -> str:
        """A style for this component defined in CSS and added to Roles"""
        self.avatar.role = value

    @anvil_prop
    @property
    def menu_items(self, value=[]) -> list:
        """A list of components to be added to the menu."""
        for i in value:
            self.add_component(i, slot='anvil-m3-avatarMenu-slot')


    def _anvil_get_interactions_(self):
        return [
            {
                "type": "designer_events",
                "callbacks": {
                "onSelectDescendent": self._on_select_descendent,
                "onSelectOther": self._on_select_other,
            },
            },
        ]

    def _on_select_descendent(self):
        self._toggle_visibility(value=True)
    
    def _on_select_other(self):
        self._toggle_visibility(value=False)

  #!componentProp(m3.AvatarMenu)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
  #!componentProp(m3.AvatarMenu)!1: {name:"appearance",type:"enum",options:["filled", "elevated", "tonal", "outlined", "text"],description:"A predefined style for this component."}
  #!componentProp(m3.AvatarMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.AvatarMenu)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.AvatarMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.AvatarMenu)!1: {name:"avatar_text_color",type:"color",description:"Color of the initials displayed on the Avatar if no image is provided"}
  #!componentProp(m3.AvatarMenu)!1: {name:"avatar_font_family",type:"string",description:"The font family to use for the initials on the Avatar"}
  #!componentProp(m3.AvatarMenu)!1: {name:"fallback_icon",type:"enum",description:"The icon to display on the Avatar if no image or user_name is provided."}
  #!componentProp(m3.AvatarMenu)!1: {name:"avatar_font_size",type:"number",description:"The font size of the initials displayed on the Avatar"}
  #!componentProp(m3.AvatarMenu)!1: {name:"fallback_icon_color",type:"color",description:"The color of the icon displayed on the Avatar"}
  #!componentProp(m3.AvatarMenu)!1: {name:"menu_background_color",type:"color",description:"The color of the menu."}
  #!componentProp(m3.AvatarMenu)!1: {name:"menu_border",type:"color",description:"The border of the menu. Can take any valid CSS border value."}
  #!componentProp(m3.AvatarMenu)!1: {name:"fallback_icon_size",type:"number",description:"The size (pixels) of the icon on the Avatar"}
  #!componentProp(m3.AvatarMenu)!1: {name:"avatar_background_color",type:"color",description:"Background color of the Avatar in this component if no image is provided"}
  #!componentProp(m3.AvatarMenu)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!componentProp(m3.AvatarMenu)!1: {name:"avatar_border",type:"string",description:"The border of the Avatar in this component. Can take any valid CSS border value."}
  #!componentProp(m3.AvatarMenu)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.AvatarMenu)!1: {name:"menu_items",type:"object",description:"A list of components to be added to the menu."}
  #!componentProp(m3.AvatarMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
  #!componentProp(m3.AvatarMenu)!1: {name:"image",type:"uri",description:"The image to display on the component."}
  #!componentProp(m3.AvatarMenu)!1: {name:"user_name",type:"string",description:"The name of the associated user. If no image is provided, the avatar will display initials generated from the user_name."}


  #!componentEvent(m3.AvatarMenu)!1: {name: "click", description: "When the Avatar is clicked.", parameters:[]}


#!defClass(m3, AvatarMenu, anvil.Component)!:


