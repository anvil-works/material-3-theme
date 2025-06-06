## Version 1.2.5
_Release date: 6 June 2025_

## What's Changed
* The DropdownMenu's `error` property now actually works by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/286
* Add show and hide events to CardContentContainer by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/288
* Add "full" as an option for the FileLoader's `align` property by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/287
* You can now import all components using the components package, e.g. `from m3.components import Avatar` by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/289
* The `margin` property of the AvatarMenu is applied to the correct element, which means that adding margin no longer messes with the placement of the menu by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/291
* FileLoader's default spacing now targets correct element. This means that the default margin and padding are properly displayed in the Properties Panel and can be overridden by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/294
* The Menu in Menu components (e.g. ButtonMenu) is now `display:none` when closed by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/292
* Fix theme still not working well with Free Plan banner by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/295
* `.anvil-panel-row` divs no longer center align their children. This stops the ColumnPanel from center aligning components. by @bcm628 in https://github.com/anvil-works/material-3-theme/pull/296

## Version 1.2.4
_Release date: 16 May 2025_

**Fixes**
* The `role` property for TextInputs (TextBoxes and TextAreas) is now actually implemented. This means the DropdownMenu `role` property works as expected.
* Fixed an issue where the Avatar image could be blurry if the aspect ratio wasn't 1:1
* Reordered components in the Toolbox so Menus are not at the top

## Version 1.2.3
_Release date: 11 April 2025_

**New Components**
* Avatar: The Avatar component is for displaying a user's avatar. It has the following key properties:
  * `image`: This is the image that will be displayed on the avatar 
  * `name`: You can associate the user's name with the Avatar. If no image is provided, the Avatar will display the user's initials, generated from the name
  * `fallback_icon`: By default, if no image or name is provided, the Avatar will display the person icon. You can change this icon by setting the fallback_icon property
* AvatarMenu: Like the ButtonMenu, the AvatarMenu component is an Avatar component that opens a popup menu when clicked. You can drag and drop components into this menu from the Anvil Editor, or add components via the `menu_items` property. MenuItem components are designed to be added to this menu (but you can add whatever you want!).
* IconButtonMenu: Similarly, the IconButtonMenu component is an IconButton that opens a popup menu when clicked.

**Updates**
* Theme colors are now set to CSS variables. This means that if app.theme_colors is updated at runtime, colors set in component properties will update.

**Fixes**
* Fixed an extraneous import in theme.css
* Fixed an issue where Buttons could be out of alignment in built-in Anvil modals (such as the Login Form)
* Fixed an issue where canceling the FileLoader file selector window instead of selecting a file could raise an IndexError
* The theme now accomodates the Free Banner, which previously overlayed the page content
* For properties that set a JS element's innerText, the property is first set to a string. This stops Python booleans from being converted to JS booleans (e.g. `True` was previously displayed as `true`)
* The `tooltip` property on IconButtons previously didn't appear under the component if the alignment was set to anything other than `left`
* You can now set the `spacing` property of ButtonMenu components from the Anvil Editor
* The `icon_position` property of ButtonMenu components is now called `icon_align`. This means it actually works and matches the name of the equivalent Button property
  
## Version 1.2.2
_Release date: 6 February 2025_

**Updates**
* The NavigationDrawerLayout now has methods to open and close the navigation drawer from code
* The modal navigation drawer now has a `max-width` so it will never take up the whole screen, making it difficult to close 

**Fixes**
* Fixed an issue where clicking the Dropdown icon could cause the space bar to open and close the menu even when the Dropdown doesn't have focus
* Fixed an AttributeError when autofilling TextBoxes and TextAreas
* The bottom app bar on mobile layouts no longer overlays the content on the page
* Fixed a styling issue with Notifications
* The ButtonMenu now works in the old M3 navigation drawer
* Fixed an issue with importing the TextArea and TextBox components
* Fixed the sliding animation on the NavigationDrawerLayout's navigation drawer
* Fixed a styling issue with the borders of DataRowPanels when added to a DataGrid
* The RadioButton no longer squishes when there is a lot of label text
* Fixed an issue where the autocompleter considered properties to be methods

## Version 1.2.1
_Release date: 19 November 2024_

**Updates**
* When in the designer, the placeholder text for the Link looks more like placeholder text
* The RadioGroupPanel's `change` event now appears in the Object Palette
  
**Fixes**
* The border of the DropdownMenu menu is now rounded
* Fixed an issue with the DropdownMenu where when the items are a list of tuples, the selected_value is the entire tuple
* Fixed an issue with outlined DropdownMenu where the label was appearing beind the component's border
* Add writeback support for various components (Checkbox, DropdownMenu, RadioGroupPanel, Switch)
* The placeholder text reappears when a component is removed from a Link
* Added a close button to Notification and Confirm modals
* Added click event parameters to all click events. Add the keys argument to ButtomMenus, IconButtons and ToggleIconButtons
* Added the `change_end` event to Sliders, which triggers when the user stops dragging the Slider thumb
* Inherit the font-family of Buttons and NavigationLinks from the body
* Fix typo in the Toolbox with the LinearPanel
* Fixed the TextInput subcontent style properties to work as expected
* The align property now works as expected for TextBoxes and DropdownMenus

## Version 1.2.0
_Release date: 6 November 2024_

**Breaking Changes**
* The navigation slot in the NavigationDrawerLayout and the NavigationRailLayout now have the same name. This means that if you change the layout of your Form, the components in the navigation slot will stay there. For existing apps, components that were in a navigation slot will need to be dragged from the [orphaned components panel](https://anvil.works/docs/ui/layouts#orphaned-components) back into the correct slot.

**Updates**
* The SidesheetContent component is now pre-populated with a Heading and IconButton.
* The RadioGroupPanel component is now pre-populated with three RadioButtons.
* When using the NavigationDrawerLayout that has collapsed to mobile view, you can now double click on the hamburger menu button in the designer to open the navigation drawer.
* Some components had `background` properties that are now renamed to `background_color`.
* In the designer, the NavigationDrawerLayout won't collapse to modal view until the screen is smaller.
* When Text and Heading components have no `text`, their component names actually look like placeholders.
* The `label` of a TextArea can now be edited from the Object Palette or by double clicking the component.

**Fixes**
* FileLoader now has a `files` property that works as expected.
* DataGrids now work as expected - they're automatically populated with a RepeatingPanel.
* Fixed an issue where DropdownMenu items were being duplicated when the `show` event was fired.
* Fixed an issue where you couldn't make changes to DropdownMenu items once the component was rendered.
* Material Icons no longer flash as text before being rendered as icons.
* Fixed an issue where Data Binding writeback wasn't working for TextBoxes and TextAreas.
* Setting the `align` property of ButtonMenus to `full` now works.
* The `align` property of Links now works.
* Fixed an issue where the ButtonMenu menu rendered behind popup menus.
* The `display_text_color` property of TextBoxes and TextAreas now works.
* Links in built-in Anvil modals are now properly styled.
