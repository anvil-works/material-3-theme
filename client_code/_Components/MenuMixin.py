from .._utils import fui
from .MenuItem import MenuItem


class MenuMixin():
    def __init__(self, **properties):
        self._open = False
        self._hoverIndex = None
        self._children = None
        self._shown = False
        self._itemIndices = set()

    def _setup_fui(self, component_node, menu_node):
        if self._shown:
            self._cleanup()
            self._cleanup = fui.auto_update(
                component_node, menu_node, placement="bottom-start"
            )

    def _child_clicked(self, event, enabled):
        # do the click action. The child should handle this
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
            classes.toggle('anvil-m3-buttonMenu-items-hidden', not value)
        else:
            classes.toggle('anvil-m3-buttonMenu-items-hidden')

        self._open = not classes.contains('anvil-m3-buttonMenu-items-hidden')
        if self._open and component_node and menu_node:
            self._setup_fui(component_node, menu_node)
            self._get_hover_index_information()
        else:
            self._cleanup()
            self._hoverIndex = None
            self._clear_hover_styles()

    def _handle_keyboard_events(self, event, component_node, menu_node):
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
            self._hoverIndex
        )  # holding value for situations like alerts, where it awaits
        self._toggle_visibility(component_node=component_node, menu_node=menu_node, value=False)

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
            if self._hoverIndex is None or self._hoverIndex is (len(self._children) - 1):
                self._hoverIndex = -1
            while True:
                self._hoverIndex += 1
                if self._hoverIndex in self._itemIndices:
                    break
        else:
            if self._hoverIndex is None or self._hoverIndex == 0:
                self._hoverIndex = len(self._children)
            while True:
                self._hoverIndex -= 1
                if self._hoverIndex in self._itemIndices:
                    break
        self._children[self._hoverIndex].dom_nodes['anvil-m3-menuItem-container'].scrollIntoView({'block': 'nearest'})
        self._update_hover_styles()

    def _update_hover_styles(self):
        self._clear_hover_styles()
        self._children[self._hoverIndex].dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

    def _clear_hover_styles(self):
        if self._children is not None:
            for child in self._children:
                if isinstance(child, MenuItem):
                    child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', False)

    def _body_click(self, event, component_node, menu_node):
        if component_node.contains(event.target) or menu_node.contains(event.target):
            return
        self._toggle_visibility(component_node=component_node, menu_node=menu_node, value=False)
        
    def _get_hover_index_information(self):
        self._children = self.get_components()[:-1]
        for i in range(0, len(self._children)):
            if isinstance(self._children[i], MenuItem):
                self._itemIndices.add(i)
