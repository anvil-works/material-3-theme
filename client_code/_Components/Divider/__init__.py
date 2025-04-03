from anvil import *

from ..._utils.properties import (
    anvil_prop,
    color_property,
    get_unset_margin,
    margin_property,
    role_property,
)
from ._anvil_designer import DividerTemplate


class Divider(DividerTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-divider"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    #!componentEvent(m3.Divider)!1: {name: "show", description: "When the Divider is shown on the screen."}
    #!componentEvent(m3.Divider)!1: {name: "hide", description: "When the Divider is removed from the screen."}

    #!componentProp(m3.Divider)!1: {name:"type",type:"enum",options:["full_width", "inset"],description:"Display the Divider across the full width of the container or inset."}
    #!componentProp(m3.Divider)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Divider)!1: {name:"color",type:"color",description:"The colour of this component."}
    #!componentProp(m3.Divider)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.Divider)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}

    visible = HtmlTemplate.visible
    color = color_property('anvil-m3-divider', 'border-color', 'color')
    role = role_property('anvil-m3-divider')
    margin = margin_property('anvil-m3-divider')

    @anvil_prop
    @property
    def type(self, value) -> str:
        """Display the Divider across the full width of the container or inset."""
        divider = self.dom_nodes['anvil-m3-divider']
        value = value.lower().replace(' ', '-')
        divider.className = "anvil-m3-divider"
        self.dom_nodes['anvil-m3-divider'].classList.add(value)


#!defClass(m3, Divider, anvil.Component)!:
