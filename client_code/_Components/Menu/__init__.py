from anvil import *
from anvil import HtmlTemplate

from ..._utils.properties import color_property
from ._anvil_designer import MenuTemplate


class Menu(MenuTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.tag = ComponentTag()
        self._props = properties
        self.init_components(**properties)

    """ Properties """
    visible = HtmlTemplate.visible
    background_color = color_property(
        'anvil-m3-menu-items-container', 'backgroundColor', 'background_color'
    )

    """ Functions """

    def set_or_toggle_visibility(self, value=None):
        if value is not None:
            self.visible = value
        else:
            currVal = self.visible
            self.visible = not currVal

    def _anvil_get_interactions_(self):
        return [
            {
                "type": "designer_events",
                "callbacks": {
                    "onSelectDescendent": self._on_select_descendant,
                    "onSelectOther": self._on_select_other,
                },
            },
        ]

    def _on_select_descendant(self):
        pass

    def _on_select_other(self):
        pass
