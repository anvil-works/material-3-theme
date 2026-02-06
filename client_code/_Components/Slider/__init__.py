import anvil.js
from anvil import *
from anvil import HtmlTemplate
from anvil.designer import in_designer
from anvil.js.window import ResizeObserver, document

from ..._utils.properties import (
    anvil_prop,
    color_property,
    get_unset_margin,
    margin_property,
    role_property,
    simple_prop,
    theme_color_to_css,
    tooltip_property,
)
from ._anvil_designer import SliderTemplate


class Slider(SliderTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self.label_container = document.createElement('div')
        self.label_container.classList.add('anvil-m3-slider-label-container')
        self.label = document.createElement('div')
        self.label.classList.add('anvil-m3-slider-label')
        self.label_container.appendChild(self.label)
        self._props = properties
        self._tooltip_node = None
        self._mounted = False
        self.init_components(**properties)

        self.dom_nodes["anvil-m3-slider-input"].addEventListener(
            "input", self._on_input
        )
        self.dom_nodes["anvil-m3-slider-input"].addEventListener(
            "mousedown", self._on_mouse_down
        )
        self.dom_nodes['anvil-m3-slider-input'].addEventListener(
            "change", self._on_change
        )
        self.add_event_handler("x-anvil-page-added", self._on_mount)
        self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

    def focus(self):
        self.dom_nodes["anvil-m3-slider-input"].focus()

    def _on_mount(self, **event_args):
        self.resize_observer = ResizeObserver(self._on_window_resize)
        self.resize_observer.observe(self.dom_nodes['anvil-m3-slider'])
        self._mounted = True
        self._set_markers()
        self.dom_nodes[
            'anvil-m3-slider-track-container'
        ].style.width = self._get_track_width()
        self._update_progress()

    def _on_cleanup(self, **event_args):
        self.resize_observer.unobserve(self.dom_nodes['anvil-m3-slider'])
        self._mounted = False

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes["anvil-m3-slider"]
        m = get_unset_margin(el, self.margin)
        return {"margin": m}

    def _on_change(self, event):
        self.raise_event("change_end")

    def _on_input(self, event):
        self._update_progress()
        self.raise_event("change")

    def _on_mouse_down(self, event):
        self._do_show_label()
        document.addEventListener("mouseup", self._on_mouse_up)

    def _on_mouse_up(self, event):
        self._do_hide_label()
        document.removeEventListener("mouseup", self._on_mouse_up)

    def _on_window_resize(self, *args):
        self.dom_nodes[
            'anvil-m3-slider-track-container'
        ].style.width = self._get_track_width()
        self._set_markers()
        self._update_progress()

    def _update_progress(self):
        slider = self.dom_nodes["anvil-m3-slider-input"]
        progress = self.dom_nodes["anvil-m3-slider-progress"]
        background = self.dom_nodes["anvil-m3-slider-background"]
        range = float(slider.max) - float(slider.min)
        abs_value = float(slider.value) - float(slider.min)
        percent = (abs_value / range) * 100
        progress.style.width = f"max(calc({percent}% - 6px), 0px)"
        background.style.width = f"max(calc({100 - percent}% - 6px), 0px)"
        progress_right, progress_top = self._check_position()
        self.label.textContent = slider.value
        self.label_container.style.left = str(progress_right) + "px"
        self.label_container.style.top = str(progress_top) + "px"
        if slider.value == slider.min:
            self.label_container.style.marginLeft = '-25px'
        else:
            self.label_container.style.marginLeft = '-18px'

    def _get_track_width(self):
        input = self.dom_nodes["anvil-m3-slider-input"]
        input_width = input.getBoundingClientRect().width
        return str(input_width - 4) + "px"

    def _check_position(self):
        progress_rect = self.dom_nodes[
            "anvil-m3-slider-progress"
        ].getBoundingClientRect()
        progress_right = progress_rect.right
        progress_top = progress_rect.top
        return progress_right, progress_top

    def _do_show_label(self):
        if self.show_label:
            self.label_container.remove()
            document.body.appendChild(self.label_container)
            self._update_progress()

    def _do_hide_label(self):
        self.label_container.remove()

    def _set_markers(self):
        slider = self.dom_nodes["anvil-m3-slider-input"]
        markers_container_bg = self.dom_nodes["anvil-m3-slider-markers-container-bg"]
        markers_container_progress = self.dom_nodes[
            "anvil-m3-slider-markers-container-progress"
        ]
        markers_container_bg.innerHTML = ''
        markers_container_progress.innerHTML = ''
        markers_container_bg.style.width = self._get_track_width()
        markers_container_progress.style.width = self._get_track_width()
        slider_range = float(slider.max) - float(slider.min)
        if slider.step != 'null':
            marker_count = int(slider_range // float(slider.step))
        else:
            marker_count = slider_range
        if self.show_markers:
            for i in range(marker_count + 1):
                marker_bg = document.createElement('span')
                marker_progress = document.createElement('span')
                marker_bg.classList.add('anvil-m3-slider-marker-bg')
                marker_progress.classList.add('anvil-m3-slider-marker-progress')
                markers_container_bg.appendChild(marker_bg)
                markers_container_progress.appendChild(marker_progress)

    #!componentProp(m3.Slider)!1: {name:"show_label",type:"boolean",description:"If True, display a label above the thumb with the current value."}
    #!componentProp(m3.Slider)!1: {name:"progress_color",type:"color",description:"The colour of the progress bar"}
    #!componentProp(m3.Slider)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.Slider)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.Slider)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles"}
    #!componentProp(m3.Slider)!1: {name:"thumb_color",type:"color",description:"The colour of the slider thumb."}
    #!componentProp(m3.Slider)!1: {name:"label_color",type:"color",description:"The colour of the background of the label"}
    #!componentProp(m3.Slider)!1: {name:"label_text_color",type:"color",description:"The colour of the text of the label"}
    #!componentProp(m3.Slider)!1: {name:"value",type:"number",description:"The value of the slider."}
    #!componentProp(m3.Slider)!1: {name:"min",type:"number",description:"The minimum value of the Slider."}
    #!componentProp(m3.Slider)!1: {name:"max",type:"number",description:"The maximum value of the Slider."}
    #!componentProp(m3.Slider)!1: {name:"step",type:"number",description:"The stepping interval for the Slider."}
    #!componentProp(m3.Slider)!1: {name:"show_markers",type:"boolean",description:"If True, display discrete markers on the track."}
    #!componentProp(m3.Slider)!1: {name:"margin",type:"margin",description:"The margin (pixels) of the component."}
    #!componentProp(m3.Slider)!1: {name:"track_color",type:"color",description:"The colour of the slider track."}
    #!componentProp(m3.Slider)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.Slider)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    #!componentEvent(m3.Slider)!1: {name: "change", description: "When the value of the component is changed", parameters:[]}

    progress_color = color_property(
        "anvil-m3-slider-progress", 'background', 'progress_color'
    )
    track_color = color_property(
        "anvil-m3-slider-background", 'background', 'track_color'
    )
    margin = margin_property("anvil-m3-slider")
    tooltip = tooltip_property('anvil-m3-slider')
    visible = HtmlTemplate.visible
    role = role_property('anvil-m3-slider')
    show_label = simple_prop("show_label")

    @anvil_prop
    @property
    def thumb_color(self, value=None) -> str:
        """The colour of the slider thumb."""
        if self.thumb_color:
            self.dom_nodes['anvil-m3-slider-input'].style.setProperty(
                '--anvil-m3-slider-thumb-color', theme_color_to_css(self.thumb_color)
            )
        else:
            self.dom_nodes['anvil-m3-slider-input'].style.setProperty(
                '--anvil-m3-slider-thumb-color', 'var(--anvil-m3-primary)'
            )

    @anvil_prop
    @property
    def label_color(self, value) -> str:
        """The colour of the background of the label"""
        self.label_container.style.background = theme_color_to_css(value)

    @anvil_prop
    @property
    def label_text_color(self, value) -> str:
        """The colour of the text of the label"""
        self.label_container.style.color = theme_color_to_css(value)

    @anvil_prop
    @property
    def enabled(self, value) -> bool:
        """If True, this component allows user interaction."""
        self._enabled = value
        full_slider = self.dom_nodes['anvil-m3-slider']
        input = self.dom_nodes['anvil-m3-slider-input']
        if value:
            input.removeAttribute("disabled")
            full_slider.classList.remove("anvil-m3-slider-disabled")
        else:
            input.setAttribute("disabled", " ")
            full_slider.classList.add("anvil-m3-slider-disabled")

    @anvil_prop
    @property
    def show_markers(self, value) -> bool:
        """If True, display discrete markers on the track."""
        if self._mounted:
            self._set_markers()

    @property
    def value(self):
        return float(self.dom_nodes['anvil-m3-slider-input'].value)

    @value.setter
    def value(self, value):
        if value is not None or not in_designer:
            self.dom_nodes["anvil-m3-slider-input"].value = value
            self._update_progress()

    @property
    def min(self):
        return float(self.dom_nodes['anvil-m3-slider-input'].min)

    @min.setter
    def min(self, value):
        if value is not None or not in_designer:
            if value < self.max:
                self.dom_nodes["anvil-m3-slider-input"].min = value
                self._update_progress()
        if in_designer and self._mounted:
            anvil.designer.update_component_properties(self, {"value": self.value})

    @property
    def max(self):
        return float(self.dom_nodes['anvil-m3-slider-input'].max)

    @max.setter
    def max(self, value):
        if value is not None or not in_designer:
            if value > self.min:
                self.dom_nodes["anvil-m3-slider-input"].max = value
                self._update_progress()
        if in_designer and self._mounted:
            anvil.designer.update_component_properties(self, {"value": self.value})

    @property
    def step(self):
        return self.dom_nodes['anvil-m3-slider-input'].step

    @step.setter
    def step(self, value):
        if not value:
            value = 1
        if value is not None or not in_designer:
            self.dom_nodes["anvil-m3-slider-input"].step = value
            self._update_progress()
        if in_designer and self._mounted:
            anvil.designer.update_component_properties(self, {"value": self.value})


#!defClass(m3,Slider,anvil.Component)!:
