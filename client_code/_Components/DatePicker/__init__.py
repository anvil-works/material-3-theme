import anvil
import anvil.designer
import datetime
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
from ._anvil_designer import DatePickerTemplate

_MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
]
_MONTH_ABBR = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
]


class DatePicker(DatePickerTemplate):
    def __init__(self, **properties):
        self.tag = ComponentTag()
        self._props = properties
        self._date = None
        self._pending_date = None
        self._view_year = None
        self._view_month = None
        self._is_open = False
        self._view_mode = 'day'   # 'day' | 'month' | 'year'
        self._cleanup = noop
        self._tooltip_node = None

        self._panelNode = self.dom_nodes['anvil-m3-datepicker-panel']

        self._set_designer_text_placeholder, self._start_inline_editing = (
            inline_editing(
                self,
                self.selection_field.dom_nodes['anvil-m3-label-text'],
                self._set_label,
                'label',
            )
        )

        # Make the trigger field read-only (date is set via the calendar only)
        field = self.selection_field.dom_nodes['anvil-m3-textbox']
        field.setAttribute('readonly', True)
        field.style.caretColor = 'transparent'
        field.style.cursor = 'pointer'

        # Month and year selector buttons
        self.dom_nodes['anvil-m3-datepicker-month-btn'].addEventListener(
            'click', self._toggle_month_view
        )
        self.dom_nodes['anvil-m3-datepicker-year-btn'].addEventListener(
            'click', self._toggle_year_view
        )

        # Prev / next month navigation
        self.dom_nodes['anvil-m3-datepicker-prev'].addEventListener(
            'click', self._prev_month
        )
        self.dom_nodes['anvil-m3-datepicker-next'].addEventListener(
            'click', self._next_month
        )

        # Cancel / OK action buttons
        self.dom_nodes['anvil-m3-datepicker-cancel'].addEventListener(
            'click', self._handle_cancel
        )
        self.dom_nodes['anvil-m3-datepicker-ok'].addEventListener(
            'click', self._handle_ok
        )

        # Toggle panel on trigger click
        self.dom_nodes['anvil-m3-datepicker-container'].addEventListener(
            'click', self._handle_trigger_click
        )

        self.add_event_handler('x-anvil-page-added', self._on_mount)
        self.add_event_handler('x-anvil-page-removed', self._on_cleanup)

        self.init_components(**properties)

    def _anvil_get_unset_property_values_(self):
        el = self.dom_nodes['anvil-m3-datepicker-textfield']
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

    # ── View mode ────────────────────────────────────────────────────────────

    def _set_view_mode(self, mode):
        self._view_mode = mode
        self.dom_nodes['anvil-m3-datepicker-grid'].classList.toggle(
            'anvil-m3-datepicker-hidden', mode != 'day'
        )
        self.dom_nodes['anvil-m3-datepicker-month-grid'].classList.toggle(
            'anvil-m3-datepicker-hidden', mode != 'month'
        )
        self.dom_nodes['anvil-m3-datepicker-year-grid'].classList.toggle(
            'anvil-m3-datepicker-hidden', mode != 'year'
        )
        self.dom_nodes['anvil-m3-datepicker-month-arrow'].classList.toggle(
            'anvil-m3-datepicker-arrow-up', mode == 'month'
        )
        self.dom_nodes['anvil-m3-datepicker-year-arrow'].classList.toggle(
            'anvil-m3-datepicker-arrow-up', mode == 'year'
        )
        # Prev/next and weekdays only make sense in day view
        nav_hidden = mode != 'day'
        self.dom_nodes['anvil-m3-datepicker-prev'].classList.toggle(
            'anvil-m3-datepicker-hidden', nav_hidden
        )
        self.dom_nodes['anvil-m3-datepicker-next'].classList.toggle(
            'anvil-m3-datepicker-hidden', nav_hidden
        )
        self.dom_nodes['anvil-m3-datepicker-weekdays'].classList.toggle(
            'anvil-m3-datepicker-hidden', nav_hidden
        )
        self.dom_nodes['anvil-m3-datepicker-footer'].classList.toggle(
            'anvil-m3-datepicker-hidden', nav_hidden
        )

    def _toggle_month_view(self, event):
        event.stopPropagation()
        new_mode = 'day' if self._view_mode == 'month' else 'month'
        self._set_view_mode(new_mode)
        if new_mode == 'month':
            self._render_month_grid()

    def _toggle_year_view(self, event):
        event.stopPropagation()
        new_mode = 'day' if self._view_mode == 'year' else 'year'
        self._set_view_mode(new_mode)
        if new_mode == 'year':
            self._render_year_grid()

    # ── Calendar Rendering ──────────────────────────────────────────────────

    def _days_in_month(self, year, month):
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        return (next_month - datetime.date(year, month, 1)).days

    def _render_calendar(self):
        self.dom_nodes['anvil-m3-datepicker-month-label'].textContent = (
            _MONTH_NAMES[self._view_month - 1]
        )
        self.dom_nodes['anvil-m3-datepicker-year-label'].textContent = (
            str(self._view_year)
        )

        grid = self.dom_nodes['anvil-m3-datepicker-grid']
        grid.innerHTML = ''

        today = datetime.date.today()
        first = datetime.date(self._view_year, self._view_month, 1)
        # weekday(): 0=Mon … 6=Sun → shift so Sunday=0
        start_offset = (first.weekday() + 1) % 7
        days = self._days_in_month(self._view_year, self._view_month)
        min_date = self._props.get('min_date')
        max_date = self._props.get('max_date')

        total_cells = ((start_offset + days + 6) // 7) * 7  # minimum rows × 7
        for i in range(total_cells):
            day_num = i - start_offset + 1
            cell = document.createElement('button')
            cell.setAttribute('type', 'button')
            cell.className = 'anvil-m3-datepicker-day'

            if day_num < 1:
                # Trailing days of previous month
                if self._view_month == 1:
                    prev_year, prev_month = self._view_year - 1, 12
                else:
                    prev_year, prev_month = self._view_year, self._view_month - 1
                cell.textContent = str(self._days_in_month(prev_year, prev_month) + day_num)
                cell.disabled = True
                cell.classList.add('anvil-m3-datepicker-day-outside')
            elif day_num > days:
                # Leading days of next month
                cell.textContent = str(day_num - days)
                cell.disabled = True
                cell.classList.add('anvil-m3-datepicker-day-outside')
            else:
                d = datetime.date(self._view_year, self._view_month, day_num)
                cell.textContent = str(day_num)

                if d == today:
                    cell.classList.add('anvil-m3-datepicker-day-today')
                if self._pending_date and d == self._pending_date:
                    cell.classList.add('anvil-m3-datepicker-day-selected')

                if (min_date and d < min_date) or (max_date and d > max_date):
                    cell.disabled = True
                    cell.classList.add('anvil-m3-datepicker-day-disabled')
                else:
                    cell.addEventListener('click', self._make_day_handler(d))

            grid.appendChild(cell)

    def _make_day_handler(self, d):
        def handler(event):
            event.stopPropagation()
            self._pending_date = d
            self._render_calendar()
        return handler

    def _render_month_grid(self):
        grid = self.dom_nodes['anvil-m3-datepicker-month-grid']
        grid.innerHTML = ''
        for i, name in enumerate(_MONTH_NAMES):
            month_num = i + 1
            cell = document.createElement('button')
            cell.setAttribute('type', 'button')
            cell.className = 'anvil-m3-datepicker-month-cell'
            cell.textContent = name
            if month_num == self._view_month:
                cell.classList.add('anvil-m3-datepicker-month-selected')
            cell.addEventListener('click', self._make_month_handler(month_num))
            grid.appendChild(cell)

        selected = grid.querySelector('.anvil-m3-datepicker-month-selected')
        if selected:
            selected.scrollIntoView({'block': 'center'})

    def _make_month_handler(self, month_num):
        def handler(event):
            event.stopPropagation()
            self._view_month = month_num
            self._set_view_mode('day')
            self._render_calendar()
        return handler

    def _render_year_grid(self):
        grid = self.dom_nodes['anvil-m3-datepicker-year-grid']
        grid.innerHTML = ''
        base = self._view_year or datetime.date.today().year
        for yr in range(base - 100, base + 101):
            cell = document.createElement('button')
            cell.setAttribute('type', 'button')
            cell.className = 'anvil-m3-datepicker-year-cell'
            cell.textContent = str(yr)
            if yr == base:
                cell.classList.add('anvil-m3-datepicker-year-selected')
            cell.addEventListener('click', self._make_year_handler(yr))
            grid.appendChild(cell)

        selected = grid.querySelector('.anvil-m3-datepicker-year-selected')
        if selected:
            selected.scrollIntoView({'block': 'center'})

    def _make_year_handler(self, year):
        def handler(event):
            event.stopPropagation()
            self._view_year = year
            self._set_view_mode('day')
            self._render_calendar()
        return handler

    def _prev_month(self, event):
        event.stopPropagation()
        if self._view_month == 1:
            self._view_month, self._view_year = 12, self._view_year - 1
        else:
            self._view_month -= 1
        self._render_calendar()

    def _next_month(self, event):
        event.stopPropagation()
        if self._view_month == 12:
            self._view_month, self._view_year = 1, self._view_year + 1
        else:
            self._view_month += 1
        self._render_calendar()

    def _handle_ok(self, event):
        event.stopPropagation()
        if self._pending_date != self._date:
            self.date = self._pending_date
            self.raise_event('change')
        self._close_panel()

    def _handle_cancel(self, event):
        event.stopPropagation()
        self._close_panel()

    def _open_panel(self):
        ref = self._date or datetime.date.today()
        self._view_year = ref.year
        self._view_month = ref.month
        self._pending_date = self._date
        self._set_view_mode('day')
        self._render_calendar()
        self._panelNode.classList.remove('anvil-m3-datepicker-hidden')
        self._is_open = True

    def _close_panel(self):
        self._panelNode.classList.add('anvil-m3-datepicker-hidden')
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
        container = self.dom_nodes['anvil-m3-datepicker-container']
        if not container.contains(event.target) and not self._panelNode.contains(event.target):
            self._close_panel()

    def form_show(self, **event_args):
        self._set_designer_text_placeholder()

    # ── Designer Interactions ────────────────────────────────────────────────

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

    # ── Date formatting ──────────────────────────────────────────────────────

    def _format_date(self, value):
        fmt = self._props.get('format')
        if fmt:
            return value.strftime(fmt)
        return f"{_MONTH_ABBR[value.month - 1]} {value.day}, {value.year}"

    # ── Properties ──────────────────────────────────────────────────────────

    visible = HtmlTemplate.visible
    margin = margin_property('anvil-m3-datepicker-textfield')

    @anvil_prop
    @property
    def date(self, value) -> object:
        """The selected date as a Python datetime.date object."""
        self._date = value
        if value is not None:
            self.selection_field.text = self._format_date(value)
        else:
            self.selection_field.text = ''

    @anvil_prop
    @property
    def format(self, value) -> str:
        """A strftime format string for displaying the selected date (e.g. "%d/%m/%Y"). Leave blank for the default "Jan 4, 2026" format."""
        if self._date is not None:
            self.selection_field.text = self._format_date(self._date)

    @anvil_prop
    @property
    def min_date(self, value) -> object:
        """The minimum selectable date."""
        if self._is_open:
            self._render_calendar()

    @anvil_prop
    @property
    def max_date(self, value) -> object:
        """The maximum selectable date."""
        if self._is_open:
            self._render_calendar()

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
        """The text to be displayed when no date is selected."""
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
        """If True, the displayed date text will be bold."""
        self.selection_field.display_bold = value

    @anvil_prop
    @property
    def display_italic(self, value) -> bool:
        """If True, the displayed date text will be italic."""
        self.selection_field.display_italic = value

    @anvil_prop
    @property
    def display_underline(self, value) -> bool:
        """If True, the displayed date text will be underlined."""
        self.selection_field.display_underline = value

    @anvil_prop
    @property
    def display_font_family(self, value) -> str:
        """The font family to use for the displayed date text."""
        self.selection_field.display_font_family = value

    @anvil_prop
    @property
    def display_text_color(self, value) -> str:
        """The colour of the displayed date text."""
        self.selection_field.display_text_color = value

    @anvil_prop
    @property
    def display_font_size(self, value) -> float:
        """The font size of the displayed date text."""
        self.selection_field.display_font_size = value

    @anvil_prop
    @property
    def tooltip(self, value) -> str:
        """The text to display when the mouse is hovered over this component."""
        self.selection_field.tooltip = value

    #!componentProp(m3.DatePicker)!1: {name:"align",type:"enum",options:["left","center","right","full"],description:"The position of this component in the available space."}
    #!componentProp(m3.DatePicker)!1: {name:"appearance",type:"enum",options:["filled","outlined"],description:"A predefined style for this component."}
    #!componentProp(m3.DatePicker)!1: {name:"visible",type:"boolean",description:"If True, the component will be displayed."}
    #!componentProp(m3.DatePicker)!1: {name:"enabled",type:"boolean",description:"If True, this component allows user interaction."}
    #!componentProp(m3.DatePicker)!1: {name:"error",type:"boolean",description:"If True, this component is in an error state."}
    #!componentProp(m3.DatePicker)!1: {name:"role",type:"themeRole",description:"A style for this component defined in CSS and added to Roles."}
    #!componentProp(m3.DatePicker)!1: {name:"label",type:"string",description:"The label text of the component."}
    #!componentProp(m3.DatePicker)!1: {name:"placeholder",type:"string",description:"The text to be displayed when no date is selected."}
    #!componentProp(m3.DatePicker)!1: {name:"date",type:"object",description:"The selected date as a Python datetime.date object."}
    #!componentProp(m3.DatePicker)!1: {name:"format",type:"string",description:"A strftime format string for displaying the selected date."}
    #!componentProp(m3.DatePicker)!1: {name:"min_date",type:"object",description:"The minimum selectable date."}
    #!componentProp(m3.DatePicker)!1: {name:"max_date",type:"object",description:"The maximum selectable date."}
    #!componentProp(m3.DatePicker)!1: {name:"supporting_text",type:"string",description:"The supporting text displayed underneath this component."}
    #!componentProp(m3.DatePicker)!1: {name:"label_color",type:"color",description:"The colour of the label text on the component."}
    #!componentProp(m3.DatePicker)!1: {name:"label_font_family",type:"string",description:"The font family to use for the label on this component."}
    #!componentProp(m3.DatePicker)!1: {name:"label_font_size",type:"number",description:"The font size of the label text on this component."}
    #!componentProp(m3.DatePicker)!1: {name:"label_underline",type:"boolean",description:"If True, the label text will be underlined."}
    #!componentProp(m3.DatePicker)!1: {name:"label_italic",type:"boolean",description:"If True, the label text will be italic."}
    #!componentProp(m3.DatePicker)!1: {name:"label_bold",type:"boolean",description:"If True, the label text will be bold."}
    #!componentProp(m3.DatePicker)!1: {name:"display_text_color",type:"color",description:"The colour of the displayed date text."}
    #!componentProp(m3.DatePicker)!1: {name:"display_font_family",type:"string",description:"The font family to use for the displayed date text."}
    #!componentProp(m3.DatePicker)!1: {name:"display_font_size",type:"number",description:"The font size of the displayed date text."}
    #!componentProp(m3.DatePicker)!1: {name:"display_underline",type:"boolean",description:"If True, the displayed date text will be underlined."}
    #!componentProp(m3.DatePicker)!1: {name:"display_italic",type:"boolean",description:"If True, the displayed date text will be italic."}
    #!componentProp(m3.DatePicker)!1: {name:"display_bold",type:"boolean",description:"If True, the displayed date text will be bold."}
    #!componentProp(m3.DatePicker)!1: {name:"background_color",type:"color",description:"The colour of the background of this component."}
    #!componentProp(m3.DatePicker)!1: {name:"border_color",type:"color",description:"The colour of the border of this component."}
    #!componentProp(m3.DatePicker)!1: {name:"supporting_text_color",type:"color",description:"The colour of the supporting text."}
    #!componentProp(m3.DatePicker)!1: {name:"supporting_text_font_family",type:"string",description:"The font family to use for the supporting text."}
    #!componentProp(m3.DatePicker)!1: {name:"supporting_text_font_size",type:"number",description:"The font size of the supporting text."}
    #!componentProp(m3.DatePicker)!1: {name:"margin",type:"margin",description:"The margin of this component."}
    #!componentProp(m3.DatePicker)!1: {name:"tooltip",type:"string",description:"The text to display when the mouse is hovered over this component."}
    #!componentProp(m3.DatePicker)!1: {name:"tag",type:"object",description:"Use this property to store any extra data for the component."}

    #!componentEvent(m3.DatePicker)!1: {name:"change",description:"When a date is selected.",parameters:[]}


#!defClass(m3,DatePicker,anvil.Component)!:
