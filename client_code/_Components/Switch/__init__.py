import anvil.designer
import anvil.server
from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import (
    anvil_prop,
    enabled_property,
    get_unset_margin,
    margin_property,
    property_with_callback,
    role_property,
    style_property,
    theme_color_to_css,
    tooltip_property,
)
from ._anvil_designer import SwitchTemplate


class Switch(SwitchTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.tag = ComponentTag()
        self._tooltip_node = None
        self._props = properties
        self.init_components(**properties)
        self.dom_nodes['anvil-m3-switch-input'].addEventListener(
            "change", self._handle_change
        )

    def focus(self):
        self.dom_nodes['anvil-m3-switch-input'].focus()

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-switch-container"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    def _anvil_get_interactions_(self):
        return [
            {
                "type": "region",
                "bounds": self.dom_nodes['anvil-m3-switch-container'],
                "sensitivity": 0,
                "callbacks": {"execute": self._toggle_selected},
            }
        ]

    def _toggle_selected(self):
        self.selected = not self.selected
        anvil.designer.update_component_properties(self, {'selected': self.selected})

    def _handle_change(self, event):
        if self.enabled:
            self.selected = not self.selected
            self.raise_event("change")

    def _set_color_styles(self, value=None):
        if self.selected:
            self.dom_nodes['anvil-m3-switch-slider'].style.backgroundColor = (
                theme_color_to_css(self.selected_background_color)
                if self.selected_background_color
                else None
            )
            if self.selected_thumb_color:
                self.dom_nodes['anvil-m3-switch-slider'].style.setProperty(
                    '--anvil-m3-selected-thumb-color',
                    theme_color_to_css(self.selected_thumb_color),
                )
            else:
                self.dom_nodes['anvil-m3-switch-slider'].style.setProperty(
                    '--anvil-m3-selected-thumb-color', 'var(--anvil-m3-on-primary)'
                )
        else:
            self.dom_nodes['anvil-m3-switch-slider'].style.backgroundColor = (
                theme_color_to_css(self.unselected_background_color)
                if self.unselected_background_color
                else None
            )
            self.dom_nodes['anvil-m3-switch-slider'].style.borderColor = (
                theme_color_to_css(self.unselected_outline_color)
                if self.unselected_outline_color
                else None
            )
            if self.unselected_thumb_color:
                self.dom_nodes['anvil-m3-switch-slider'].style.setProperty(
                    '--anvil-m3-unselected-thumb-color',
                    theme_color_to_css(self.unselected_thumb_color),
                )
            else:
                self.dom_nodes['anvil-m3-switch-slider'].style.setProperty(
                    '--anvil-m3-unselected-thumb-color', 'var(--anvil-m3-outline)'
                )

    #!componentEvent(m3.Switch)!1: {name: "change", description: "When the state of the Switch is changed."}
    #!componentEvent(m3.Switch)!1: {name: "show", description: "When the Switch is shown on the screen."}
    #!componentEvent(m3.Switch)!1: {name: "hide", description: "When the Switch is removed from the screen."}

    #!componentProp(m3.Switch)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.Switch)!1: {name:"align",type:"enum", options:["left", "center", "right"],description:"The position of this component in the available space."}
    #!componentProp(m3.Switch)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Switch)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.Switch)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.Switch)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.Switch)!1: {name:"selected_background_color",type:"color",description:"The background colour of the component when toggled on."}
    #!componentProp(m3.Switch)!1: {name:"unselected_background_color",type:"color",description:"The background colour of the component when toggled off."}
    #!componentProp(m3.Switch)!1: {name:"selected_thumb_color",type:"color",description:"The colour of the Switch thumb when toggled on."}
    #!componentProp(m3.Switch)!1: {name:"unselected_thumb_color",type:"color",description:"The colour of the Switch thumb when toggled off."}
    #!componentProp(m3.Switch)!1: {name:"unselected_outline_color",type:"color",description:"The colour of the outline of the Switch when toggled off."}
    #!componentProp(m3.Switch)!1: {name:"selected_icon",type:"enum",description:"Optional icon to appear on the Switch when toggled on."}
    #!componentProp(m3.Switch)!1: {name:"unselected_icon",type:"enum",description:"Optional icon to appear on the Switch when toggled off."}
    #!componentProp(m3.Switch)!1: {name:"selected",type:"boolean",description:"If True, this component is toggled on."}
    #!componentProp(m3.Switch)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    enabled = enabled_property('anvil-m3-switch-input')
    align = style_property('anvil-m3-switch-container', 'justifyContent', 'align')
    visible = HtmlTemplate.visible
    margin = margin_property('anvil-m3-switch-container')
    tooltip = tooltip_property('anvil-m3-switch')
    role = role_property('anvil-m3-switch')
    selected_background_color = property_with_callback(
        'selected_background_color', _set_color_styles
    )
    unselected_background_color = property_with_callback(
        'unselected_background_color', _set_color_styles
    )
    selected_thumb_color = property_with_callback(
        'selected_thumb_color', _set_color_styles
    )
    unselected_thumb_color = property_with_callback(
        'unselected_thumb_color', _set_color_styles
    )
    unselected_outline_color = property_with_callback(
        'unselected_outline_color', _set_color_styles
    )

    @anvil_prop
    @property
    def selected_icon(self, value) -> str:
        """Optional icon to appear on the Switch when toggled on."""
        link_icon = self.dom_nodes['anvil-m3-enabled-switch-icon']
        switch_slider = self.dom_nodes['anvil-m3-switch-slider']
        link_icon.classList.remove("material-symbols-outlined")
        link_icon.innerText = value[3:]
        if value:
            link_icon.classList.add("material-symbols-outlined")
            switch_slider.classList.add('anvil-m3-has-enabled-icon')

    @anvil_prop
    @property
    def unselected_icon(self, value) -> str:
        """Optional icon to appear on the Switch when toggled off."""
        link_icon = self.dom_nodes['anvil-m3-disabled-switch-icon']
        switch_slider = self.dom_nodes['anvil-m3-switch-slider']
        link_icon.innerText = value[3:]
        link_icon.classList.remove("material-symbols-outlined")
        if value:
            link_icon.classList.add("material-symbols-outlined")
            switch_slider.classList.add('anvil-m3-has-disabled-icon')

    @anvil_prop
    @property
    def selected(self, value) -> bool:
        """If True, this component is toggled on."""
        self.dom_nodes['anvil-m3-switch-input'].checked = value
        self._set_color_styles()


#!defClass(m3, Switch, anvil.Component)!:
