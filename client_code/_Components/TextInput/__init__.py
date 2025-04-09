import anvil.server
from anvil import *
from anvil import HtmlTemplate

from ..._utils import gen_id
from ..._utils.properties import (
  anvil_prop,
  bold_property,
  color_property,
  font_family_property,
  font_size_property,
  get_unset_margin,
  get_unset_value,
  innerText_property,
  italic_property,
  margin_property,
  property_with_callback,
  theme_color_to_css,
  tooltip_property,
  underline_property,
)
from ._anvil_designer import TextInputTemplate


class TextInput(TextInputTemplate):
  def __init__(self, **properties):
    self.tag = ComponentTag()
    self._props = properties
    self._tooltip_node = None
    self.init_components(**properties)

    self._on_input = self._on_input

  def _get_common_unset_property_values_(self):
    el = self.dom_nodes['anvil-m3-textinput']
    m = get_unset_margin(el, self.margin)
    lfs = get_unset_value(
      self.dom_nodes['anvil-m3-label-text'], "fontSize", self.label_font_size
    )
    spfs = get_unset_value(
      self.dom_nodes['anvil-m3-subcontent'],
      "fontSize",
      self.subcontent_font_size,
    )
    return {
      "label_font_size": lfs,
      "subcontent_font_size": spfs,
      "margin": m,
    }

  def _set_id(self, value):
    self.dom_nodes["anvil-m3-label-text"].setAttribute("for", value)
    self.dom_nodes["anvil-m3-supporting-text"].setAttribute("for", value)
    self.dom_nodes["anvil-m3-character-amount"].setAttribute("for", value)

  def _on_input(self, e):
    self.dom_nodes['anvil-m3-character-amount'].innerText = len(e.target.value)
    # input event is anvil's change event
    self.raise_event("change")

  def _on_change(self, e):
    # On text input/textarea the change event fires when we lose focus
    self.raise_event("x-anvil-write-back-text")

  def _on_focus(self, e):
    self.raise_event("focus")

  def _on_lost_focus(self, e):
    self.raise_event("lost_focus")

  def _anvil_get_interactions_(self):
    return [
      {
        "type": "whole_component",
        "title": "Edit text",
        "icon": "edit",
        "default": True,
        "callbacks": {
          "execute": lambda: anvil.designer.start_inline_editing(
            self, "label", self.dom_nodes['anvil-m3-label-text']
          )
        },
      }
    ]

  visible = HtmlTemplate.visible
  label_italic = italic_property('anvil-m3-label-text', 'label_italic')
  label_bold = bold_property('anvil-m3-label-text', 'label_bold')
  label_underline = underline_property('anvil-m3-label-text', 'label_underline')
  label_font_size = font_size_property('anvil-m3-label-text', 'label_font_size')
  label_font_family = font_family_property('anvil-m3-label-text', 'label_font_family')
  label_color = color_property('anvil-m3-label-text', 'color', 'label_color')
  margin = margin_property('anvil-m3-textinput')
  tooltip = tooltip_property('anvil-m3-textinput')
  subcontent_color = color_property('anvil-m3-subcontent', 'color', 'subcontent_color')
  subcontent_font_family = font_family_property(
    'anvil-m3-subcontent', 'subcontent_font_family'
  )
  subcontent_font_size = font_size_property(
    'anvil-m3-subcontent', 'subcontent_font_size'
  )
  supporting_text = innerText_property('anvil-m3-supporting-text', 'supporting_text')

  @anvil_prop
  @property
  def appearance(self, value):
    if value == 'outlined':
      self.dom_nodes['anvil-m3-textinput'].classList.toggle('outlined', True)
    else:
      self.dom_nodes['anvil-m3-textinput'].classList.toggle('outlined', False)

  def _set_error(self, value):
    classes = self.dom_nodes['anvil-m3-textinput'].classList
    if value:
      classes.add("anvil-m3-textinput-error")
    else:
      classes.remove("anvil-m3-textinput-error")

  error = property_with_callback('error', _set_error)

  @anvil_prop
  @property
  def border_color(self, value):
    if self.border_color:
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border', theme_color_to_css(self.border_color)
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border-hover', theme_color_to_css(self.border_color)
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border-focus', theme_color_to_css(self.border_color)
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border', theme_color_to_css(self.border_color)
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border-hover', theme_color_to_css(self.border_color)
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border-focus', theme_color_to_css(self.border_color)
      )
    else:
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border', 'var(--anvil-m3-outline)'
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border-hover', 'var(--anvil-m3-on-surface)'
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-outlined-border-focus', 'var(--anvil-m3-primary)'
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border', 'var(--anvil-m3-on-surface-variant)'
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border-hover', 'var(--anvil-m3-on-surface)'
      )
      self.dom_nodes["anvil-m3-textinput"].style.setProperty(
        '--anvil-m3-filled-border-focus', 'var(--anvil-m3-primary)'
      )

  def form_show(self, **event_args):
    id = gen_id()
    self._set_id(id)
    if anvil.designer.in_designer:
      if not self.label:
        self.dom_nodes[
          'anvil-m3-label-text'
        ].innerText = anvil.designer.get_design_name(self)
