from anvil import *

from ._anvil_designer import RadioGroupPanelTemplate


class RadioGroup(Component):
    _anvil_events_ = [{"name": "change", "defaultEvent": True}]

    def __init__(self):
        self._buttons = []
        self._selected_button = None

    #!componentEvent(m3.RadioGroupPanel)!1: {name: "change", description: "When the Radio Button selection changes."}
    #!componentEvent(m3.RadioGroupPanel)!1: {name: "show", description: "When the component is shown on the screen."}
    #!componentEvent(m3.RadioGroupPanel)!1: {name: "hide", description: "When the component is removed from the screen."}

    #!componentProp(m3.RadioGroupPanel)!1: {name:"selected_value",type:"object",description:"Value property of the selected RadioButton."}

    @property
    def buttons(self):
        return self._buttons

    def _add_button(self, button):
        self._buttons.append(button)

    def _remove_button(self, button):
        self._buttons.remove(button)

    def _handle_change(self):
        self.raise_event("x-anvil-write-back-selected_value")
        self.raise_event("change")

    @property
    def selected_button(self):
        for button in self._buttons:
            if button.selected:
                return button
        return None

    @selected_button.setter
    def selected_button(self, button):
        if button is None:
            # Deselect the currently selected button
            selected_button = self.selected_button
            if selected_button:
                selected_button.selected = False
        else:
            if button not in self._buttons:
                raise ValueError("RadioButton is not in this group")
            button.selected = True

    @property
    def selected_value(self):
        button = self.selected_button
        if button is None:
            return None
        else:
            return button.value

    @selected_value.setter
    def selected_value(self, requested_value):
        for button in self._buttons:
            if button.value == requested_value:
                self.selected_button = button
                return
        self.selected_button = None

    @classmethod
    def enclosing(cls, component):
        while component:
            component = component.parent
            if isinstance(component, cls):
                return component

        # No enclosing RadioGroup container, return a global one
        return global_radio_group


global_radio_group = RadioGroup()


class RadioGroupPanel(RadioGroup, RadioGroupPanelTemplate):
    def __init__(self, **properties):
        super().__init__()
        self.init_components(**properties)


#!defClass(m3, RadioGroupPanel, anvil.Component)!:
