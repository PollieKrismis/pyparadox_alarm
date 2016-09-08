# pyparadox
Some code to interface with a Paradox Alarm Panel.

The code was developed for the purpose of integrating Paradox Alarms into the Home Assistant home automation software.

The current version is able to connect to the alarm panel request all area and zone labels as well as their statuses. 

It is also able to keep a dictionary in sync with the alarm panel my mirroring area and zone statuses.

The next version must accept callback functions which will then be used to keep the Home Assistant devices in sync.

The third version should be able to submit arming and maybe disarming commands to the panel.

In it's current form it is only able to integrate with a Paradox Alarm panel that has the PRT3 module installed. 

Later versions can be expanded to also support the IP100/150 modules. 

Versioning:
- 0.1.2: 
  - Gets zone and area labels and statusses and report on zone open/close status and area arm/disarm status.
  - Allows Callbacks, albeit not tested yet.
