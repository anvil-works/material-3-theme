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
  get_unset_value,
  get_unset_margin,
)
)
from ..MenuMixin import MenuMixin
from ._anvil_designer import AvatarMenuTemplate


class AvatarMenu(AvatarMenuTemplate, MenuMixin):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._design_name = ""
        self._cleanup = noop
        self._menuNode = self.dom_nodes['anvil-m3-avatarMenu-items-container']
        self._buttonNode = self.dom_nodes['anvil-m3-avatarMenu-button']
        self._open = False
        self._hoverIndex = None
        self._itemIndices = set()
        self._children = None
        self._shown = False
    
        self.init_components(**properties)
    
        self.add_event_handler("x-anvil-page-added", self._on_mount)
        self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    def _on_mount(self, **event_args):
        self._shown = True
        document.addEventListener('keydown', self._call_handle_keyboard_events)
        self._menuNode.addEventListener('click', self._handle_child_clicked)
        self._buttonNode.addEventListener('click', self._handle_click)
        document.addEventListener('click', self._handle_body_click)
        # We still have a reference to the dom node but we've moved it to the body
        # This gets around the fact that Anvil containers set their overflow to hidden
        document.body.append(self._menuNode)
        super()._setup_fui(self._buttonNode, )

    def _on_cleanup(self, **event_args):
        self._shown = False
        document.removeEventListener('keydown', self._call_handle_keyboard_events)
        self._menuNode.removeEventListener('click', self._handle_child_clicked)
        document.removeEventListener('click', self._handle_body_click)
        self._cleanup()
        # Remove the menu node we put on the body
        self._menuNode.remove()

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

    def _handle_click(self, event):
        if self.enabled:
            super()._toggle_visibility()

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

    def _toggle_menu_visibility(self, **event_args):
        super()._toggle_visibility(component_node=self._buttonNode, menu_node=self._menuNode)

    def _handle_child_clicked(self, event):
        # do the click action. The child should handle this
        super()._child_clicked(self.enabled)

    def _handle_body_click(self, event):
        super()._body_click(event, self._buttonNode, self._menuNode)

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
        super()._toggle_visibility(component_node=self._buttonNode, menu_node=self._menuNode, value=True)
    
    def _on_select_other(self):
        super()._toggle_visibility(component_node=self._buttonNode, menu_node=self._menuNode, value=False)



