from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import (
    anvil_prop,
    get_unset_margin,
    margin_property,
    role_property,
    theme_color_to_css,
    tooltip_property,
)
from ._anvil_designer import LinearProgressIndicatorTemplate


class LinearProgressIndicator(LinearProgressIndicatorTemplate):
    def __init__(self, **properties):
        self._tooltip_node = None
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-progressindicator-linear"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    visible = HtmlTemplate.visible
    tooltip = tooltip_property('anvil-m3-progressindicator-linear')
    role = role_property('anvil-m3-progressindicator-linear')
    margin = margin_property('anvil-m3-progressindicator-linear')

    @anvil_prop
    @property
    def progress_color(self, value) -> str:
        """The colour of the progress bar"""
        if value:
            value = theme_color_to_css(value)
        self.dom_nodes['anvil-m3-progressindicator-indicator'].style['stroke'] = value
        self.dom_nodes['anvil-m3-progressindicator-indicator-indeterminate'].style[
            'stroke'
        ] = value
        self.dom_nodes['anvil-m3-progressindicator-indicator-indeterminate-2'].style[
            'stroke'
        ] = value

    @anvil_prop
    @property
    def track_color(self, value) -> str:
        """The colour of the LinearProgressIndicator track."""
        if value:
            value = theme_color_to_css(value)
        self.dom_nodes[
            'anvil-m3-progressindicator-indeterminate'
        ].style.backgroundColor = value
        self.dom_nodes[
            'anvil-m3-progressindicator-determinate'
        ].style.backgroundColor = value

    @anvil_prop
    @property
    def type(self, value) -> str:
        """Display a determinate or indeterminate progress indicator. Use determinate to set the progress with the progress property. Use indeterminate to express an unspecified amount of wait time."""
        v = value == "determinate"
        self.dom_nodes['anvil-m3-progressindicator-indeterminate'].classList.toggle(
            'anvil-m3-progressindicator-hidden', v
        )
        self.dom_nodes['anvil-m3-progressindicator-determinate'].classList.toggle(
            'anvil-m3-progressindicator-hidden', not v
        )

    @anvil_prop
    @property
    def progress(self, value) -> float:
        """The progress of the LinearProgressIndicator."""
        v = max(min(value or 0, 100), 0)
        self.dom_nodes['anvil-m3-progressindicator-indicator'].setAttribute(
            "x2", f"{v}%"
        )

    #!componentProp(m3.LinearProgressIndicator)!1: {name:"progress_color",type:"color",description:"The colour of the progress bar"}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"progress",type:"number",description:"The progress of the LinearProgressIndicator."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"track_color",type:"color",description:"The colour of the LinearProgressIndicator track."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
    #!componentProp(m3.LinearProgressIndicator)!1: {name:"type",type:"enum",options:["determinate", "indeterminate"],description:"Display a determinate or indeterminate progress indicator. Use determinate to set the progress with the progress property. Use indeterminate to express an unspecified amount of wait time."}


#!defClass(m3,LinearProgressIndicator,anvil.Component)!:
