# paradox-alarm
Some code to interface with a Paradox Alarm Panel.

The code is needed to allow Paradox Alarms to be used in Home Assistant.

For now most things will be hard-coded in order to test integration with Home Assistant. As it starts to work hard-coding will be replaced with actual interfacing code.

The main goal is to get the PRT-3 module to work as it does not require the panel to be exposed to the internet directly. Later on the code can be expanded to also support the IP100/150 modules. By definition this means only panels that support the PRT-3, IP100 and IP150 modules wll be supported, i.e. Evo and Magellan.
