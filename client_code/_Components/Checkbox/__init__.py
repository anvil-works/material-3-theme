import anvil.designer
from anvil import *
from anvil import HtmlTemplate

from ..._utils import gen_id
from ..._utils.properties import (
  anvil_prop,
  bold_property,
  border_property,
  color_property,
  enabled_property,
  font_family_property,
  font_size_property,
  get_unset_spacing,
  get_unset_value,
  italic_property,
  role_property,
  spacing_property,
  simple_prop,
  style_property,
  theme_color_to_css,
  tooltip_property,
  underline_property,
)
from ._anvil_designer import CheckboxTemplate


class Checkbox(CheckboxTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self._allow_indeterminate = properties['allow_indeterminate']
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dom_nodes['anvil-m3-checkbox-hover'].addEventListener(
      "click", self._handle_change
    )

    if not anvil.designer.in_designer:
      id = gen_id()
      self.dom_nodes["anvil-m3-checkbox"].id = id
      self.dom_nodes["anvil-m3-checkbox-label"].setAttribute("for", id)

  def _anvil_get_unset_property_values_(self):
    el = self.dom_nodes["anvil-m3-checkbox-component"]
    sp = get_unset_spacing(el, el, self.spacing)
    fs = get_unset_value(
      self.dom_nodes['anvil-m3-checkbox-label'], "fontSize", self.font_size
    )
    return {"font_size": fs, "spacing": sp}

  #!defMethod(_)!2: "Set the keyboard focus to this Checkbox." ["focus"]
  def focus(self):
    self.dom_nodes['anvil-m3-checkbox'].focus()

  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    if anvil.designer.in_designer and not self.text:
      self.text = anvil.designer.get_design_name(self)

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(
            self, "text", self.dom_nodes['anvil-m3-checkbox-label']
          )
        },
      },
      {
        "type": "region",
        "bounds": self.dom_nodes['anvil-m3-checkbox-hover'],
        "sensitivity": 0,
        "callbacks": {"execute": self._toggle_checked},
      },
    ]

  def _toggle_checked(self):
    self.checked = not self.checked
    anvil.designer.update_component_properties(self, {'checked': self.checked})

  def _handle_change(self, event):
    if self.enabled:
      self.dom_nodes['anvil-m3-checkbox'].focus()
      self.checked = not self.checked
      self.raise_event("change")

  #!componentEvent(m3.Checkbox)!1: {name: "change", description: "When the Checkbox is checked or unchecked."}
  #!componentEvent(m3.Checkbox)!1: {name: "show", description: "When the Checkbox is shown on the screen."}
  #!componentEvent(m3.Checkbox)!1: {name: "hide", description: "When the Checkbox is removed from the screen."}

  #!componentProp(m3.Checkbox)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
  #!componentProp(m3.Checkbox)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
  #!componentProp(m3.Checkbox)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
  #!componentProp(m3.Checkbox)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
  #!componentProp(m3.Checkbox)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
  #!componentProp(m3.Checkbox)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
  #!componentProp(m3.Checkbox)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
  #!componentProp(m3.Checkbox)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
  #!componentProp(m3.Checkbox)!1: {name:"text_color",type:"color",description:"The color of the text on the component."}
  #!componentProp(m3.Checkbox)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
  #!componentProp(m3.Checkbox)!1: {name:"align",type:"enum",description:"The position of this component in the available space."}
  #!componentProp(m3.Checkbox)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
  #!componentProp(m3.Checkbox)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
  #!componentProp(m3.Checkbox)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
  #!componentProp(m3.Checkbox)!1: {name:"text",type:"string",description:"The text displayed on this component"}
  #!componentProp(m3.Checkbox)!1: {name:"checkbox_color",type:"color",description:"The color of the checkbox."}
  #!componentProp(m3.Checkbox)!1: {name:"checked",type:"boolean",description:"If True, the checkbox is checked."}
  #!componentProp(m3.Checkbox)!1: {name:"allow_indeterminate",type:"boolean",description:"If True, supports an indeterminate state. The indeterminate state can only be set in code by setting checked=None."}
  #!componentProp(m3.Checkbox)!1: {name:"error",type:"boolean",description:"If True, the checkbox is in an error state."}
  #!componentProp(m3.Checkbox)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

  enabled = enabled_property('anvil-m3-checkbox')
  visible = HtmlTemplate.visible
  underline = underline_property('anvil-m3-checkbox-label')
  italic = italic_property('anvil-m3-checkbox-label')
  bold = bold_property('anvil-m3-checkbox-label')
  font_size = font_size_property('anvil-m3-checkbox-label')
  border = border_property('anvil-m3-checkbox-container')
  font_family = font_family_property('anvil-m3-checkbox-label', 'font')
  text_color = color_property('anvil-m3-checkbox-label', 'color', 'text_color')
  background_color = color_property(
    'anvil-m3-checkbox-component', 'backgroundColor', 'background'
  )
  align = style_property('anvil-m3-checkbox-component', 'justifyContent', 'align')
  spacing = spacing_property('anvil-m3-checkbox-component')
  tooltip = tooltip_property('anvil-m3-checkbox-container')
  role = role_property('anvil-m3-checkbox-container')
  allow_indeterminate = simple_prop('allow_indeterminate')

  @anvil_prop
  @property
  def text(self, value) -> str:
    """The text displayed on this component"""
    if value:
      self.dom_nodes['anvil-m3-checkbox-label'].innerText = str(value if value is not None else "")
      self.dom_nodes['anvil-m3-checkbox-label'].style.display = 'block'
    else:
      self.dom_nodes['anvil-m3-checkbox-label'].style.display = 'none'

  @anvil_prop
  @property
  def checkbox_color(self, value) -> str:
    """The color of the checkbox."""
    if value:
      value = theme_color_to_css(value)
    self.dom_nodes['anvil-m3-checkbox-unchecked'].style.color = value
    self.dom_nodes['anvil-m3-checkbox-checked'].style.color = value
    self.dom_nodes['anvil-m3-checkbox-indeterminate'].style.color = value

  @anvil_prop
  @property
  def checked(self, value) -> bool:
    """If True, the checkbox is checked."""
    if value is None and self.allow_indeterminate:
      self.dom_nodes['anvil-m3-checkbox'].indeterminate = True
      self.dom_nodes['anvil-m3-checkbox-unchecked'].style.display = 'none'
      self.dom_nodes['anvil-m3-checkbox-checked'].style.display = 'none'
      self.dom_nodes['anvil-m3-checkbox-indeterminate'].style.display = 'inline'
    elif value is True:
      self.dom_nodes['anvil-m3-checkbox'].checked = value
      self.dom_nodes['anvil-m3-checkbox-unchecked'].style.display = 'none'
      self.dom_nodes['anvil-m3-checkbox-checked'].style.display = 'inline'
      self.dom_nodes['anvil-m3-checkbox-indeterminate'].style.display = 'none'
    else:
      self.dom_nodes['anvil-m3-checkbox'].checked = value
      self.dom_nodes['anvil-m3-checkbox-unchecked'].style.display = 'inline'
      self.dom_nodes['anvil-m3-checkbox-checked'].style.display = 'none'
      self.dom_nodes['anvil-m3-checkbox-indeterminate'].style.display = 'none'

  @anvil_prop
  @property
  def error(self, value) -> bool:
    """If True, the checkbox is in an error state."""
    self.dom_nodes['anvil-m3-checkbox-container'].classList.remove(
      'anvil-m3-checkbox-error'
    )
    if value:
      self.dom_nodes['anvil-m3-checkbox-container'].classList.add(
        'anvil-m3-checkbox-error'
      )


#!defClass(m3,Checkbox, anvil.Component)!:
