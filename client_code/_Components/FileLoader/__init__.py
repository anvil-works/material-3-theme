import anvil.server
from anvil import *

from ..._utils import gen_id
from ..._utils.properties import (
    anvil_prop,
    bold_property,
    color_property,
    enabled_property,
    font_family_property,
    font_size_property,
    get_unset_spacing,
    get_unset_value,
    innerText_property,
    italic_property,
    role_property,
    simple_prop,
    spacing_property,
    style_property,
    tooltip_property,
    underline_property,
)
from ._anvil_designer import FileLoaderTemplate


class FileLoader(FileLoaderTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._tooltip_node = None
        self.init_components(**properties)

        self._handle_change = self._handle_change
        self._handle_focus = self._handle_focus
        self._handle_lost_focus = self._handle_lost_focus

        self.dom_nodes['anvil-m3-fileloader-input'].addEventListener(
            "change", self._handle_change
        )
        self.dom_nodes['anvil-m3-fileloader-container'].addEventListener(
            "focus", self._handle_focus
        )
        self.dom_nodes['anvil-m3-fileloader-container'].addEventListener(
            "blur", self._handle_lost_focus
        )

        if not anvil.designer.in_designer:
            id = gen_id()
            self.dom_nodes["anvil-m3-fileloader-input"].id = id
            self.dom_nodes["anvil-m3-fileloader-label"].setAttribute("for", id)

    def _anvil_get_interactions_(self):
        return [
            {
                "type": "whole_component",
                "title": "Edit text",
                "icon": "edit",
                "default": True,
                "callbacks": {
                    "execute": lambda: anvil.designer.start_inline_editing(
                        self, "text", self.dom_nodes['anvil-m3-fileloader-label']
                    )
                },
            }
        ]

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-fileloader-form"]
        sp = get_unset_spacing(el, el, self.spacing)
        tfs = get_unset_value(
            self.dom_nodes['anvil-m3-fileloader-label'], "fontSize", self.font_size
        )
        ifs = get_unset_value(
            self.dom_nodes['anvil-m3-fileloader-icon'], "fontSize", self.icon_size
        )
        return {"font_size": tfs, "icon_size": ifs, "spacing": sp}

    #!defMethod(_)!2: "Clear any selected files from this FileLoader." ["clear"]
    def clear(self):
        self.dom_nodes['anvil-m3-fileloader-input'].value = ''
        self.file = None
        self.dom_nodes['anvil-m3-fileloader-label'].innerText = str(
            self.text if self.text is not None else ""
        )
        # update show_state text if present

    #!defMethod(_)!2: "Set the keyboard focus to this FileLoader." ["focus"]
    def focus(self):
        self.dom_nodes['anvil-m3-fileloader-container'].focus()

    #!defMethod(_)!2: "Open the file selector from code, this should be called within a click event handler for another component." ["open_file_selector"]
    def open_file_selector(self):
        self.dom_nodes['anvil-m3-fileloader-input'].click()

    def _handle_change(self, event, **event_args):
        files = self.dom_nodes['anvil-m3-fileloader-input'].files
        if not files:
            return
        self.files = [anvil.js.to_media(file) for file in files]
        self.file = self.files[0]
        self.raise_event('change', file=self.files[0], files=self.files)
        if self.show_state:
            num_files = len(files)
            self.dom_nodes['anvil-m3-fileloader-label'].innerText = (
                "1 file selected" if num_files == 1 else f"{num_files} files selected"
            )

    def _handle_focus(self, event, **event_args):
        self.raise_event("focus")

    def _handle_lost_focus(self, event, **event_args):
        self.raise_event("lost_focus")

    #!componentEvent(m3.FileLoader)!1: {name: "change", description: "When a new file is loaded into this FileLoader.", parameters:[{name: "file", description: "The first selected file. Set the 'multiple' property to allow loading more than one file."},{name: "files", description: "A list of loaded files. Set the 'multiple' property to allow loading more than one file."}]}
    #!componentEvent(m3.FileLoader)!1: {name: "show", description: "When the FileLoader is shown on the screen."}
    #!componentEvent(m3.FileLoader)!1: {name: "hide", description: "When the FileLoader is removed from the screen."}
    #!componentEvent(m3.FileLoader)!1: {name: "focus", description: "When the FileLoader gets focus."}
    #!componentEvent(m3.FileLoader)!1: {name: "lost_focus", description: "When the FileLoader loses focus."}

    #!componentProp(m3.FileLoader)!1: {name:"text",type:"string",description:"The text displayed on this component"}
    #!componentProp(m3.FileLoader)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.FileLoader)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.FileLoader)!1: {name:"text_color",type:"color",description:"The color of the text on the component."}
    #!componentProp(m3.FileLoader)!1: {name:"icon_color",type:"color",description:"The color of the icon displayed on this component."}
    #!componentProp(m3.FileLoader)!1: {name:"background_color",type:"color",description:"The color of the background of this component."}
    #!componentProp(m3.FileLoader)!1: {name:"underline",type:"boolean",description:"If True, this component’s text will be underlined."}
    #!componentProp(m3.FileLoader)!1: {name:"italic",type:"boolean",description:"If True, this component’s text will be italic."}
    #!componentProp(m3.FileLoader)!1: {name:"bold",type:"boolean",description:"If True, this component’s text will be bold."}
    #!componentProp(m3.FileLoader)!1: {name:"font_family",type:"string",description:"The font family to use for this component."}
    #!componentProp(m3.FileLoader)!1: {name:"icon_size",type:"number",description:"The size (pixels) of the icon displayed on this component."}
    #!componentProp(m3.FileLoader)!1: {name:"font_size",type:"number",description:"The font size of text displayed on this component."}
    #!componentProp(m3.FileLoader)!1: {name:"align",type:"enum", options:["left", "center", "right"],description:"The position of this component in the available space."}
    #!componentProp(m3.FileLoader)!1: {name:"border",type:"string",description:"The border of this component. Can take any valid CSS border value."}
    #!componentProp(m3.FileLoader)!1: {name:"spacing",type:"spacing",description:"The margin and padding (pixels) of the component."}
    #!componentProp(m3.FileLoader)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.FileLoader)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.FileLoader)!1: {name:"appearance",type:"enum",options:["text", "filled", "elevated", "tonal", "outlined"],description:"A predefined style for this component."}
    #!componentProp(m3.FileLoader)!1: {name:"show_state",type:"boolean",description:"If True, display a message indicating the number of selected files."}
    #!componentProp(m3.FileLoader)!1: {name:"icon",type:"enum",description:"The icon to display on this component."}
    #!componentProp(m3.FileLoader)!1: {name:"file_types",type:"string",description:"Specify what type of file to upload. Can accept a MIME type (eg 'image/png' or 'image/*'), an extension (eg '.png'), or a comma-separated set of them (eg '.png,.jpg,.jpeg')."}
    #!componentProp(m3.FileLoader)!1: {name:"multiple",type:"boolean",description:"If True, this FileLoader can load multiple files at the same time."}
    #!componentProp(m3.FileLoader)!1: {name:"file",type:"object",description:"The currently selected file (or the first, if multiple files are selected). This is a Media object."}
    #!componentProp(m3.FileLoader)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    text = innerText_property('anvil-m3-fileloader-label')
    visible = HtmlTemplate.visible
    enabled = enabled_property('anvil-m3-fileloader-input')
    text_color = color_property('anvil-m3-fileloader-label', 'color', 'text_color')
    icon_color = color_property('anvil-m3-fileloader-icon', 'color', 'icon_color')
    background_color = color_property(
        'anvil-m3-fileloader-form', 'backgroundColor', 'background_color'
    )
    underline = underline_property('anvil-m3-fileloader-label')
    italic = italic_property('anvil-m3-fileloader-label')
    bold = bold_property('anvil-m3-fileloader-label')
    font_family = font_family_property('anvil-m3-fileloader-label', 'font')
    icon_size = font_size_property('anvil-m3-fileloader-icon', 'icon_size')
    font_size = font_size_property('anvil-m3-fileloader-label', 'font_size')
    # align = style_property('anvil-m3-fileloader-form', 'justifyContent', 'align')
    border = style_property('anvil-m3-fileloader-container', 'border', 'border')
    spacing = spacing_property('anvil-m3-fileloader-container')
    tooltip = tooltip_property('anvil-m3-fileloader-container')
    role = role_property('anvil-m3-fileloader-container')
    show_state = simple_prop("show_state")
    file = simple_prop("file")
    files = simple_prop("files")


    @anvil_prop
    @property
    def align(self, value) -> str:
        """The position of this component in the available space."""
        self.dom_nodes['anvil-m3-fileloader-form'].classList.toggle('anvil-m3-full-width', False)
        if value == 'full':
            self.dom_nodes['anvil-m3-fileloader-form'].classList.toggle(
                'anvil-m3-full-width', True
            )
        else:
            self.dom_nodes['anvil-m3-fileloader-form'].style.justifyContent = value

    @anvil_prop
    @property
    def appearance(self, value) -> str:
        """A predefined style for this component."""
        file_loader = self.dom_nodes['anvil-m3-fileloader-container']
        file_loader.classList.remove('anvil-m3-elevated')
        file_loader.classList.remove('anvil-m3-filled')
        file_loader.classList.remove('anvil-m3-tonal')
        file_loader.classList.remove('anvil-m3-outlined')
        if value and value != 'text':
            file_loader.classList.add(f"anvil-m3-{value}")

    @anvil_prop(default_value="mi:file_upload")
    @property
    def icon(self, value) -> str:
        """The icon to display on this component."""
        if value:
            self.dom_nodes['anvil-m3-fileloader-icon'].style.marginRight = "8px"
        else:
            self.dom_nodes['anvil-m3-fileloader-icon'].style.marginRight = ""
        self.dom_nodes['anvil-m3-fileloader-icon'].innerText = value[3:]

    @anvil_prop
    @property
    def file_types(self, value) -> str:
        """Specify what type of file to upload. Can accept a MIME type (eg 'image/png' or 'image/*'), an extension (eg '.png'), or a comma-separated set of them (eg '.png,.jpg,.jpeg')."""
        self.dom_nodes['anvil-m3-fileloader-input'].accept = value

    @anvil_prop
    @property
    def multiple(self, value) -> bool:
        """If True, this FileLoader can load multiple files at the same time."""
        self.dom_nodes['anvil-m3-fileloader-input'].multiple = value


#!defClass(m3, FileLoader, anvil.Component)!:
