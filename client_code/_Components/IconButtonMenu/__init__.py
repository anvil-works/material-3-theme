from ..MenuMixin import MenuMixin
from ._anvil_designer import IconButtonMenuTemplate
from anvil import *
    
    
class IconButtonMenu(MenuMixin, IconButtonMenuTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties

        self._menu_node = self.dom_nodes['anvil-m3-iconButtonMenu-items-container']
        self._btn_node = get_dom_node(self.icon_button).querySelector("button")
        self._btn_node.addEventListener('click', self._handle_click)

        MenuMixin.__init__(self, self._btn_node, self._menu_node)

        self.init_components(**properties)
    
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
    
    def _toggle_menu_visibility(self, **event_args):
        """This method is called when the component is clicked."""
        self._toggle_visibility()