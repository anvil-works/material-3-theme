from anvil.js.window import document

from .._utils import fui, noop
from .MenuItem import MenuItem


class MenuMixin():

    def __init__(self, component_node, menu_node):
        self._shown = False
        self._component_node = component_node
        self._menu_node = menu_node
        self._open = False
        self._cleanup = noop
        self._hover_index = None
        self._item_indices = set()
        self._children = None
        self.add_event_handler("x-page-added", self._menu_mixin_mount)
        self.add_event_handler("x-page-removed", self._menu_mixin_cleanup)

    def _menu_mixin_mount(self, **event_args):
        self._shown = True
        self._menu_node.addEventListener('click', self._handle_child_click)
        document.addEventListener('click', self._body_click)
        document.addEventListener('keydown', self._call_handle_keyboard_events)
        # We still have a reference to the dom node but we've moved it to the body
        # This gets around the fact that Anvil containers set their overflow to hidden
        
        self._setup_fui()

    def _menu_mixin_cleanup(self, **event_args):
        self._shown = False
        self._menu_node.removeEventListener('click', self._handle_child_click)
        document.removeEventListener('click', self._body_click)
        document.removeEventListener('keydown', self._call_handle_keyboard_events)
        # Remove the menu node we put on the body
        
        self._cleanup()
        
    def _setup_fui(self):
        if self._shown:
            self._cleanup()
            self._cleanup = fui.auto_update(
                self._component_node, self._menu_node, placement="bottom-start"
            )

    def _handle_child_click(self, event):
        # do the click action. The child should handle this
        self._child_click(event, self.enabled)

    def _child_click(self, event, enabled):
        # do the click action. The child should handle this
        self._toggle_visibility( value=False)
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
    
    def _toggle_visibility(self, value=None):
        classes = self._menu_node.classList
        if value is not None:
            classes.toggle('anvil-m3-buttonMenu-items-hidden', not value)
        else:
            classes.toggle('anvil-m3-buttonMenu-items-hidden')

        self._open = not classes.contains('anvil-m3-buttonMenu-items-hidden')
        if self._open:
            self._setup_fui()
            self._get_hover_index_information()
        else:
            self._cleanup()
            self._hover_index = None
            self._clear_hover_styles()

    def _handle_keyboard_events(self, event):
        if not self._open:
            return
        action_keys = set(["ArrowUp", "ArrowDown", "Tab", "Escape", " ", "Enter"])
        if event.key not in action_keys:
            return
        if event.key in ["ArrowUp", "ArrowDown"]:
            self._iterate_hover(event.key == "ArrowDown")
            event.preventDefault()
            return
        hover = (
            self._hover_index
        )  # holding value for situations like alerts, where it awaits
        self._toggle_visibility(value=False)

        def attemptSelect():
            event.preventDefault()
            if hover is not None:
                self._children[hover].raise_event(
                    "click",
                    event=event,
                    keys={
                        "shift": event.shiftKey,
                        "alt": event.altKey,
                        "ctrl": event.ctrlKey,
                        "meta": event.metaKey,
                    },
                    )
            if event.key == " ":  # " " indicates the space key
                attemptSelect()
            if event.key == "Enter":
                attemptSelect()

    def _iterate_hover(self, inc=True):
        if inc:
            if self._hover_index is None or self._hover_index is (len(self._children) - 1):
                self._hover_index = -1
            while True:
                self._hover_index += 1
                if self._hover_index in self._item_indices:
                    break
        else:
            if self._hover_index is None or self._hover_index == 0:
                self._hover_index = len(self._children)
            while True:
                self._hover_index -= 1
                if self._hover_index in self._item_indices:
                    break
        self._children[self._hover_index].dom_nodes['anvil-m3-menuItem-container'].scrollIntoView({'block': 'nearest'})
        self._update_hover_styles()

    def _update_hover_styles(self):
        self._clear_hover_styles()
        self._children[self._hover_index].dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

    def _clear_hover_styles(self):
        if self._children is not None:
            for child in self._children:
                if isinstance(child, MenuItem):
                    child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', False)

    def _body_click(self, event):
        if self._component_node.contains(event.target) or self._menu_node.contains(event.target):
            return
        self._toggle_visibility(value=False)
        
    def _get_hover_index_information(self):
        self._children = self.get_components()[:-1]
        for i in range(0, len(self._children)):
            if isinstance(self._children[i], MenuItem):
                self._item_indices.add(i)
