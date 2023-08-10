
from ._anvil_designer import ButtonMenuTemplate
from anvil import *
from anvil.js.window import document
import random, string
from Menu import Menu

class ButtonMenu(ButtonMenuTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # TODO: needs an event handler to close when not focused
  
  @property
  def text(self):
    return self._text
  @text.setter
  def text(self, value):
    self._text = value
    self.menu_button.text = value
    
  @property
  def appearance(self):
    return self._appearance
  @appearance.setter
  def appearance(self, value):
    self.menu_button.appearance = value

  # @property
  # def menuOpen(self):
  #   return self._menuOpen
  # @menuOpen.setter
  # def menuOpen(self, value):
  #   self._menuOpen = value or False
    # self.dom_nodes['anvil-m3-buttonMenu-container']
    # if value:
    #   self.dom_nodes['anvil-m3-buttonMenu-container'].addEventListener('focus', self.checkFocus)
  @property
  def menuComponent(self):
    return self._menuComponent
  @menuComponent.setter
  def menuComponent(self, value):
    self._menuComponent = value
  
  @property
  def enabled(self):
    return self._enabled
  @enabled.setter
  def enabled(self, value):
    self._enabled = value
    self.menu_button.enabled = value
    
  # def toggle_menu_visibility(self, **event_args):
  #   self.set_visibility()
  #   # return classes.contains(className)
  #   self.menuOpen = not self.dom_nodes['anvil-m3-buttonMenu-items-container'].classList.contains('anvil-m3-buttonMenu-items-hidden')

  # def set_visibility(self, value = None):
  #   classes = self.dom_nodes['anvil-m3-buttonMenu-items-container'].classList
  #   if value is not None:
  #     classes.toggle('anvil-m3-buttonMenu-items-hidden', not value)
  #   else:
  #     classes.toggle('anvil-m3-buttonMenu-items-hidden')

  # def closeOnLoseFocus(self, event):
  #   if not self.dom_nodes['anvil-m3-buttonMenu-items-container'].contains(event.target):
  #     self.set_visibility(False)

  # def checkFocus(self, event):
  #   # document.activeElement
  #   # var descendants = theElement.querySelectorAll("*");
  #   print(event.target)
  #   pass


  # def _anvil_get_design_info_(self, as_layout=False):
  #   design_info = super()._anvil_get_design_info_(as_layout)
  #   design_info["interactions"] = [
  #     {
  #       "type": "on_selection",
  #       "callbacks": {
  #         "onSelectDescendent": self._on_select_descendant, 
  #         "onSelectOther": self._on_select_other
  #       }
  #     },
  #   ]
  #   return design_info
   
  # def _on_select_descendant(self):
  #   print("Selected! Open")
  #   self.set_visibility(True)

  # def _on_select_other(self):
  #   print("Something else selected! Close the menu!")
  #   self.set_visibility(False)

  # def toggle_menu_visibility(self, **event_args):
  #   """This method is called when the component is clicked"""
  #   pass

  def attach_hidden_menu(self, **event_args):
    menu = Menu(visible=False)
    self.add_component(menu)
    


