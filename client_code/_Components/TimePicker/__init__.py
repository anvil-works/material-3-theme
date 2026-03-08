import anvil
import anvil.designer
import datetime
import math
from anvil import HtmlTemplate
from anvil.js import get_dom_node
from anvil.js.window import document

from ..._utils import fui, noop
from ..._utils.properties import (
    ComponentTag,
    anvil_prop,
    get_unset_margin,
    get_unset_value,
    inline_editing,
    margin_property,
)
from ._anvil_designer import TimePickerTemplate

_SVG_NS = 'http://www.w3.org/2000/svg'


class TimePicker(TimePickerTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._time = None
        self._pending_hour = 12     # 1-12 (12hr) or 0-23 (24hr)
        self._pending_minute = 0    # 0-59
        self._pending_is_am = True  # 12hr only
        self._editing = 'hour'      # 'hour' | 'minute'
        self._input_mode = False    # False = dial, True = text inputs
        self._is_open = False
        self._cleanup = noop
        self._tooltip_node = None

        self._panelNode = self.dom_nodes['anvil-m3-timepicker-panel']

        self._set_designer_text_placeholder, self._start_inline_editing = (
            inline_editing(
                self,
                self.selection_field.dom_nodes['anvil-m3-label-text'],
                self._set_label,
                'label',
            )
        )

        # Make the trigger field read-only
        field = self.selection_field.dom_nodes['anvil-m3-textbox']
        field.setAttribute('readonly', True)
        field.style.caretColor = 'transparent'
        field.style.cursor = 'pointer'

        # Time chip focus/input — editing mode follows focused chip
        self.dom_nodes['anvil-m3-timepicker-hour-chip'].addEventListener(
            'focus', self._handle_hour_focus
        )
        self.dom_nodes['anvil-m3-timepicker-minute-chip'].addEventListener(
            'focus', self._handle_minute_focus
        )
        self.dom_nodes['anvil-m3-timepicker-hour-chip'].addEventListener(
            'input', self._handle_hour_input
        )
        self.dom_nodes['anvil-m3-timepicker-minute-chip'].addEventListener(
            'input', self._handle_minute_input
        )

        # AM/PM buttons
        self.dom_nodes['anvil-m3-timepicker-am-btn'].addEventListener(
            'click', self._handle_am_click
        )
        self.dom_nodes['anvil-m3-timepicker-pm-btn'].addEventListener(
            'click', self._handle_pm_click
        )

        # Clock dial click
        self.dom_nodes['anvil-m3-timepicker-svg'].addEventListener(
            'click', self._handle_dial_click
        )

        # Toggle panel on trigger click
        self.dom_nodes['anvil-m3-timepicker-container'].addEventListener(
            'click', self._handle_trigger_click
        )

        self.add_event_handler('x-anvil-page-added', self._on_mount)
        self.add_event_handler('x-anvil-page-removed', self._on_cleanup)

        self.init_components(**properties)

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes['anvil-m3-timepicker-textfield']
        m = get_unset_margin(el, self.margin)
        lfs = get_unset_value(
            self.selection_field.dom_nodes['anvil-m3-label-text'],
            'fontSize',
            self.label_font_size,
        )
        stfs = get_unset_value(
            self.selection_field.dom_nodes['anvil-m3-supporting-text'],
            'fontSize',
            self.supporting_text_font_size,
        )
        dfs = get_unset_value(
            self.selection_field.dom_nodes['anvil-m3-textbox'],
            'fontSize',
            self.display_font_size,
        )
        return {
            'label_font_size': lfs,
            'supporting_text_font_size': stfs,
            'display_font_size': dfs,
            'margin': m,
        }

    # ── Mount / Cleanup ──────────────────────────────────────────────────────

    def _on_mount(self, **event_args):
        document.addEventListener('click', self._handle_outside_click)
        document.body.append(self._panelNode)
        self._cleanup = fui.auto_update(
            get_dom_node(self.selection_field),
            self._panelNode,
            placement='bottom-start',
            offset=4,
        )

    def _on_cleanup(self, **event_args):
        document.removeEventListener('click', self._handle_outside_click)
        self._cleanup()
        self._panelNode.remove()
        self._cleanup = noop

    # ── Panel Control ────────────────────────────────────────────────────────

    def _open_panel(self):
        self._init_pending()
        self._editing = 'hour'
        self._input_mode = False
        self.dom_nodes['anvil-m3-timepicker-dial'].classList.remove('anvil-m3-timepicker-hidden')
        self.mode_toggle_btn.icon = 'mi:keyboard'
        self._update_display()
        self._render_dial()
        self._panelNode.classList.remove('anvil-m3-timepicker-hidden')
        self._is_open = True

    def _close_panel(self):
        self._panelNode.classList.add('anvil-m3-timepicker-hidden')
        self._is_open = False

    def _handle_trigger_click(self, event):
        if not self._props.get('enabled', True):
            return
        if self._is_open:
            self._close_panel()
        else:
            self._open_panel()

    def _handle_outside_click(self, event):
        if not self._is_open:
            return
        container = self.dom_nodes['anvil-m3-timepicker-container']
        if not container.contains(event.target) and not self._panelNode.contains(event.target):
            self._close_panel()

    # ── Pending State ────────────────────────────────────────────────────────

    def _init_pending(self):
        t = self._time or datetime.datetime.now().time()
        is_24 = self._props.get('hour_24', False)
        if is_24:
            self._pending_hour = t.hour
        else:
            self._pending_is_am = t.hour < 12
            self._pending_hour = t.hour % 12 or 12
        self._pending_minute = t.minute

    # ── Display ──────────────────────────────────────────────────────────────

    def _update_display(self):
        is_24 = self._props.get('hour_24', False)

        hour_chip = self.dom_nodes['anvil-m3-timepicker-hour-chip']
        minute_chip = self.dom_nodes['anvil-m3-timepicker-minute-chip']

        # Only set value when the chip isn't actively being typed into
        if document.activeElement != hour_chip:
            hour_chip.value = f'{self._pending_hour:02d}' if is_24 else str(self._pending_hour)
        if document.activeElement != minute_chip:
            minute_chip.value = f'{self._pending_minute:02d}'

        hour_chip.classList.toggle('anvil-m3-timepicker-chip-active', self._editing == 'hour')
        minute_chip.classList.toggle('anvil-m3-timepicker-chip-active', self._editing == 'minute')

        self.dom_nodes['anvil-m3-timepicker-am-btn'].classList.toggle(
            'anvil-m3-timepicker-ampm-selected', self._pending_is_am
        )
        self.dom_nodes['anvil-m3-timepicker-pm-btn'].classList.toggle(
            'anvil-m3-timepicker-ampm-selected', not self._pending_is_am
        )
        self.dom_nodes['anvil-m3-timepicker-ampm'].style.display = 'none' if is_24 else ''

    # ── Clock Dial ───────────────────────────────────────────────────────────

    def _svg_el(self, tag, **attrs):
        el = document.createElementNS(_SVG_NS, tag)
        for k, v in attrs.items():
            el.setAttribute(k.replace('_', '-'), str(v))
        return el

    def _render_dial(self):
        svg = self.dom_nodes['anvil-m3-timepicker-svg']
        svg.innerHTML = ''

        cx, cy = 120, 120
        face_r = 120
        num_r = 88        # outer ring radius
        num_r_inner = 56  # inner ring radius (24hr)
        num_cr = 20       # number circle radius
        is_24 = self._props.get('hour_24', False)

        # 1. Background circle
        bg = self._svg_el('circle', cx=cx, cy=cy, r=face_r)
        bg.setAttribute('class', 'anvil-m3-timepicker-clock-face')
        svg.appendChild(bg)

        # Calculate hand endpoint
        if self._editing == 'hour':
            h_angle = ((self._pending_hour % 12) * 30 - 90) * math.pi / 180
            if is_24:
                is_inner = (self._pending_hour == 0 or self._pending_hour >= 13)
                hand_r = num_r_inner if is_inner else num_r
            else:
                hand_r = num_r
            hand_angle = h_angle
        else:
            hand_angle = (self._pending_minute * 6 - 90) * math.pi / 180
            hand_r = num_r

        hand_x = cx + hand_r * math.cos(hand_angle)
        hand_y = cy + hand_r * math.sin(hand_angle)

        # 2. Hand line
        line = self._svg_el('line', x1=cx, y1=cy, x2=hand_x, y2=hand_y)
        line.setAttribute('class', 'anvil-m3-timepicker-hand')
        svg.appendChild(line)

        # 3. Handle circle at tip (covered by selected number circle for labeled values)
        handle = self._svg_el('circle', cx=hand_x, cy=hand_y, r=num_cr)
        handle.setAttribute('class', 'anvil-m3-timepicker-hand-tip')
        svg.appendChild(handle)

        # 4 & 5. Numbers
        if self._editing == 'hour':
            if is_24:
                numbers_outer = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                numbers_inner = [0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            else:
                numbers_outer = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                numbers_inner = []
            selected = self._pending_hour
        else:
            numbers_outer = [i * 5 for i in range(12)]  # 0, 5, 10, ..., 55
            numbers_inner = []
            selected = self._pending_minute

        # Outer ring
        for v in numbers_outer:
            if self._editing == 'hour':
                a = ((v % 12) * 30 - 90) * math.pi / 180
            else:
                a = (v * 6 - 90) * math.pi / 180
            x = cx + num_r * math.cos(a)
            y = cy + num_r * math.sin(a)
            is_sel = (v == selected)

            circ = self._svg_el('circle', cx=x, cy=y, r=num_cr)
            circ.setAttribute(
                'class',
                'anvil-m3-timepicker-num-circle' +
                (' anvil-m3-timepicker-num-selected' if is_sel else '')
            )
            svg.appendChild(circ)

            txt = self._svg_el('text', x=x, y=y)
            txt.setAttribute(
                'class',
                'anvil-m3-timepicker-num-text' +
                (' anvil-m3-timepicker-num-text-selected' if is_sel else '')
            )
            txt.setAttribute('text-anchor', 'middle')
            txt.setAttribute('dominant-baseline', 'central')
            txt.textContent = f'{v:02d}' if self._editing == 'minute' else str(v)
            svg.appendChild(txt)

        # Inner ring (24hr hour mode only)
        for v in numbers_inner:
            a = ((v % 12) * 30 - 90) * math.pi / 180
            x = cx + num_r_inner * math.cos(a)
            y = cy + num_r_inner * math.sin(a)
            is_sel = (v == selected)

            circ = self._svg_el('circle', cx=x, cy=y, r=num_cr)
            circ.setAttribute(
                'class',
                'anvil-m3-timepicker-num-circle' +
                (' anvil-m3-timepicker-num-selected' if is_sel else '')
            )
            svg.appendChild(circ)

            txt = self._svg_el('text', x=x, y=y)
            txt.setAttribute(
                'class',
                'anvil-m3-timepicker-num-text anvil-m3-timepicker-num-text-inner' +
                (' anvil-m3-timepicker-num-text-selected' if is_sel else '')
            )
            txt.setAttribute('text-anchor', 'middle')
            txt.setAttribute('dominant-baseline', 'central')
            txt.textContent = str(v)
            svg.appendChild(txt)

        # 6. Center dot (on top)
        center = self._svg_el('circle', cx=cx, cy=cy, r=6)
        center.setAttribute('class', 'anvil-m3-timepicker-center-dot')
        svg.appendChild(center)

    def _handle_dial_click(self, event):
        event.stopPropagation()
        svg = self.dom_nodes['anvil-m3-timepicker-svg']
        rect = svg.getBoundingClientRect()
        # Map click to viewBox coordinates
        x = (event.clientX - rect.left) / rect.width * 240
        y = (event.clientY - rect.top) / rect.height * 240
        dx = x - 120
        dy = y - 120
        angle = (math.atan2(dy, dx) * 180 / math.pi + 90) % 360
        dist = math.sqrt(dx * dx + dy * dy)

        is_24 = self._props.get('hour_24', False)

        if self._editing == 'hour':
            hour_idx = round(angle / 30) % 12
            if is_24:
                threshold = (88 + 56) / 2  # 72
                if dist > threshold:
                    # Outer ring: 12, 1-11
                    self._pending_hour = hour_idx or 12
                else:
                    # Inner ring: 0, 13-23
                    self._pending_hour = 0 if hour_idx == 0 else hour_idx + 12
            else:
                self._pending_hour = hour_idx or 12
            # Auto-switch to minute editing
            self._editing = 'minute'
        else:
            self._pending_minute = round(angle / 6) % 60

        self._update_display()
        self._render_dial()

    # ── Display Chip Focus ───────────────────────────────────────────────────

    def _handle_hour_focus(self, event):
        self._editing = 'hour'
        self._update_display()
        if not self._input_mode:
            self._render_dial()

    def _handle_minute_focus(self, event):
        self._editing = 'minute'
        self._update_display()
        if not self._input_mode:
            self._render_dial()

    # ── AM/PM ────────────────────────────────────────────────────────────────

    def _handle_am_click(self, event):
        event.stopPropagation()
        self._pending_is_am = True
        self._update_display()

    def _handle_pm_click(self, event):
        event.stopPropagation()
        self._pending_is_am = False
        self._update_display()

    # ── Mode Toggle (show/hide dial) ─────────────────────────────────────────

    def _toggle_mode(self, **event_args):
        self._input_mode = not self._input_mode
        dial = self.dom_nodes['anvil-m3-timepicker-dial']
        dial.classList.toggle('anvil-m3-timepicker-hidden', self._input_mode)
        self.mode_toggle_btn.icon = 'mi:schedule' if self._input_mode else 'mi:keyboard'

    # ── Time Chip Input Handlers ─────────────────────────────────────────────

    def _handle_hour_input(self, event):
        is_24 = self._props.get('hour_24', False)
        try:
            h = int(self.dom_nodes['anvil-m3-timepicker-hour-chip'].value)
            self._pending_hour = max(0, min(23, h)) if is_24 else max(1, min(12, h))
        except (ValueError, TypeError):
            pass
        if not self._input_mode:
            self._render_dial()

    def _handle_minute_input(self, event):
        try:
            m = int(self.dom_nodes['anvil-m3-timepicker-minute-chip'].value)
            self._pending_minute = max(0, min(59, m))
        except (ValueError, TypeError):
            pass
        if not self._input_mode:
            self._render_dial()

    # ── OK / Cancel ──────────────────────────────────────────────────────────

    def _handle_ok(self, **event_args):
        is_24 = self._props.get('hour_24', False)
        # Sync chip input values into pending state (in case user typed without blurring)
        try:
            h = int(self.dom_nodes['anvil-m3-timepicker-hour-chip'].value)
            self._pending_hour = max(0, min(23, h)) if is_24 else max(1, min(12, h))
        except (ValueError, TypeError):
            pass
        try:
            m = int(self.dom_nodes['anvil-m3-timepicker-minute-chip'].value)
            self._pending_minute = max(0, min(59, m))
        except (ValueError, TypeError):
            pass
        hour = self._pending_hour
        if not is_24:
            hour = hour % 12          # 12 AM → 0
            if not self._pending_is_am:
                hour += 12            # 1 PM → 13, 12 PM → 12
        self._time = datetime.time(hour, self._pending_minute)
        self.selection_field.text = self._format_time(self._time)
        self._close_panel()
        self.raise_event('change')

    def _handle_cancel(self, **event_args):
        self._close_panel()

    # ── Time Formatting ──────────────────────────────────────────────────────

    def _format_time(self, value):
        fmt = self._props.get('format')
        if fmt:
            return value.strftime(fmt)
        if self._props.get('hour_24', False):
            return f'{value.hour:02d}:{value.minute:02d}'
        h = value.hour % 12 or 12
        ampm = 'AM' if value.hour < 12 else 'PM'
        return f'{h}:{value.minute:02d} {ampm}'

    # ── Designer ─────────────────────────────────────────────────────────────

    def form_show(self, **event_args):
        self._set_designer_text_placeholder()

    def _anvil_get_interactions_(self):
        return [
            {
                'type': 'whole_component',
                'title': 'Edit Label',
                'icon': 'edit',
                'default': True,
                'callbacks': {'execute': self._start_inline_editing},
            }
        ]

    # ── Properties ──────────────────────────────────────────────────────────

    visible = HtmlTemplate.visible
    margin = margin_property('anvil-m3-timepicker-textfield')

    @anvil_prop
    @property
    def time(self, value) -> object:
        """The selected time as a Python datetime.time object."""
        self._time = value
        if value is not None:
            self.selection_field.text = self._format_time(value)
        else:
            self.selection_field.text = ''

    @anvil_prop
    @property
    def format(self, value) -> str:
        """A strftime format string for displaying the selected time. Leave blank for the default format."""
        if self._time is not None:
            self.selection_field.text = self._format_time(self._time)

    @anvil_prop
    @property
    def hour_24(self, value) -> bool:
        """If True, the time picker uses 24-hour format."""
        if self._time is not None:
            self.selection_field.text = self._format_time(self._time)
        if self._is_open:
            self._init_pending()
            self._update_display()
            self._render_dial()

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
    def placeholder(self, value) -> str:
        """The text to be displayed when no time is selected."""
        self.selection_field.placeholder = value

    @anvil_prop
    @property
    def appearance(self, value) -> str:
        """A predefined style for this component."""
        self.selection_field.appearance = value

    @anvil_prop(default_value=True)
    @property
    def enabled(self, value) -> bool:
        """If True, this component allows user interaction."""
        self.selection_field.enabled = value

    @anvil_prop
    @property
    def error(self, value) -> bool:
        """If True, this component is in an error state."""
        if value:
            self.selection_field.dom_nodes['anvil-m3-textinput'].classList.add(
                'anvil-m3-textinput-error'
            )
        else:
            self.selection_field.dom_nodes['anvil-m3-textinput'].classList.remove(
                'anvil-m3-textinput-error'
            )

    @anvil_prop
    @property
    def align(self, value) -> str:
        """The position of this component in the available space."""
        self.selection_field.align = value

    @anvil_prop
    @property
    def role(self, value) -> str:
        """A style for this component defined in CSS and added to Roles."""
        self.selection_field.role = value

    @anvil_prop
    @property
    def background_color(self, value) -> str:
        """The colour of the background of this component."""
        self.selection_field.background_color = value

    @anvil_prop
    @property
    def border_color(self, value) -> str:
        """The colour of the border of this component."""
        self.selection_field.border_color = value

    @anvil_prop
    @property
    def supporting_text(self, value) -> str:
        """The supporting text displayed underneath this component."""
        self.selection_field.supporting_text = value

    @anvil_prop
    @property
    def supporting_text_color(self, value) -> str:
        """The colour of the supporting text."""
        self.selection_field.subcontent_color = value

    @anvil_prop
    @property
    def supporting_text_font_size(self, value) -> float:
        """The font size of the supporting text."""
        self.selection_field.subcontent_font_size = value

    @anvil_prop
    @property
    def supporting_text_font_family(self, value) -> str:
        """The font family to use for the supporting text."""
        self.selection_field.subcontent_font_family = value

    @anvil_prop
    @property
    def label_color(self, value) -> str:
        """The colour of the label text on the component."""
        self.selection_field.label_color = value

    @anvil_prop
    @property
    def label_bold(self, value) -> bool:
        """If True, the label text will be bold."""
        self.selection_field.label_bold = value

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
    def label_font_size(self, value) -> float:
        """The font size of the label text."""
        self.selection_field.label_font_size = value

    @anvil_prop
    @property
    def label_font_family(self, value) -> str:
        """The font family to use for the label."""
        self.selection_field.label_font_family = value

    @anvil_prop
    @property
    def display_bold(self, value) -> bool:
        """If True, the displayed time text will be bold."""
        self.selection_field.display_bold = value

    @anvil_prop
    @property
    def display_italic(self, value) -> bool:
        """If True, the displayed time text will be italic."""
        self.selection_field.display_italic = value

    @anvil_prop
    @property
    def display_underline(self, value) -> bool:
        """If True, the displayed time text will be underlined."""
        self.selection_field.display_underline = value

    @anvil_prop
    @property
    def display_font_family(self, value) -> str:
        """The font family to use for the displayed time text."""
        self.selection_field.display_font_family = value

    @anvil_prop
    @property
    def display_text_color(self, value) -> str:
        """The colour of the displayed time text."""
        self.selection_field.display_text_color = value

    @anvil_prop
    @property
    def display_font_size(self, value) -> float:
        """The font size of the displayed time text."""
        self.selection_field.display_font_size = value

    @anvil_prop
    @property
    def tooltip(self, value) -> str:
        """The text to display when the mouse is hovered over this component."""
        self.selection_field.tooltip = value

    #!componentProp(m3.TimePicker)!1: {name:"align",type:"enum",options:["left","center","right"],description:"The position of this component in the available space."}
    #!componentProp(m3.TimePicker)!1: {name:"appearance",type:"enum",options:["filled","outlined"],description:"A predefined style for this component."}
    #!componentProp(m3.TimePicker)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.TimePicker)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.TimePicker)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
    #!componentProp(m3.TimePicker)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.TimePicker)!1: {name:"label",type:"string",description:"The label text of the component."}
    #!componentProp(m3.TimePicker)!1: {name:"placeholder",type:"string",description:"The text to be displayed when no time is selected."}
    #!componentProp(m3.TimePicker)!1: {name:"time",type:"object",description:"The selected time as a Python datetime.time object."}
    #!componentProp(m3.TimePicker)!1: {name:"format",type:"string",description:"A strftime format string for displaying the selected time."}
    #!componentProp(m3.TimePicker)!1: {name:"hour_24",type:"boolean",description:"If True, the time picker uses 24-hour format."}
    #!componentProp(m3.TimePicker)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed underneath this component."}
    #!componentProp(m3.TimePicker)!1: {name:"label_color",type:"color",description:"The colour of the label text on the component."}
    #!componentProp(m3.TimePicker)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label on this component."}
    #!componentProp(m3.TimePicker)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
    #!componentProp(m3.TimePicker)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
    #!componentProp(m3.TimePicker)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
    #!componentProp(m3.TimePicker)!1: {name:"label_bold",type:"boolean",description:"If True, the label text will be bold."}
    #!componentProp(m3.TimePicker)!1: {name:"display_text_color",type:"color",description:"The colour of the displayed time text."}
    #!componentProp(m3.TimePicker)!1: {name:"display_font_family",type:"string",description:"The font family to use for the displayed time text."}
    #!componentProp(m3.TimePicker)!1: {name:"display_font_size",type:"number",description:"The font size of the displayed time text."}
    #!componentProp(m3.TimePicker)!1: {name:"display_underline",type:"boolean",description:"If True, the displayed time text will be underlined."}
    #!componentProp(m3.TimePicker)!1: {name:"display_italic",type:"boolean",description:"If True, the displayed time text will be italic."}
    #!componentProp(m3.TimePicker)!1: {name:"display_bold",type:"boolean",description:"If True, the displayed time text will be bold."}
    #!componentProp(m3.TimePicker)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
    #!componentProp(m3.TimePicker)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
    #!componentProp(m3.TimePicker)!1: {name:"supporting_text_color",type:"color",description:"The colour of the supporting text."}
    #!componentProp(m3.TimePicker)!1: {name:"supporting_text_font_family",type:"string",description:"The font family to use for the supporting text."}
    #!componentProp(m3.TimePicker)!1: {name:"supporting_text_font_size",type:"number",description:"The font size of the supporting text."}
    #!componentProp(m3.TimePicker)!1: {name:"margin",type:"margin",description:"The margin of this component."}
    #!componentProp(m3.TimePicker)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.TimePicker)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    #!componentEvent(m3.TimePicker)!1: {name:"change",description:"When a time is selected.",parameters:[]}


#!defClass(m3,TimePicker,anvil.Component)!:
