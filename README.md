# pyparadox
Some code to interface with a Paradox Alarm Panel.

The code was developed for the purpose of integrating Paradox Alarms into the Home Assistant home automation software.

It defines a dictionary to mirror the alarm state. Currently only zone changes and arming/disarming events are mirrored which is the minimum required to be useful in Home Assistant.

It uses callback functions that can be set by the calling code to be notified of zone and area status changes.

As it merely relays the commands, theoretically it also supports all other commands, but it might not react to it intelligently.

In it's current form it is only able to integrate with a Paradox Alarm panel that has the PRT3 module installed. 

Later versions can be expanded to also support the IP100/150 modules. 
