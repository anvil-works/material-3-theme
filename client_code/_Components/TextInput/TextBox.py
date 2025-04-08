import anvil.designer
import anvil.server

from ..._utils.properties import (
  anvil_prop,
  bold_property,
  color_property,
  font_family_property,
  font_size_property,
  get_unset_value,
  italic_property,
  property_with_callback,
  underline_property,
  style_property,
)
from . import TextInput

text_property = {
  "name": "text",
  "type": "string",
  "default_value": "None",
  "description": "The text displayed on this component.",
  "supportsWriteback": True,
  "important": True,
}
leading_icon_property = {
  "name": "leading_icon",
  "type": "icon",
  "iconsets": ["material-icons"],
  "group": "Icon",
  "important": True,
  "default_value": "None",
  "includeNoneOption": True,  # This might change to snake case at some point
  "noneOptionLabel": "None",
  "description": "The leading icon to display on this component.",
}
trailing_icon_property = {
  "name": "trailing_icon",
  "type": "icon",
  "group": "Icon",
  "iconsets": ["material-icons"],
  "important": True,
  "default_value": "None",
  "includeNoneOption": True,
  "noneOptionLabel": "None",
  "description": "The trailing icon to display on this component.",
}
type_property = {
  "name": "type",
  "type": "enum",
  "options": ["text", "number", "email", "tel", "url"],
  "group": "Other",
  "important": False,
  "default_value": "text",
  "description": "The type of data that the user can enter into this box.",
}
hide_text_property = {
  "name": "hide_text",
  "type": "boolean",
  "group": "Other",
  "important": False,
  "default_value": False,
  "description": "If True, display stars instead of text when the user types input into this component.",
}
leading_icon_color_property = {
  "name": "leading_icon_color",
  "type": "color",
  "group": "Look and Feel",
  "important": False,
  "default_value": "",
  "description": "The colour of the leading icon.",
}
trailing_icon_color_property = {
  "name": "trailing_icon_color",
  "type": "color",
  "group": "Look and Feel",
  "important": False,
  "default_value": "",
  "description": "The colour of the trailing icon.",
}

click_event = {
  "name": "trailing_icon_click",
  "defaultEvent": False,
  "description": "When the trailing icon is clicked.",
}
pressed_enter_event = {
  "name": "pressed_enter",
  "defaultEvent": True,
  "description": "When the user presses enter in this component.",
}


class TextBox(TextInput):
  _anvil_properties_ = [
    text_property,
    leading_icon_property,
    trailing_icon_property,
    type_property,
    hide_text_property,
    leading_icon_color_property,
    trailing_icon_color_property,
    *TextInput._anvil_properties_,
  ]
  _anvil_events_ = [click_event, pressed_enter_event, *TextInput._anvil_events_]

  def __init__(self, **properties):
    super().__init__(**properties)
    self.init_components(**properties)

    self.display_italic = self.display_italic
    self.display_bold = self.display_bold
    self.display_underline = self.display_underline
    self.display_font_size = self.display_font_size
    self.display_font_family = self.display_font_family
    self.display_text_color = self.display_text_color
    self.background_color = self.background_color
    self.leading_icon_color = self.leading_icon_color
    self.trailing_icon_color = self.trailing_icon_color
    self.placeholder = self.placeholder
    self.text = self.text
    self.label = self.label
    self.enabled = self.enabled
    self.read_only = self.read_only
    self.error = self.error
    self.leading_icon = self.leading_icon
    self.character_limit = self.character_limit
    self.type = self.type
    self.hide_text = self.hide_text

    hiddenInput = self.dom_nodes['anvil-m3-textarea']
    self.dom_nodes['anvil-m3-input-container'].removeChild(hiddenInput)

    self._on_key_down = self._on_key_down
    self._on_change = self._on_change
    self._handle_click = self._handle_click
    self._on_focus = self._on_focus
    self._on_lost_focus = self._on_lost_focus

    self.dom_nodes['anvil-m3-textbox'].addEventListener("input", self._on_input)
    self.dom_nodes['anvil-m3-textbox'].addEventListener("keydown", self._on_key_down)
    self.dom_nodes['anvil-m3-textbox'].addEventListener("change", self._on_change)
    self.dom_nodes['anvil-m3-textbox'].addEventListener("focus", self._on_focus)
    self.dom_nodes['anvil-m3-textbox'].addEventListener("blur", self._on_lost_focus)
    self.dom_nodes['anvil-m3-trailing-icon'].addEventListener(
      "click", self._handle_click
    )

  def _on_key_down(self, e):
    if getattr(e, 'key', None) == "Enter":
      self.raise_event("x-anvil-write-back-text")
      self.raise_event("pressed_enter")

  def _handle_click(self, event):
    event.preventDefault()
    self.raise_event(
      "trailing_icon_click",
      event=event,
      keys={
        "shift": event.shiftKey,
        "alt": event.altKey,
        "ctrl": event.ctrlKey,
        "meta": event.metaKey,
      },
    )

  def _set_id(self, value):
    super()._set_id(value)
    self.dom_nodes["anvil-m3-textbox"].id = value

  def _anvil_get_unset_property_values_(self):
    common_props = TextInput._get_common_unset_property_values_(self)
    common_props['display_font_size'] = get_unset_value(
      self.dom_nodes['anvil-m3-textbox'], "fontSize", self.display_font_size
    )
    return common_props

  def focus(self):
    self.dom_nodes['anvil-m3-textbox'].focus()

  def select(self):
    self.dom_nodes['anvil-m3-textbox'].select()

  display_italic = italic_property('anvil-m3-textbox', 'display_italic')
  display_bold = bold_property('anvil-m3-textbox', 'display_bold')
  display_underline = underline_property('anvil-m3-textbox', 'display_underline')
  display_font_size = font_size_property('anvil-m3-textbox', 'display_font_size')
  display_font_family = font_family_property('anvil-m3-textbox', 'display_font')
  display_text_color = color_property('anvil-m3-textbox', 'color', 'display_text_color')
  background_color = color_property(
    'anvil-m3-textbox', 'backgroundColor', 'background_color'
  )
  leading_icon_color = color_property(
    'anvil-m3-leading-icon', 'color', 'leading_icon_color'
  )
  trailing_icon_color = color_property(
    'anvil-m3-trailing-icon', 'color', 'trailing_icon_color'
  )

  @anvil_prop
  @property
  def placeholder(self, value) -> str:
    """The text to be displayed when the component is empty"""
    input = self.dom_nodes['anvil-m3-textbox']
    if value:
      input.placeholder = value
      input.classList.add('anvil-m3-has-placeholder')
    else:
      input.placeholder = " "
      input.classList.remove('anvil-m3-has-placeholder')

  @property
  def text(self):
    if self._props.get('type') == "number" and self.dom_nodes['anvil-m3-textbox'].value:
      return float(self.dom_nodes['anvil-m3-textbox'].value)
    else:
      return self.dom_nodes['anvil-m3-textbox'].value

  @text.setter
  def text(self, value):
    self.dom_nodes['anvil-m3-textbox'].value = value

  @anvil_prop
  @property
  def label(self, value) -> str:
    """The label text of the component."""
    self.dom_nodes['anvil-m3-label-text'].innerText = value or ""
    if value:
      self.dom_nodes['anvil-m3-textbox'].classList.toggle('has_label_text', True)
    else:
      self.dom_nodes['anvil-m3-textbox'].classList.toggle(
        'has_label_text', anvil.designer.in_designer
      )

  @anvil_prop
  @property
  def enabled(self, value) -> bool:
    """If True, this component allows user interaction."""
    supporting_text = self.dom_nodes['anvil-m3-subcontent']
    trailing_icon = self.dom_nodes['anvil-m3-trailing-icon']
    if value:
      self.dom_nodes['anvil-m3-textbox'].removeAttribute("disabled")
      supporting_text.classList.remove("anvil-m3-textinput-disabled")
      trailing_icon.classList.remove("anvil-m3-disable-icon")
    else:
      self.dom_nodes['anvil-m3-textbox'].setAttribute("disabled", " ")
      supporting_text.classList.add("anvil-m3-textinput-disabled")
      trailing_icon.classList.add("anvil-m3-disable-icon")

  @anvil_prop
  @property
  def read_only(self, value) -> bool:
    """If True, this component won't allow it's value to be changed."""
    if value:
      self.dom_nodes['anvil-m3-textbox'].setAttribute("readonly", " ")
    else:
      self.dom_nodes['anvil-m3-textbox'].removeAttribute("readonly")

  @anvil_prop
  @property
  def error(self, value) -> bool:
    """If True, this component is in an error state."""
    super()._set_error(value)
    if value:
      icon = "mi:error"
      self._set_trailing_icon(icon)
      self.dom_nodes["anvil-m3-trailing-icon"].classList.add("anvil-m3-error-icon")
    else:
      icon = self.trailing_icon
      self._set_trailing_icon(icon)
      self.dom_nodes["anvil-m3-trailing-icon"].classList.remove("anvil-m3-error-icon")

  @anvil_prop
  @property
  def leading_icon(self, value) -> str:
    """The leading icon to display on this component."""
    icon_container = self.dom_nodes['anvil-m3-icon-container']
    leading_icon = self.dom_nodes['anvil-m3-leading-icon']
    text_box_input = self.dom_nodes['anvil-m3-textbox']
    border_container = self.dom_nodes['anvil-m3-border-container']
    if value:
      leading_icon.style.display = "block"
      leading_icon.innerText = value[3:]
      icon_container.style.paddingLeft = "12px"
      text_box_input.style.paddingLeft = "48px"
      border_container.classList.add("with-icon")
    else:
      leading_icon.style.display = "none"
      leading_icon.innerText = ""
      icon_container.style.paddingLeft = "16px"
      text_box_input.style.paddingLeft = "16px"
      border_container.classList.remove("with-icon")

  def _set_trailing_icon(self, value):
    trailing_icon = self.dom_nodes['anvil-m3-trailing-icon']
    text_box_input = self.dom_nodes['anvil-m3-textbox']
    if value:
      trailing_icon.style.display = "block"
      trailing_icon.innerText = value[3:]
      text_box_input.style.paddingRight = "48px"
    else:
      trailing_icon.style.display = "none"
      trailing_icon.innerText = ""
      text_box_input.style.paddingRight = "16px"

  trailing_icon = property_with_callback('trailing_icon', _set_trailing_icon)

  @anvil_prop
  @property
  def character_limit(self, value) -> float:
    """The max number of characters a user can enter into this component. The limit is displayed below the component."""
    if value is None or value < 1:
      text_box_input = self.dom_nodes['anvil-m3-textbox'].removeAttribute("maxlength")
      self.dom_nodes['anvil-m3-character-counter'].style = "display: none"
    else:
      text_box_input = self.dom_nodes['anvil-m3-textbox'].setAttribute(
        "maxlength", value
      )
      self.dom_nodes['anvil-m3-character-counter'].style = "display: inline"
      self.dom_nodes['anvil-m3-character-limit'].innerText = int(value)

  @anvil_prop
  @property
  def type(self, value) -> str:
    """The type of data that the user can enter into this box."""
    self.dom_nodes['anvil-m3-textbox'].setAttribute("type", value)

  @anvil_prop
  @property
  def hide_text(self, value) -> bool:
    """If True, display stars instead of text when the user types input into this component."""
    self.dom_nodes['anvil-m3-textbox'].setAttribute(
      "type", "password" if value else self.type
    )

  align = style_property('anvil-m3-textbox', 'textAlign', 'align')

  #!componentProp(m3.TextBox)!1: {name:"align",type:"enum",options:["left", "right", "center"],description:"The position of this component in the available space."}
  #!componentProp(m3.TextBox)!1: {name:"appearance",type:"enum",options:["filled", "outlined"],description:"A predefined style for this component."}
  #!componentProp(m3.TextBox)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.TextBox)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.TextBox)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
  #!componentProp(m3.TextBox)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}

  #!componentProp(m3.TextBox)!1: {name:"label_color",type:"color",description:"The colour of the label text on the component."}
  #!componentProp(m3.TextBox)!1: {name:"label",type:"string",description:"The label text of the component."}
  #!componentProp(m3.TextBox)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label this component."}
  #!componentProp(m3.TextBox)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
  #!componentProp(m3.TextBox)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
  #!componentProp(m3.TextBox)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
  #!componentProp(m3.TextBox)!1: {name:"label_bold",type:"boolean",description:"If True, the label text will be bold."}

  #!componentProp(m3.TextBox)!1: {name:"display_text_color",type:"color",description:"The colour of the input text displayed on this component."}
  #!componentProp(m3.TextBox)!1: {name:"display_font_family",type:"string",description:"The font family to use for the input and placeholder text."}
  #!componentProp(m3.TextBox)!1: {name:"display_font_size",type:"number",description:"The font size of the input and placeholder text."}
  #!componentProp(m3.TextBox)!1: {name:"display_underline",type:"boolean",description:"If True, the input and placeholder text will be underlined."}
  #!componentProp(m3.TextBox)!1: {name:"display_italic",type:"boolean",description:"If True, the input and placeholder text will be italic."}
  #!componentProp(m3.TextBox)!1: {name:"display_bold",type:"boolean",description:"If True, the input and placeholder text will be bold."}

  #!componentProp(m3.TextBox)!1: {name:"leading_icon",type:"enum",description:"The leading icon to display on this component."}
  #!componentProp(m3.TextBox)!1: {name:"trailing_icon",type:"enum",description:"The trailing icon to display on this component."}
  #!componentProp(m3.TextBox)!1: {name:"leading_icon_color",type:"color",description:"The colour of the leading icon displayed on this component."}
  #!componentProp(m3.TextBox)!1: {name:"trailing_icon_color",type:"color",description:"The colour of the trailing icon displayed on this component."}

  #!componentProp(m3.TextBox)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed below this component"}
  #!componentProp(m3.TextBox)!1: {name:"character_limit",type:"number",description:"The max number of characters a user can enter into this component. The limit is displayed below the component."}
  #!componentProp(m3.TextBox)!1: {name:"subcontent_color",type:"color",description:"The colour of the supporting text and the character limit below this component."}
  #!componentProp(m3.TextBox)!1: {name:"subcontent_font_family",type:"color",description:"The font family to use for the supporting text and the character limit below this component."}
  #!componentProp(m3.TextBox)!1: {name:"subcontent_font_size",type:"color",description:"The font size of the supporting text and the character limit displayed below this component."}

  #!componentProp(m3.TextBox)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
  #!componentProp(m3.TextBox)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
  #!componentProp(m3.TextBox)!1: {name:"placeholder",type:"string",description:"The text to be displayed when the component is empty"}

  #!componentProp(m3.TextBox)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.TextBox)!1: {name:"type",type:"enum",options:["text", "number", "email", "tel", "url"],description:"The type of data that the user can enter into this box."}
  #!componentProp(m3.TextBox)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.TextBox)!1: {name:"text",type:"string",description:"The input text to display on this component"}
  #!componentProp(m3.TextBox)!1: {name:"hide_text",type:"boolean",description:"If True, display stars instead of text when the user types input into this component."}
  #!componentProp(m3.TextBox)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  #!componentEvent(m3.TextBox)!1: {name: "change", description: "When the text in this component is edited.", parameters:[]}
  #!componentEvent(m3.TextBox)!1: {name: "focus", description: "When the component gets focus.", parameters:[]}
  #!componentEvent(m3.TextBox)!1: {name: "lost_focus", description: "When the component loses focus.", parameters:[]}
  #!componentEvent(m3.TextBox)!1: {name: "trailing_icon_click", description: "When the trailing icon is clicked.", parameters:[]}
  #!componentEvent(m3.TextBox)!1: {name: "pressed_enter", description: "When the user presses enter in this component.", parameters:[]}

  #!defMethod(_)!2: "Set the keyboard focus to this TextBox." ["focus"]
  #!defMethod(_)!2: "Set the input text on this TextBox." ["select"]


#!defClass(m3,TextBox, anvil.Component)!:
