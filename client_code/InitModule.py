from anvil import pluggable_ui

from ._Components.Button import Button
from ._Components.Checkbox import Checkbox
from ._Components.TextInput.TextBox import TextBox


def make_button(align=None, **kwargs):
    return Button(align='center', **kwargs)


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


def is_using_legacy_classes():
    # TODO expose this in a public API
    # Probably shouldn't merge this
    from anvil.js import window

    runtime_options = window.debugAnvilData.app.runtime_options
    print(runtime_options)

    version = runtime_options.version
    if version < 3:
        return True

    return runtime_options.get("legacy_features", {}).get("class_names")


def init_runtime_backwards_compatibility():
    if not is_using_legacy_classes():
        return

    print("Loading legacy CSS")

    from anvil.js.window import document

    link = document.createElement("link")
    link.rel = "stylesheet"
    link.href = "_/theme/anvil-m3/legacy.css"
    document.head.append(link)


init_runtime_backwards_compatibility()
