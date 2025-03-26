from ..._utils import fui, noop


class MenuMixin():

    def _setup_fui(self, component_node, menu_node):
        if self._shown:
            self._cleanup()
            self._cleanup = fui.auto_update(
                component_node, menu_node, placement="bottom-start"
            )

    def _child_clicked(self, event, enabled):
        # do the click action. The child should handle this
        print(event)
        self._toggle_visibility(value=False)
        if enabled:
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
    
    def _toggle_visibility(self, component_node=None, menu_node=None, value=None):
        classes = menu_node.classList
        if value is not None:
            classes.toggle('anvil-m3-menuContainer-items-hidden', not value)
        else:
            classes.toggle('anvil-m3-menuContainer-items-hidden')

        self._open = not classes.contains('anvil-m3-menuContainer-items-hidden')
        if self._open and component_node and menu_node:
            self._setup_fui(component_node, menu_node)
            self._get_hover_index_information()
        else:
            self._cleanup()
            self._hoverIndex = None
            self._clear_hover_styles()
  
