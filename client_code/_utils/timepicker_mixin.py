import datetime
import math
from anvil.js.window import document

_SVG_NS = 'http://www.w3.org/2000/svg'


class TimePickerMixin:
    """Shared clock-dial + time-chip logic for TimePicker and DatePicker (pick_time mode).

    Call _tp_setup() in __init__ to wire up DOM nodes and register event listeners.
    All state is prefixed with _tp_ to avoid collisions with the host class.
    """

    def _tp_setup(self, svg_node, hour_chip, minute_chip, am_btn, pm_btn, ampm_container):
        """Wire up DOM node references, initialise state, and register event listeners."""
        self._tp_svg = svg_node
        self._tp_hour_chip = hour_chip
        self._tp_minute_chip = minute_chip
        self._tp_am_btn = am_btn
        self._tp_pm_btn = pm_btn
        self._tp_ampm_container = ampm_container

        self._tp_pending_hour = 12
        self._tp_pending_minute = 0
        self._tp_pending_is_am = True
        self._tp_editing = 'hour'

        hour_chip.addEventListener('focus', self._tp_handle_hour_focus)
        minute_chip.addEventListener('focus', self._tp_handle_minute_focus)
        hour_chip.addEventListener('input', self._tp_handle_hour_input)
        minute_chip.addEventListener('input', self._tp_handle_minute_input)
        am_btn.addEventListener('click', self._tp_handle_am_click)
        pm_btn.addEventListener('click', self._tp_handle_pm_click)
        svg_node.addEventListener('click', self._tp_handle_dial_click)

    def _tp_is_24(self):
        return self._props.get('hour_24', False)

    def _tp_init_pending(self, t=None):
        """Initialise pending time state from a datetime.time, or now() if None."""
        if t is None:
            t = datetime.datetime.now().time()
        is_24 = self._tp_is_24()
        if is_24:
            self._tp_pending_hour = t.hour
        else:
            self._tp_pending_is_am = t.hour < 12
            self._tp_pending_hour = t.hour % 12 or 12
        self._tp_pending_minute = t.minute

    # ── SVG helpers ──────────────────────────────────────────────────────────

    def _svg_el(self, tag, **attrs):
        el = document.createElementNS(_SVG_NS, tag)
        for k, v in attrs.items():
            el.setAttribute(k.replace('_', '-'), str(v))
        return el

    # ── Dial rendering ───────────────────────────────────────────────────────

    def _tp_render_dial(self):
        svg = self._tp_svg
        svg.innerHTML = ''

        cx, cy = 120, 120
        num_r = 88
        num_r_inner = 56
        num_cr = 20
        is_24 = self._tp_is_24()

        # Background circle
        bg = self._svg_el('circle', cx=cx, cy=cy, r=120)
        bg.setAttribute('class', 'anvil-m3-timepicker-clock-face')
        svg.appendChild(bg)

        # Hand endpoint
        if self._tp_editing == 'hour':
            h_angle = ((self._tp_pending_hour % 12) * 30 - 90) * math.pi / 180
            is_inner = is_24 and (self._tp_pending_hour == 0 or self._tp_pending_hour >= 13)
            hand_r = num_r_inner if is_inner else num_r
            hand_angle = h_angle
        else:
            hand_angle = (self._tp_pending_minute * 6 - 90) * math.pi / 180
            hand_r = num_r

        hand_x = cx + hand_r * math.cos(hand_angle)
        hand_y = cy + hand_r * math.sin(hand_angle)

        line = self._svg_el('line', x1=cx, y1=cy, x2=hand_x, y2=hand_y)
        line.setAttribute('class', 'anvil-m3-timepicker-hand')
        svg.appendChild(line)

        handle = self._svg_el('circle', cx=hand_x, cy=hand_y, r=num_cr)
        handle.setAttribute('class', 'anvil-m3-timepicker-hand-tip')
        svg.appendChild(handle)

        # Numbers
        if self._tp_editing == 'hour':
            numbers_outer = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            numbers_inner = [0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] if is_24 else []
            selected = self._tp_pending_hour
        else:
            numbers_outer = [i * 5 for i in range(12)]
            numbers_inner = []
            selected = self._tp_pending_minute

        for v in numbers_outer:
            a = ((v % 12) * 30 - 90) * math.pi / 180 if self._tp_editing == 'hour' else (v * 6 - 90) * math.pi / 180
            x = cx + num_r * math.cos(a)
            y = cy + num_r * math.sin(a)
            is_sel = (v == selected)
            circ = self._svg_el('circle', cx=x, cy=y, r=num_cr)
            circ.setAttribute('class', 'anvil-m3-timepicker-num-circle' + (' anvil-m3-timepicker-num-selected' if is_sel else ''))
            svg.appendChild(circ)
            txt = self._svg_el('text', x=x, y=y)
            txt.setAttribute('class', 'anvil-m3-timepicker-num-text' + (' anvil-m3-timepicker-num-text-selected' if is_sel else ''))
            txt.setAttribute('text-anchor', 'middle')
            txt.setAttribute('dominant-baseline', 'central')
            txt.textContent = f'{v:02d}' if self._tp_editing == 'minute' else str(v)
            svg.appendChild(txt)

        for v in numbers_inner:
            a = ((v % 12) * 30 - 90) * math.pi / 180
            x = cx + num_r_inner * math.cos(a)
            y = cy + num_r_inner * math.sin(a)
            is_sel = (v == selected)
            circ = self._svg_el('circle', cx=x, cy=y, r=num_cr)
            circ.setAttribute('class', 'anvil-m3-timepicker-num-circle' + (' anvil-m3-timepicker-num-selected' if is_sel else ''))
            svg.appendChild(circ)
            txt = self._svg_el('text', x=x, y=y)
            txt.setAttribute('class', 'anvil-m3-timepicker-num-text anvil-m3-timepicker-num-text-inner' + (' anvil-m3-timepicker-num-text-selected' if is_sel else ''))
            txt.setAttribute('text-anchor', 'middle')
            txt.setAttribute('dominant-baseline', 'central')
            txt.textContent = str(v)
            svg.appendChild(txt)

        center = self._svg_el('circle', cx=cx, cy=cy, r=6)
        center.setAttribute('class', 'anvil-m3-timepicker-center-dot')
        svg.appendChild(center)

    def _tp_handle_dial_click(self, event):
        event.stopPropagation()
        rect = self._tp_svg.getBoundingClientRect()
        x = (event.clientX - rect.left) / rect.width * 240
        y = (event.clientY - rect.top) / rect.height * 240
        dx, dy = x - 120, y - 120
        angle = (math.atan2(dy, dx) * 180 / math.pi + 90) % 360
        dist = math.sqrt(dx * dx + dy * dy)
        is_24 = self._tp_is_24()
        if self._tp_editing == 'hour':
            hour_idx = round(angle / 30) % 12
            if is_24:
                if dist > (88 + 56) / 2:
                    self._tp_pending_hour = hour_idx or 12
                else:
                    self._tp_pending_hour = 0 if hour_idx == 0 else hour_idx + 12
            else:
                self._tp_pending_hour = hour_idx or 12
            self._tp_editing = 'minute'
        else:
            self._tp_pending_minute = round(angle / 6) % 60
        self._tp_update_display()
        self._tp_render_dial()

    # ── Display ──────────────────────────────────────────────────────────────

    def _tp_update_display(self):
        is_24 = self._tp_is_24()
        if document.activeElement != self._tp_hour_chip:
            self._tp_hour_chip.value = f'{self._tp_pending_hour:02d}' if is_24 else str(self._tp_pending_hour)
        if document.activeElement != self._tp_minute_chip:
            self._tp_minute_chip.value = f'{self._tp_pending_minute:02d}'
        self._tp_hour_chip.classList.toggle('anvil-m3-timepicker-chip-active', self._tp_editing == 'hour')
        self._tp_minute_chip.classList.toggle('anvil-m3-timepicker-chip-active', self._tp_editing == 'minute')
        self._tp_am_btn.classList.toggle('anvil-m3-timepicker-ampm-selected', self._tp_pending_is_am)
        self._tp_pm_btn.classList.toggle('anvil-m3-timepicker-ampm-selected', not self._tp_pending_is_am)
        self._tp_ampm_container.style.display = 'none' if is_24 else ''

    # ── Chip focus / input ───────────────────────────────────────────────────

    def _tp_handle_hour_focus(self, event):
        self._tp_editing = 'hour'
        self._tp_update_display()
        self._tp_render_dial()

    def _tp_handle_minute_focus(self, event):
        self._tp_editing = 'minute'
        self._tp_update_display()
        self._tp_render_dial()

    def _tp_handle_hour_input(self, event):
        is_24 = self._tp_is_24()
        try:
            h = int(self._tp_hour_chip.value)
            self._tp_pending_hour = max(0, min(23, h)) if is_24 else max(1, min(12, h))
        except (ValueError, TypeError):
            pass
        self._tp_render_dial()

    def _tp_handle_minute_input(self, event):
        try:
            m = int(self._tp_minute_chip.value)
            self._tp_pending_minute = max(0, min(59, m))
        except (ValueError, TypeError):
            pass
        self._tp_render_dial()

    # ── AM / PM ──────────────────────────────────────────────────────────────

    def _tp_handle_am_click(self, event):
        event.stopPropagation()
        self._tp_pending_is_am = True
        self._tp_update_display()

    def _tp_handle_pm_click(self, event):
        event.stopPropagation()
        self._tp_pending_is_am = False
        self._tp_update_display()
