import anvil
import anvil.designer
import anvil.server
from anvil.js import get_dom_node
from anvil.js.window import document

from ..._utils import fui, noop
from ..._utils.properties import (
  anvil_prop,
  get_unset_margin,
  get_unset_value,
  inline_editing,
  margin_property,
)
from ..MenuItem import MenuItem
from ._anvil_designer import DropdownMenuTemplate


class DropdownMenu(DropdownMenuTemplate):
  def __init__(self, **properties):
    self._init = False
    self.tag = anvil.ComponentTag()
    self._props = properties
    self._clean_items = []
    self._children = []
    self._hoverIndex = None
    self.selected_value = None
    self._set_designer_text_placeholder, self._start_inline_editing = inline_editing(
      self,
      self.selection_field.dom_nodes['anvil-m3-label-text'],
      self._set_label,
      "label",
    )
    self._cleanup = noop
    self._has_focus = False
    self._menuNode = self.dom_nodes['anvil-m3-dropdownMenu-items-container']
    self._field = self.selection_field.dom_nodes['anvil-m3-textbox']

    self.init_components(**properties)

    if not self.allow_none:
      self.selection_field.text = ""

    self.dom_nodes['anvil-m3-dropdownMenu-container'].addEventListener(
      'click', self._handle_component_click
    )
    self.selection_field.dom_nodes['anvil-m3-textbox'].addEventListener(
      'focus', self._handle_selection_field_focus
    )
    self.selection_field.dom_nodes['anvil-m3-textbox'].addEventListener(
      'blur', self._handle_selection_field_blur
    )

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    self.selection_field.dom_nodes['anvil-m3-textbox'].style.caretColor = 'transparent'
    self.selection_field.dom_nodes['anvil-m3-textbox'].style.cursor = "pointer"
    self.selection_field.dom_nodes['anvil-m3-textbox'].setAttribute("readonly", True)

    if anvil.designer.in_designer:
      self._menuNode.classList.toggle("anvil-m3-menu-hidden", True)

    self._init = True
    self._create_menu_items()

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes['anvil-m3-dropdownMenu-textbox']
    m = get_unset_margin(el, self.margin)
    lfs = get_unset_value(
      self.selection_field.dom_nodes['anvil-m3-label-text'],
      "fontSize",
      self.label_font_size,
    )
    stfs = get_unset_value(
      self.selection_field.dom_nodes['anvil-m3-supporting-text'],
      "fontSize",
      self.supporting_text_font_size,
    )
    sfs = get_unset_value(
      self.selection_field.dom_nodes['anvil-m3-textbox'],
      "fontSize",
      self.selected_font_size,
    )
    return {
      "label_font_size": lfs,
      "supporting_text_font_size": stfs,
      "selected_font_size": sfs,
      "margin": m,
    }

  def _on_mount(self, **event_args):
    document.addEventListener('keydown', self._handle_keyboard_events)
    document.addEventListener('click', self._body_click)
    document.body.append(self._menuNode)
    self._cleanup = fui.auto_update(
      self._field, self._menuNode, placement="bottom-start", offset=0
    )
    self._menuNode.addEventListener('click', self._child_clicked)

  def _on_cleanup(self, **event_args):
    document.removeEventListener('keydown', self._handle_keyboard_events)
    document.removeEventListener('click', self._body_click)
    self._menuNode.removeEventListener('click', self._child_clicked)
    self._cleanup()
    self._menuNode.remove()

  def _handle_selection_field_focus(self, event):
    self._has_focus = True

  def _handle_selection_field_blur(self, event):
    self._has_focus = False

  def _handle_keyboard_events(self, event):
    if not self._has_focus:
      return
    else:
      action_keys = set(["ArrowUp", "ArrowDown", "Tab", "Escape", " ", "Enter"])
      open_keys = set(["ArrowUp", "ArrowDown", " ", "Enter"])
      if not self.menu.visible:
        if event.key in open_keys:
          self._set_menu_visibility(True)
          event.preventDefault()
        return

      if event.key not in action_keys:
        return

      if event.key == "ArrowUp" or event.key == "ArrowDown":
        event.preventDefault()
        self._iterate_hover(event.key == "ArrowDown")
        return

      if event.key in ["Tab", "Escape"]:
        self._set_menu_visibility(False)

      if event.key == " ":
        event.preventDefault()
        self._attempt_select(event)
      if event.key == "Enter":
        self._attempt_select(event)

  def _iterate_hover(self, inc=True):
    if inc:
      if self._hoverIndex is None or self._hoverIndex is (len(self._children) - 1):
        self._hoverIndex = -1
      self._hoverIndex += 1
    else:
      if self._hoverIndex is None or self._hoverIndex == 0:
        self._hoverIndex = len(self._children)
      self._hoverIndex -= 1
    self._children[self._hoverIndex].dom_nodes[
      'anvil-m3-menuItem-container'
    ].scrollIntoView({'block': 'nearest'})
    self._update_hover_styles()

  def _attempt_select(self, event):
    if self._hoverIndex is not None:
      self._children[self._hoverIndex].raise_event(
        "click",
        event=event,
        keys={
          "shift": event.shiftKey,
          "alt": event.altKey,
          "ctrl": event.ctrlKey,
          "meta": event.metaKey,
        },
      )
    self._set_menu_visibility(False)

  def _clear_hover_styles(self):
    if self._children is not None:
      for child in self._children:
        child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle(
          'anvil-m3-menuItem-container-keyboardHover', False
        )

  def _update_hover_styles(self):
    self._clear_hover_styles()
    if self._hoverIndex is None:
      return
    self._children[self._hoverIndex].dom_nodes[
      'anvil-m3-menuItem-container'
    ].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

  def _handle_component_click(self, event):
    self._set_menu_visibility()

  def _set_menu_visibility(self, value=None):
    if value is None:
      value = not self.menu.visible
    if self.read_only:
        value = False

    self.menu.visible = value
    self._menuNode.classList.toggle("anvil-m3-menu-hidden", not value)

    if value:
      selection_field_width = get_dom_node(self.selection_field).offsetWidth
      self._menuNode.style.width = f"{selection_field_width}px"

      # dealing with hover
      selected_value = self.selected_value
      for index, child in enumerate(self._children):
        if child.tag.value == selected_value:
          self._hoverIndex = index
          break
      else:  # no break
        self._hoverIndex = None

      self._update_hover_styles()

      if not anvil.designer.in_designer:
        self.selection_field.trailing_icon = "mi:arrow_drop_up"
        if self._hoverIndex:
          self._children[self._hoverIndex].dom_nodes[
            'anvil-m3-menuItem-container'
          ].scrollIntoView({'block': 'nearest'})

    else:
      self.selection_field.trailing_icon = "" if self.read_only else "mi:arrow_drop_down"
      if self.selected_value is None:
        self._hoverIndex = None

  def _body_click(self, event):
    icon = self.selection_field.dom_nodes['anvil-m3-icon-container']
    if (
      self._field.contains(event.target)
      or self._menuNode.contains(event.target)
      or icon.contains(event.target)
    ):
      self.selection_field.focus()
    else:
        self._set_menu_visibility(False)

  def _child_clicked(self, event):
    event.stopPropagation()
    self._set_menu_visibility(False)

  def form_show(self, **event_args):
    self._set_designer_text_placeholder()

  def _create_menu_items(self):
    self.menu.clear()
    item_props = {
      "hide_leading_icon": True,
      "bold": self.items_bold,
      "italic": self.items_italic,
      "underline": self.items_underline,
      "text_color": self.items_text_color,
      "font_family": self.items_font_family,
      "font_size": self.items_font_size,
    }

    p = MenuItem(**item_props, text=self.placeholder or "")
    p.tag.value = None
    p.tag.label = ""

    def _handle_select_placeholder(**e):
      if self.allow_none:
        self.selected_value = None
      self.raise_event("change")

    if not self.allow_none:
      p.enabled = False

    self._children = []

    if self.allow_none or self.placeholder:
      p.add_event_handler('click', _handle_select_placeholder)
      self.menu.add_component(p, slot="anvil-m3-menu-slot")
      self._children.append(p)

    for label, value in self._clean_items:
      selection = MenuItem(**item_props, text=label)
      selection.tag.value = value
      selection.tag.label = label

      def _handle_selection_click(value=value, **e):
        self.selected_value = value
        self.raise_event("change")

      selection.add_event_handler('click', _handle_selection_click)
      self.menu.add_component(selection, slot="anvil-m3-menu-slot")
      self._children.append(selection)

    self.selected_value = self.selected_value

  # DESIGNER INTERACTIONS
  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit Label",
        "icon": "edit",
        "default": True,
        "callbacks": {"execute": self._start_inline_editing},
      }
    ]

  # properties
  visible = anvil.HtmlTemplate.visible
  margin = margin_property('anvil-m3-dropdownMenu-textbox')

  @anvil_prop
  @property
  def allow_none(self, value) -> bool:
    """If True, a placeholder item is added to the menu with value None"""
    self._recreate_items()

  @anvil_prop
  @property
  def background_color(self, value) -> str:
    """The colour of the background of this component."""
    self.selection_field.background_color = value

  @anvil_prop
  @property
  def label_bold(self, value) -> bool:
    """If True, the label text will be bold."""
    self.selection_field.label_bold = value

  @anvil_prop
  @property
  def label_font(self, value) -> str:
    """The label text of the component."""
    self.selection_field.label_font = value

  @anvil_prop
  @property
  def label_font_size(self, value) -> float:
    """The font size of the label text on this component."""
    self.selection_field.label_font_size = value

  @anvil_prop
  @property
  def label_color(self, value) -> str:
    """The colour of the label text on the component."""
    self.selection_field.label_color = value

  @anvil_prop
  @property
  def label_italic(self, value) -> bool:
    """If True, the label text will be italic."""
    self.selection_field.label_italic = value

  @anvil_prop
  @property
  def label_underline(self, value) -> bool:
    """If True, the label text will be underlined."""
    self.selection_field.label_underline = value

  @anvil_prop
  @property
  def enabled(self, value) -> bool:
    """If True, this component allows user interaction."""
    self.selection_field.enabled = value

  @anvil_prop
  @property
  def read_only(self, value) -> bool:
    """If True, this component won't allow it's value to be changed."""
    self.selection_field.read_only = value
    self._set_menu_visibility(False)

  @anvil_prop
  @property
  def appearance(self, value) -> str:
    """A predefined style for this component."""
    self.selection_field.appearance = value

  @anvil_prop
  @property
  def align(self, value) -> str:
    """The position of this component in the available space."""
    self.selection_field.align = value

  @anvil_prop
  @property
  def role(self, value) -> str:
    """A style for this component defined in CSS and added to Roles"""
    self.selection_field.role = value

  @anvil_prop
  @property
  def selected_italic(self, value) -> bool:
    """If True and there is a selected item, the displayed text in italic."""
    self.selection_field.display_italic = value

  @anvil_prop
  @property
  def selected_bold(self, value) -> bool:
    """If True and there is a selected item, the displayed text is bold."""
    self.selection_field.display_bold = value

  @anvil_prop
  @property
  def selected_underline(self, value) -> bool:
    """If True and there is a selected item, the displayed text is underlined"""
    self.selection_field.display_underline = value

  @anvil_prop
  @property
  def selected_font(self, value):
    self.selection_field.selected_font = value

  @anvil_prop
  @property
  def selected_font_size(self, value) -> int:
    """The font size (pixels) of the displayed text if there is a selected item."""
    self.selection_field.selected_font_size = value

  @anvil_prop
  @property
  def selected_text_color(self, value) -> str:
    """The colour of the displayed text if there is a selected item."""
    self.selection_field.selected_text_color = value

  @anvil_prop
  @property
  def icon(self, value) -> str:
    self.selection_field.leading_icon = value

  @anvil_prop
  @property
  def icon_color(self, value) -> str:
    self.selection_field.leading_icon_color = value

  @anvil_prop
  @property
  def tooltip(self, value) -> str:
    """The text to display when the mouse is hovered over this component."""
    self.selection_field.tooltip = value

  @anvil_prop
  @property
  def supporting_text(self, value) -> str:
    """The supporting text displayed below this component"""
    self.selection_field.supporting_text = value

  @anvil_prop
  @property
  def supporting_text_color(self, value) -> str:
    """The colour of the supporting text below this component."""
    self.selection_field.subcontent_color = value

  @anvil_prop
  @property
  def supporting_text_font_family(self, value) -> str:
    """The font family to use for the supporting text below this component."""
    self.selection_field.subcontent_font_family = value

  @anvil_prop
  @property
  def supporting_text_font_size(self, value) -> str:
    """The font size of the supporting text displayed below this component."""
    self.selection_field.subcontent_font_size = value

  @anvil_prop
  @property
  def border_color(self, value) -> str:
    """The colour of the border of this component."""
    self.selection_field.border_color = value

  @anvil_prop
  @property
  def menu_background_color(self, value) -> str:
    """The background color of the menu."""
    self.menu.background_color = value

  @anvil_prop
  @property
  def error(self, value) -> bool:
    """If True, this component is in an error state."""
    if value:
      self.dom_nodes['anvil-m3-dropdownMenu-textbox'].classList.add(
        'anvil-m3-dropdown-error'
      )
    else:
      self.dom_nodes['anvil-m3-dropdownMenu-textbox'].classList.remove(
        'anvil-m3-dropdown-error'
      )

  def _set_label(self, value):
    self.selection_field.label = value

  @anvil_prop
  @property
  def label(self, value) -> str:
    """The label text of the component."""
    self._set_label(value)
    self._set_designer_text_placeholder()

  @anvil_prop
  @property
  def selected_value(self, value):
    """The value of the currently selected item. Can only be set at runtime."""
    if anvil.designer.in_designer:
      return

    for child in self._children:
      if child.tag.value == value:
        self.selection_field.text = child.tag.label
        break
    else:  # no break
      if value is not None:
        self.selection_field.text = "<Invalid value>"
      else:
        self.selection_field.text = ""

  @anvil_prop
  @property
  def placeholder(self, value) -> str:
    """The text to be displayed when the component is empty"""
    self.selection_field.placeholder = value
    self._recreate_items()

  def _recreate_items(self):
    if self._init:
      self._create_menu_items()

  @anvil_prop
  @property
  def items(self, value):
    items = value
    clean_items = self._clean_items = []
    for i, item in enumerate(items):
      if isinstance(item, str):
        clean_items.append((item, item))
      elif not isinstance(item, (tuple, list)):
        raise TypeError("DropdownMenu items must be a list of strings or tuples")
      else:
        label, value = item
        if not isinstance(label, str):
          raise TypeError(
            "Dropdown item tuples must be of the form ('label', value),"
            f" (at item ${i} got {item!r})"
          )

        clean_items.append((label, value))

    self._recreate_items()

  @anvil_prop
  @property
  def items_italic(self, value) -> bool:
    """If True, the menu items will be italic."""
    self._recreate_items()

  @anvil_prop
  @property
  def items_underline(self, value) -> bool:
    """If True, the menu items will be underlined."""
    self._recreate_items()

  @anvil_prop
  @property
  def items_text_color(self, value) -> str:
    """The colour of the menu items' text."""
    self._recreate_items()

  @anvil_prop
  @property
  def items_bold(self, value) -> bool:
    """If True, the menu items will be bold."""
    self._recreate_items()

  @anvil_prop
  @property
  def items_font_family(self, value) -> str:
    """The font family to use for the menu items."""
    self._recreate_items()

  @anvil_prop
  @property
  def items_font_size(self, value) -> int:
    """The font size of the menu items."""
    self._recreate_items()

  #!componentProp(m3.DropdownMenu)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
  #!componentProp(m3.DropdownMenu)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"A predefined style for this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.DropdownMenu)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.DropdownMenu)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
  #!componentProp(m3.DropdownMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}

  #!componentProp(m3.DropdownMenu)!1: {name:"label_color",type:"color",description:"The colour of the label text on the component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label",type:"string",description:"The label text of the component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
  #!componentProp(m3.DropdownMenu)!1: {name:"label_bold",type:"boolean",description:"If True, the label text will be bold."}

  #!componentProp(m3.DropdownMenu)!1: {name:"items_text_color",type:"color",description:"The colour of the menu items' text."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items_font_family",type:"string",description:"The font family to use for the menu items."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items_font_size",type:"number",description:"The font size of the menu items."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items_underline",type:"boolean",description:"If True, the menu items will be underlined."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items_italic",type:"boolean",description:"If True, the menu items will be italic."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items_bold",type:"boolean",description:"If True, the menu items will be bold."}
  #!componentProp(m3.DropdownMenu)!1: {name:"menu_background_color",type:"color",description:"The background color of the menu."}

  #!componentProp(m3.DropdownMenu)!1: {name:"selected_text_color",type:"color",description:"The colour of the displayed text if there is a selected item."}
  #!componentProp(m3.DropdownMenu)!1: {name:"selected_font_size",type:"number",description:"The font size (pixels) of the displayed text if there is a selected item."}
  #!componentProp(m3.DropdownMenu)!1: {name:"selected_font_family",type:"string",description:"The font-family of the displayed text if there is a selected item."}

  #!componentProp(m3.DropdownMenu)!1: {name:"selected_underline",type:"boolean",description:"If True and there is a selected item, the displayed text is underlined"}
  #!componentProp(m3.DropdownMenu)!1: {name:"selected_italic",type:"boolean",description:"If True and there is a selected item, the displayed text in italic."}
  #!componentProp(m3.DropdownMenu)!1: {name:"selected_bold",type:"boolean",description:"If True and there is a selected item, the displayed text is bold."}

  #!componentProp(m3.DropdownMenu)!1: {name:"leading_icon",type:"enum",description:"The leading icon to display on this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"leading_icon_color",type:"color",description:"The colour of the leading icon displayed on this component."}

  #!componentProp(m3.DropdownMenu)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed below this component"}
  #!componentProp(m3.DropdownMenu)!1: {name:"supporting_text_color",type:"color",description:"The colour of the supporting text below this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"supporting_text_font_family",type:"color",description:"The font family to use for the supporting text below this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"supporting_text_font_size",type:"color",description:"The font size of the supporting text displayed below this component."}

  #!componentProp(m3.DropdownMenu)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"placeholder",type:"string",description:"The text to be displayed when the component is empty"}
  #!componentProp(m3.DropdownMenu)!1: {name:"allow_none",type:"boolean",description:"If True, a placeholder item is added to the menu with value None"}
  #!componentProp(m3.DropdownMenu)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"items",type:"string list",description:"The items to display in the menu."}
  #!componentProp(m3.DropdownMenu)!1: {name:"selected_value",type:"object",description:"The value of the currently selected item. Can only be set at runtime."}
  #!componentProp(m3.DropdownMenu)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
  #!componentProp(m3.DropdownMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(m3.DropdownMenu)!1: {name: "change", description: "When an item is selected.", parameters:[]}


#!defClass(m3,DropdownMenu, anvil.Component)!:
