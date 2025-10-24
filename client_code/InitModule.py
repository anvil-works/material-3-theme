from anvil import pluggable_ui

from ._Components.Button import Button
from ._Components.Checkbox import Checkbox
from ._Components.TextInput.TextBox import TextBox


def make_button(align=None, **kwargs):
    if align is None:
        align = "center"
    return Button(align=align, **kwargs)


def make_footer_button(button_type, **kwargs):
    return Button(**kwargs)


pluggable_ui.provide(
    "m3",
    {
        "anvil.TextBoxWithLabel": TextBox,
        "anvil.TextBox": TextBox,
        "anvil.Button": make_button,
        "anvil.CheckBox": Checkbox,
        "anvil.alerts.FooterButton": make_footer_button,
    },
)
