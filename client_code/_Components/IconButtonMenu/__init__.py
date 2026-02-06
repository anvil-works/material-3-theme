import anvil.designer
from anvil import *
from anvil.js import get_dom_node

from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    border_property,
    color_property,
    get_unset_margin,
)
from ..MenuMixin import MenuMixin
from ._anvil_designer import IconButtonMenuTemplate


class IconButtonMenu(MenuMixin, IconButtonMenuTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties

        self._menu_node = self.dom_nodes['anvil-m3-iconButtonMenu-items-container']
        self._btn_node = get_dom_node(self.icon_button).querySelector("button")
        self._btn_node.addEventListener('click', self._handle_click)

        MenuMixin.__init__(self, self._btn_node, self._menu_node)

        self.init_components(**properties)

    def focus(self):
        self.icon_button.focus()

    def _handle_click(self, event):
        if self.enabled:
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

    def _anvil_get_unset_property_values_(self):
        el = self.icon_button.dom_nodes["anvil-m3-iconbutton-container"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    def _toggle_menu_visibility(self, **event_args):
        """This method is called when the component is clicked."""
        self._toggle_visibility()

    visible = HtmlTemplate.visible
    menu_border = border_property('anvil-m3-iconButtonMenu-items-container', 'border')
    menu_background_color = color_property(
        'anvil-m3-iconButtonMenu-items-container', 'background', 'background_color'
    )

    @anvil_prop
    @property
    def appearance(self, value) -> str:
        """A predefined style for the IconButton."""
        self.icon_button.appearance = value

    @anvil_prop
    @property
    def tooltip(self, value) -> str:
        """The text to display when the mouse is hovered over this component."""
        self.icon_button.tooltip = value

    @anvil_prop
    @property
    def enabled(self, value) -> bool:
        """If True, this component allows user interaction."""
        self.icon_button.enabled = value

    @anvil_prop
    @property
    def button_border(self, value) -> str:
        """The border of the IconButton. Can take any valid CSS border value."""
        self.icon_button.border = value

    @anvil_prop
    @property
    def button_background_color(self, value) -> str:
        """The colour of the background of the IconButton."""
        self.icon_button.background_color = value

    @anvil_prop
    @property
    def icon(self, value) -> str:
        """The icon to display on the IconButton."""
        self.icon_button.icon = value

    @anvil_prop
    @property
    def icon_color(self, value) -> str:
        """The colour of the icon displayed on the IconButton."""
        self.icon_button.icon_color = value

    @anvil_prop
    @property
    def margin(self, value) -> list:
        """The margin and padding (pixels) of the component."""
        self.icon_button.margin = value

    @anvil_prop
    @property
    def align(self, value) -> str:
        self.icon_button.dom_nodes[
            'anvil-m3-iconbutton-component'
        ].style.justifyContent = value
        self.dom_nodes['anvil-m3-iconButtonMenu-container'].style.justifyContent = value
        self._setup_fui()

    @anvil_prop
    @property
    def role(self, value) -> str:
        """A style for this component defined in CSS and added to Roles"""
        self.icon_button.role = value

    @anvil_prop
    @property
    def menu_items(self, value=[]) -> list:
        """A list of components to be added to the menu."""
        for i in value:
            self.add_component(i, slot='anvil-m3-iconButtonMenu-slot')

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

    #!componentProp(m3.IconButtonMenu)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"appearance",type:"enum",options:["filled", "elevated", "tonal", "outlined", "text"],description:"A predefined style for the IconButton."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
    #!componentProp(m3.IconButtonMenu)!1: {name:"icon",type:"enum",description:"The icon to display on the IconButton."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"icon_color",type:"color",description:"The colour of the icon displayed on the IconButton."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"menu_background_color",type:"color",description:"The color of the background of the menu."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"menu_border",type:"color",description:"The border of the menu. Can take any valid CSS border value."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"button_background_color",type:"color",description:"The colour of the background of the IconButton."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"button_border",type:"string",description:"The border of the IconButton. Can take any valid CSS border value."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"menu_items",type:"object",description:"A list of components to be added to the menu."}
    #!componentProp(m3.IconButtonMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    #!componentEvent(m3.IconButtonMenu)!1: {name: "click", description: "When the IconButton is clicked.", parameters:[]}


#!defClass(m3, IconButtonMenu, anvil.Component)!:
