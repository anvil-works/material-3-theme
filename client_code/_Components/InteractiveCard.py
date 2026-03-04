from .._utils.properties import anvil_prop
from .Card import Card
from .._utils.properties import anvil_prop
import anvil

enabled_property = {
    "name": "enabled",
    "type": "boolean",
    # "default_value": True,
    "important": True,
    "designerHint": "enabled",
    "group": "Interaction",
    "description": "If True, this component allows user interaction.",
}
click_event = {
    "name": "click",
    "defaultEvent": True,
    "description": "When the component is clicked",
}


class InteractiveCard(Card):
    _anvil_properties_ = [enabled_property, *Card._anvil_properties_]
    _anvil_events_ = [click_event, *Card._anvil_events_]

    def __init__(self, **properties):
        super().__init__(**properties)
        self.init_components(**properties)
        # Module component props don't get their default values initialized by default. This makes sure the enabled setter has run.
        self.enabled = self.enabled
        self.dom_nodes['anvil-m3-card'].classList.toggle('anvil-m3-interactive', True)
        self.dom_nodes['anvil-m3-card'].addEventListener("click", self._handle_click)
        self.dom_nodes['anvil-m3-card'].addEventListener(
            "keydown",
            lambda event: (
                event.key in ("Enter", " ")
                and (event.preventDefault() or True)
                and self._handle_click(event)
            ),
        )

    def focus(self):
        self.dom_nodes['anvil-m3-card'].focus()

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, this component allows user interaction."""
        self.dom_nodes['anvil-m3-card'].classList.toggle('anvil-m3-disabled', not value)
        self.dom_nodes['anvil-m3-card'].tabIndex = 0 if value else -1

    def _handle_click(self, event):
        event.preventDefault()
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
            return True

    #!componentProp(m3.InteractiveCard)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.InteractiveCard)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
    #!componentProp(m3.InteractiveCard)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
    #!componentProp(m3.InteractiveCard)!1: {name:"align",type:"enum",description:"The position of this component in the available space."}
    #!componentProp(m3.InteractiveCard)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
    #!componentProp(m3.InteractiveCard)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.InteractiveCard)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
    #!componentProp(m3.InteractiveCard)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}
    #!componentProp(m3.InteractiveCard)!1: {name:"appearance",type:"enum",options:["elevated", "filled", "outlined"],description:"A predefined style for this component."}
    #!componentProp(m3.InteractiveCard)!1: {name:"orientation",type:"enum",options:["column", "row"],description:"The orientation of the content in this Card"}
    #!componentProp(m3.InteractiveCard)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}

    #!componentEvent(m3.InteractiveCard)!1: {name: "click", description: "When the component is clicked.", parameters:[]}


#!defClass(m3,InteractiveCard, anvil.Component)!:
