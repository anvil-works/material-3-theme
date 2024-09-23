from ._anvil_designer import DropdownMenuTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import HtmlTemplate
from ...Functions import property_with_callback, property_without_callback, margin_property, color_property
from anvil.js import window, get_dom_node
from anvil.js.window import document
import random, string, math
import anvil.designer
from ..MenuItem import MenuItem
from ...utils import fui, noop


class DropdownMenu(DropdownMenuTemplate):
  def __init__(self, **properties):
    self._props = properties
    self._design_name = ""
    self.init_components(**properties)
        
    self._cleanup = noop

    self._menuNode = self.dom_nodes['anvil-m3-dropdownMenu-items-container']
    self._field = get_dom_node(self.selection_field).querySelector("input")

    self._hoverIndex = None
    self._children = None

    self.selected_value = None
    
    if not self.allow_none:
      self.selection_field.dom_nodes['anvil-m3-textfield'].value = ""

    self._has_focus = False
    self._handle_keyboard_events = self._handle_keyboard_events
    self._handle_selection_field_focus = self._handle_selection_field_focus
    self._child_clicked = self._child_clicked
    self._body_click = self._body_click
    self._handle_component_click = self._handle_component_click

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    self.selection_field.dom_nodes['anvil-m3-textfield'].style.caretColor = 'transparent'
    self.selection_field.dom_nodes['anvil-m3-textfield'].style.cursor = "pointer"
    self.selection_field.dom_nodes['anvil-m3-textfield'].setAttribute("readonly", True)

    # if self.placeholder: #when no label, in unfocused state, use the placeholder as the display text.
    #   self.selection_field.dom_nodes['anvil-m3-label-text'].innerText = self.placeholder

    if anvil.designer.in_designer: #hides so doesn't do the ghosty visible thing when in designer cuz i want it to just straight up not show cuz its nto like you can add stuffin anyways.
      self._menuNode.classList.toggle("anvil-m3-menu-hidden", True)

  #properties
  visible = HtmlTemplate.visible
  margin = margin_property('anvil-m3-dropdownMenu-textfield')

  def _set_background_color(self, value):
    self.selection_field.background_color = value
  background_color = property_with_callback("background_color", _set_background_color)

  def _set_label_bold(self, value):
    self.selection_field.label_bold = value
  label_bold = property_with_callback("label_bold", _set_label_bold)

  def _set_label_font(self, value):
    self.selection_field.label_font = value
  label_font_family = property_with_callback("label_font_family", _set_label_font)

  def _set_label_font_size(self, value):
    self.selection_field.label_font_size = value
  label_font_size = property_with_callback("label_font_size", _set_label_font_size)

  def _set_label_text_color(self, value):
    self.selection_field.label_text_color = value
  label_text_color = property_with_callback("label_text_color", _set_label_text_color)

  def _set_label_italic(self, value):
    self.selection_field.label_italic = value
  label_italic = property_with_callback("label_italic", _set_label_italic)

  def _set_label_underline(self, value):
    self.selection_field.label_underline = value
  label_underline = property_with_callback("label_underline", _set_label_underline)

  def _set_enabled(self, value):
    self.selection_field.enabled = value
  enabled = property_with_callback("enabled", _set_enabled)

  def _set_appearance(self, value):
    self.selection_field.appearance = value
  appearance = property_with_callback("appearance", _set_appearance)

  def _set_role(self, value):
    self.selection_field.role = value
  role = property_with_callback("role", _set_role)

  def _set_selected_italic(self, value):
    self.selection_field.display_italic = value
  selected_italic = property_with_callback("selected_italic", _set_selected_italic)

  def _set_selected_bold(self, value):
    self.selection_field.display_bold = value
  selected_bold = property_with_callback("selected_bold", _set_selected_bold)

  def _set_selected_underline(self, value):
    self.selection_field.display_underline = value
  selected_underline = property_with_callback("selected_underline", _set_selected_underline)

  def _set_selected_font(self, value):
    self.selection_field.selected_font = value
  selected_font_family = property_with_callback("selected_font_family", _set_selected_font)

  def _set_selected_font_size(self, value):
    self.selection_field.selected_font_size = value
  selected_font_size = property_with_callback("selected_font_size", _set_selected_font_size)

  def _set_selected_text_color(self, value):
    self.selection_field.selected_text_color = value
  selected_text_color = property_with_callback("selected_text_color", _set_selected_text_color)

  def _set_leading_icon(self, value):
    self.selection_field.leading_icon = value
  leading_icon = property_with_callback("leading_icon", _set_leading_icon)

  def _set_leading_icon_color(self, value):
    self.selection_field.leading_icon_color = value
  leading_icon_color = property_with_callback("leading_icon_color", _set_leading_icon_color)

  def _set_tooltip(self, value):
    self.selection_field.tooltip = value
  tooltip = property_with_callback("tooltip", _set_tooltip)

  def _set_supporting_text(self, value):
    self.selection_field.supporting_text = value
  supporting_text = property_with_callback("supporting_text", _set_supporting_text)

  def _set_supporting_text_color(self, value):
    self.selection_field.supporting_text_color = value
  supporting_text_color = property_with_callback("supporting_text_color", _set_supporting_text_color)

  def _set_supporting_text_font_family(self, value):
    self.selection_field.supporting_text_font_family = value
  supporting_text_font_family = property_with_callback("supporting_text_font_family", _set_supporting_text_font_family)

  def _set_supporting_text_font_size(self, value):
    self.selection_field.supporting_text_font_size = value
  supporting_text_font_size = property_with_callback("supporting_text_font_size", _set_supporting_text_font_size)

  def _set_border_color(self, value):
    self.selection_field.border_color = value
  border_color = property_with_callback("border_color", _set_border_color)

  def _set_menu_color(self, value):
    self.menu.background_color = value
  menu_background_color = property_with_callback("menu_color", _set_menu_color)

  def _set_error(self, value):
    if value: 
      self.dom_nodes['anvil-m3-dropdownMenu-textfield'].classList.add('anvil-m3-dropdown-error')
    else: 
      self.dom_nodes['anvil-m3-dropdownMenu-textfield'].classList.remove('anvil-m3-dropdown-error')
  error = property_with_callback("error", _set_error)

  def _set_label_text(self, value):
    v = value or ""
    self.selection_field.dom_nodes['anvil-m3-label-text'].classList.toggle('anvil-m3-textlessComponentText', False)
    if anvil.designer.in_designer and not value:
      v = self._design_name
      self.selection_field.dom_nodes['anvil-m3-label-text'].classList.toggle('anvil-m3-textlessComponentText', True)
    self.selection_field.label_text = v
  label_text = property_with_callback("label_text", _set_label_text)

  def _set_selected_value(self, value):
    if (value is None and self.allow_none) or (value in self.items):
      if value is None and self.allow_none:
        self._hoverIndex = None
      if isinstance(value, tuple):
        self.selection_field.dom_nodes['anvil-m3-textfield'].value = value[0]
      else:
        self.selection_field.dom_nodes['anvil-m3-textfield'].value = value
    else:
      self.selection_field.dom_nodes['anvil-m3-textfield'].value = "<Invalid value>"
  selected_value = property_with_callback("selected_value", _set_selected_value)

  def _set_placeholder(self, value):
    self.selection_field.placeholder = value
  placeholder = property_with_callback("placeholder", _set_placeholder)

  # placeholder = property_without_callback("placeholder")
  items = property_without_callback("items")
  allow_none = property_without_callback("allow_none")
  bold_items = property_without_callback("bold_items")
  italic_items = property_without_callback("italic_items")
  underline_items = property_without_callback("underline_items")
  items_text_color = property_without_callback("items_text_color")

  items_font = property_without_callback("items_font")
  items_font_size = property_without_callback("items_font_size")
  
  def _on_mount(self, **event_args):
    document.addEventListener('keydown', self._handle_keyboard_events)
    document.addEventListener('click', self._body_click)

    document.body.append(self._menuNode)

    self._cleanup = fui.auto_update(self._field, self._menuNode, placement="bottom-start", offset=0)

    self.dom_nodes['anvil-m3-dropdownMenu-container'].addEventListener('click', self._handle_component_click)
    self.selection_field.dom_nodes['anvil-m3-textfield'].addEventListener('focus', self._handle_selection_field_focus)
    self.selection_field.dom_nodes['anvil-m3-textfield'].addEventListener('blur', self._handle_selection_field_blur)

    self._menuNode.addEventListener('click', self._child_clicked)

  def _on_cleanup(self, **event_args):
    document.removeEventListener('keydown', self._handle_keyboard_events)
    document.removeEventListener('click', self._body_click)
    self.dom_nodes['anvil-m3-dropdownMenu-container'].removeEventListener('click', self._handle_component_click)
    self.selection_field.dom_nodes['anvil-m3-textfield'].removeEventListener('focus', self._handle_selection_field_focus)
    self.selection_field.dom_nodes['anvil-m3-textfield'].removeEventListener('blur', self._handle_selection_field_blur)
    self._menuNode.removeEventListener('click', self._child_clicked)
    self._cleanup()
    self._menuNode.remove()

  def _handle_selection_field_focus(self, event):
    if not self.label_text:
        self.selection_field.dom_nodes['anvil-m3-label-text'].innerText = ""
    self._has_focus = True

  def _handle_selection_field_blur(self, event):
    # if not self.label_text and self.placeholder and self.selected_value is None:
    #     self.selection_field.dom_nodes['anvil-m3-label-text'].innerText = self.placeholder
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

      if event.key not in action_keys: #   #TODO: eventually want to use this to jump somewhere in the list
        return

      if event.key == "ArrowUp" or event.key == "ArrowDown":
        event.preventDefault()
        self._iterate_hover(event.key == "ArrowDown")
        return

      if event.key in ["Tab", "Escape"]:
        self._set_menu_visibility(False)

      if (event.key == " "): #space key as " " is stupid
        event.preventDefault()
        self._attempt_select()
      if (event.key == "Enter"):
        self._attempt_select()

  def _iterate_hover(self, inc = True):
    if inc:
      if self._hoverIndex is None or self._hoverIndex is (len(self._children) - 1):
        self._hoverIndex = -1
      self._hoverIndex += 1
    else:
      if self._hoverIndex is None or self._hoverIndex == 0:
        self._hoverIndex = len(self._children)
      self._hoverIndex -= 1
    self._children[self._hoverIndex].dom_nodes['anvil-m3-menuItem-container'].scrollIntoView({'block': 'nearest'})
    self._update_hover_styles()

  def _attempt_select(self):
    if not self._hoverIndex == None:
      self._children[self._hoverIndex].raise_event("click")
    self._set_menu_visibility(False)

  def _clear_hover_styles(self):
    if self._children is not None:
      for child in self._children:
        # if isinstance(child, MenuItem):
        child.dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', False)
        
  def _update_hover_styles(self):
    self._clear_hover_styles()
    if self._hoverIndex is None:
      return
    self._children[self._hoverIndex].dom_nodes['anvil-m3-menuItem-container'].classList.toggle('anvil-m3-menuItem-container-keyboardHover', True)

  def _handle_component_click(self, event):
    self._set_menu_visibility()

  def _set_menu_visibility(self, value = None):
    if (value is None):
      value = not self.menu.visible
    
    self.menu.visible = value
    self._menuNode.classList.toggle("anvil-m3-menu-hidden", not value)
    
    if value:
      selection_field_width = get_dom_node(self.selection_field).offsetWidth
      self._menuNode.style.width = f"{selection_field_width}px"
      
      # dealing with hover
      if self.allow_none is True:
        if self.selected_value is None:
          self._hoverIndex = 0  
      elif self.selected_value in self.items:
        for index, child in enumerate(self._children):
          if isinstance(self.selected_value, tuple):
            if child.text == self.selected_value:
              self._hoverIndex = index
          else:
            if child.text is self.selected_value:
              self._hoverIndex = index
      else:
        self._hoverIndex = None
          
      self._update_hover_styles()

      if not anvil.designer.in_designer:
        self.selection_field.trailing_icon = "arrow_drop_up"
        if self._hoverIndex:
          self._children[self._hoverIndex].dom_nodes['anvil-m3-menuItem-container'].scrollIntoView({'block': 'nearest'})
        
    else:
      self.selection_field.trailing_icon = "arrow_drop_down"
      if self.selected_value is None:
        self._hoverIndex = None

  def _body_click(self, event):
    icon = self.selection_field.dom_nodes['anvil-m3-icon-container']
    if self._field.contains(event.target) or self._menuNode.contains(event.target) or icon.contains(event.target):
      self._has_focus = True
      return
    self._set_menu_visibility(False)

  def _child_clicked(self, event):
    event.stopPropagation()
    self._set_menu_visibility(False)

  def form_show(self, **event_args):
    self._create_menu_items()
    # selection_field_width = get_dom_node(self.selection_field).offsetWidth
    # self._menuNode.style.width = f"{selection_field_width}px"

    if anvil.designer.in_designer:
      self._design_name = anvil.designer.get_design_name(self)
      if not self.label_text:
        self.selection_field.dom_nodes['anvil-m3-label-text'].innerText = self._design_name

  def _create_menu_items(self):
    p = MenuItem()
    p.text = self.placeholder if self.placeholder else ""
    p.italic = self.italic_items
    p.underline = self.underline_items
    p.text_color = self.items_text_color
    # p.background = self.items_background_color
    p.font = self.items_font
    p.font_size = self.items_font_size
    p.hide_leading_icon = True

    def _handle_select_placeholder(**e):
      if self.allow_none: self.selected_value = None
      self.raise_event("change")

    if not self.allow_none:
      p.enabled = False

    if self.allow_none or self.placeholder:
      p.add_event_handler('click', _handle_select_placeholder)
      self.menu.add_component(p, slot="anvil-m3-menu-slot")
      self._children = [p]

    for item in self.items:
      selection = MenuItem()
      selection.hide_leading_icon = True

      selection.bold = self.bold_items
      selection.italic = self.italic_items
      selection.underline = self.underline_items
      selection.text_color = self.items_text_color
      # selection.background = self.items_background_color
      selection.font = self.items_font
      selection.font_size = self.items_font_size

      # if isinstance(item, tuple):
      #   selection.text = item[0]
      # else:
      #   selection.text = item
      selection.text = item

      def _handle_selection_click(value = item, **e):
        self.selected_value = value
        self.raise_event("change")

      selection.add_event_handler('click', _handle_selection_click)
      self.menu.add_component(selection, slot="anvil-m3-menu-slot")
      if self._children is None:
        self._children = [selection]
      else:
        self._children.append(selection)

# DESIGNER INTERACTIONS
  def _anvil_get_interactions_(self):
    return [
      {
      "type": "whole_component",
      "title": "Edit Label",
      "icon": "edit",
      "default": True,
      "callbacks": {
        "execute": lambda: anvil.designer.start_inline_editing(self, "label_text", self.selection_field.dom_nodes['anvil-m3-label-text'])
      }
    }]

  #!componentProp(material_3.DropdownMenu)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"A predefined style for this component."}  
  #!componentProp(material_3.DropdownMenu)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}

  #!componentProp(material_3.DropdownMenu)!1: {name:"label_text_color",type:"color",description:"The colour of the label text on the component."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_text",type:"string",description:"The label text of the component."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"label_bold",type:"boolean",description:"If True, the label text will be bold."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"items_text_color",type:"color",description:"The colour of the menu items' text."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"items_font_family",type:"string",description:"The font family to use for the menu items."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"items_font_size",type:"number",description:"The font size of the menu items."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"items_underline",type:"boolean",description:"If True, the menu items will be underlined."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"items_italic",type:"boolean",description:"If True, the menu items will be italic."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"items_bold",type:"boolean",description:"If True, the menu items will be bold."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"menu_background_color",type:"color",description:"The background color of the menu."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_text_color",type:"color",description:"The colour of the displayed text if there is a selected item."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_font_size",type:"number",description:"The font size (pixels) of the displayed text if there is a selected item."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_font_family",type:"string",description:"The font-family of the displayed text if there is a selected item."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_underline",type:"boolean",description:"If True and there is a selected item, the displayed text is underlined"}
  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_italic",type:"boolean",description:"If True and there is a selected item, the displayed text in italic."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_bold",type:"boolean",description:"If True and there is a selected item, the displayed text is bold."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"leading_icon",type:"enum",description:"The leading icon to display on this component."} 
  #!componentProp(material_3.DropdownMenu)!1: {name:"leading_icon_color",type:"color",description:"The colour of the leading icon displayed on this component."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed below this component"}
  #!componentProp(material_3.DropdownMenu)!1: {name:"supporting_text_color",type:"color",description:"The colour of the supporting text below this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"supporting_text_font_family",type:"color",description:"The font family to use for the supporting text below this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"supporting_text_font_size",type:"color",description:"The font size of the supporting text displayed below this component."}

  #!componentProp(material_3.DropdownMenu)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"placeholder",type:"string",description:"The text to be displayed when the component is empty"}
  #!componentProp(material_3.DropdownMenu)!1: {name:"allow_none",type:"boolean",description:"If True, a placeholder item is added to the menu with value None"}
  #!componentProp(material_3.DropdownMenu)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"items",type:"string list",description:"The items to display in the menu."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"selected_value",type:"object",description:"The value of the currently selected item. Can only be set at runtime."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
  #!componentProp(material_3.DropdownMenu)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}


  #!componentEvent(material_3.DropdownMenu)!1: {name: "change", description: "When an item is selected.", parameters:[]}

#!defClass(material_3,DropdownMenu, anvil.Component)!:

