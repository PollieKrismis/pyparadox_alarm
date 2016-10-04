'''Replicates a Paradox Alarm panel as a dictionary and allows interfacing to it.'''

import logging
import time
import threading
from queue import Queue, Empty
from pyparadox_alarm.paradox_defaults import PARADOX_MODELS
from pyparadox_alarm.alarm_serial_comms import ParadoxSerialComms
from pyparadox_alarm.alarm_state import AlarmState

_LOGGER = logging.getLogger(__name__)
COMMAND_ERR = "Cannot run this command while disconnected. Please run start() first."

class ParadoxAlarmPanel:
    '''This class represents an Paradox alarm panel.'''

    def __init__(self, paradox_model='EVO48', comm_module='PRT3',
                #username='user', password='user',
                prt_port='/dev/ttyUSB0', prt_speed=57600):
        _LOGGER.debug('Initialising Panel')
        self._paradox_model = paradox_model
        #self._username = username
        #self._password = password
        self._prt_port = prt_port
        self._prt_speed = prt_speed

        #Set callbacks
        self._callback_zone_name = self._default_callback
        self._callback_area_name = self._default_callback
        self._callback_zone_state_change = self._default_callback
        self._callback_area_armed = self._default_callback
        self._callback_area_stay_armed = self._default_callback
        self._callback_area_disarmed = self._default_callback

        #Setup default panel state
        self._panel = None
        self._max_areas = PARADOX_MODELS[self._paradox_model]['max areas']
        self._max_zones = PARADOX_MODELS[self._paradox_model]['max zones']
        self._alarm_state = AlarmState.get_initial_alarm_state(self._max_zones, self._max_areas)
        #Setup queues to be used to submit/receive data to/from the panel
        self._to_alarm = Queue()
        self._from_alarm = Queue()
        self._shutdown = None



        '''
        if 'PRT' in comm_module:
            self._serial = True
            self._tcpip = False
        elif 'IP' in comm_module:
            self._serial = False
            self._tcpip = True
        else:
            self._serial = False
            self._tcpip = False
            _LOGGER.error("Unsupported communication module.")


        self._loginSuccessCallback = self._defaultCallback
        self._loginFailureCallback = self._defaultCallback
        self._loginTimeoutCallback = self._defaultCallback
        self._commandResponseCallback = self._defaultCallback
        self._pollResponseCallback = self._defaultCallback
        self._keypadUpdateCallback = self._defaultCallback
        self._zoneStateChangeCallback = self._defaultCallback
        self._partitionStateChangeCallback = self._defaultCallback
        self._cidEventCallback = self._defaultCallback
        self._zoneTimerCallback = self._defaultCallback
        '''
        _LOGGER.debug('Panel initialised.')

    @ property
    def port(self):
        '''Returns the ip or usb port used to connect to the alarm panel.'''
        return self._prt_port

    @property
    def paradox_model(self):
        '''Returns the model of the alarm panel being connected to.'''
        _LOGGER.debug('Returning model name, %s.', self._paradox_model)
        return self._paradox_model

    @property
    def alarm_state(self):
        '''Returns the alarm state dictionary.'''
        return self._alarm_state

    @property
    def callback_zone_name(self):
        '''Calls function subscribed to zone name.'''
        return self._callback_zone_name

    @callback_zone_name.setter
    def callback_zone_name(self, value):
        '''Subscribes a function to zone name.'''
        self._callback_zone_name = value

    @property
    def callback_area_name(self):
        '''Calls function subscribed to area name.'''
        return self._callback_area_name

    @callback_area_name.setter
    def callback_area_name(self, value):
        '''Subscribes a function to area name.'''
        self._callback_area_name = value

    @property
    def callback_zone_state_change(self):
        '''Calls function subscribed to zone changes.'''
        return self._callback_zone_state_change

    @callback_zone_state_change.setter
    def callback_zone_state_change(self, value):
        '''Subscribes a function to zone changes.'''
        self._callback_zone_state_change = value

    @property
    def callback_area_armed(self):
        '''Calls function subscribed to an area/partition arming event.'''
        return self._callback_area_armed

    @callback_area_armed.setter
    def callback_area_armed(self, value):
        '''Subscribes a function to an area/partition arming event.'''
        self._callback_area_armed = value

    @property
    def callback_area_stay_armed(self):
        '''Calls function subscribed to an area/partition stay armed event.'''
        return self._callback_area_stay_armed

    @callback_area_stay_armed.setter
    def callback_area_stay_armed(self, value):
        '''Subscribes a function to an area/partition stay armed event.'''
        self._callback_area_stay_armed = value

    @property
    def callback_area_disarmed(self):
        '''Calls function subscribed to an area/partition disarming event.'''
        return self._callback_area_disarmed

    @callback_area_disarmed.setter
    def callback_area_disarmed(self, value):
        '''Subscribes a function to an area/partition disarming event.'''
        self._callback_area_disarmed = value

    def _default_callback(self, number):
        '''This is the callback that occurs when the client doesn't subscribe.'''
        _LOGGER.debug("Callback for area/zone/user %s has not been set by client.", number)

    def start(self):
        '''Connect to the Paradox Alarm and start listening for events to occur.'''
        _LOGGER.info("Connecting to Paradox on host: %s, port: %d",
                                self._prt_port, self._prt_speed)
        self._panel = ParadoxSerialComms(self._to_alarm, self._from_alarm,
                                        self._prt_port, self._prt_speed)
        self._panel.start()
        #Allow for a list of areas and zones to be passed rather than simply requesting all
        #self.request_all_labels(self._max_areas, self._max_zones)
        listen_thread = threading.Thread(target=self.monitor_response_queue)
        listen_thread.start() #We need a thread to keep on listening for alarm messages
        #time.sleep(2) #With proper queue management this should not be needed.
        #self._to_alarm.join() #Allow some time for all the requests to be serviced
        #self.request_all_statuses(self._max_areas, self._max_zones)

    def stop(self):
        '''Shut down and close our connection to the Paradox Alarm.'''
        self._shutdown = True # this should kill the "monitoring" thread
        if self._panel:
            _LOGGER.info("Disconnecting from the Paradox Alarm...")
            self._panel.stop()
        else:
            _LOGGER.error(COMMAND_ERR)

    def request_all_labels(self, area_total, zone_total):
        '''Submits requests for all area and zone labels.'''
        _LOGGER.debug("Requesting %s zone labels...", zone_total)
        for i in range(1, zone_total + 1):
            self.submit_zone_label_request(i)
            time.sleep(0.1)

        _LOGGER.info(str.format("Requesting {0} area labels...", area_total))
        for i in range(1, area_total + 1):
            self.submit_area_label_request(i)
            time.sleep(0.1)

    def request_all_statuses(self, area_total, zone_total):
        '''Submits requests for all area and zone statuses.'''
        _LOGGER.info(str.format("Requesting {0} zone statuses...", zone_total))
        for i in range(1, zone_total + 1):
            self.submit_zone_status_request(i)
            time.sleep(0.1)

        _LOGGER.info(str.format("Requesting {0} area statuses...", area_total))
        for i in range(1, area_total + 1):
            self.submit_area_status_request(i)
            time.sleep(0.1)

    def submit_area_label_request(self, area_num):
        '''Places an area label request on the request queue.'''
        self.submit_request("AL" + str(area_num).zfill(3))

    def submit_zone_label_request(self, zone_num):
        '''Places a zone label request on the request queue.'''
        self.submit_request("ZL" + str(zone_num).zfill(3))

    def submit_area_status_request(self, area_num):
        '''Places an area label request on the request queue.'''
        self.submit_request("RA" + str(area_num).zfill(3))

    def submit_zone_status_request(self, zone_num):
        '''Places a zone label request on the request queue.'''
        self.submit_request("RZ" + str(zone_num).zfill(3))

    def submit_request(self, request):
        '''Places a request on the request queue.'''
        self._to_alarm.put(request, timeout=10)

    def decode_system_event(self, response):
        '''Decodes a system event.'''
        _event_group = response[1:4]
        _event_number = int(response[5:8])
        _area_number = int(response[9:12])
        if _event_group in ['000']: #Zone closed/OK
            self.update_zone_status(_event_number, 'C')
        elif _event_group in ['001']: #Zone open
            self.update_zone_status(_event_number, 'O')
        elif _event_group in ['009', '010', '011', '012']: #Area arming
            self.update_area_status(_area_number, 'A')
        elif _event_group in ['014']: #Area disarming
            self.update_area_status(_area_number, 'D')
        else:
            _LOGGER.debug(str.format('Event {0} to be defined.', response))

    def decode_response(self, response):
        '''Decode the Paradox Alarm response.'''
        #2Do: Handle requests that failed, i.e. &fail
        _msg_type = response[:2]
        if response[:1] == "G": #System event
            self.decode_system_event(response)
        elif response[:2] == "ZL": #Zone label
            self.update_zone_name(int(response[2:5]), response[5:])
        elif _msg_type == "RZ": #Zone status
            self.update_zone_status(int(response[2:5]), response[5:])
        elif response[:2] == "AL": #Area label
            self.update_area_name(int(response[2:5]), response[5:])
        elif _msg_type == "RA": #Area status
            self.update_area_status(int(response[2:5]), response[5:])
        else:
            _LOGGER.debug(str.format('Response {0} to be defined.', response))

    def update_zone_name_cb(self, zone_number):
        '''Callback zone name to connected client.'''
        _LOGGER.debug(str.format('Zone callback to {}...', self._callback_zone_name))
        if self._callback_zone_name is not None:
            self._callback_zone_name(zone_number)

    def update_zone_name(self, zone_number, zone_name):
        '''Sets the name of the zone.'''
        self._alarm_state['zone'][zone_number]['name'] = zone_name
        _ignore = self.update_zone_name_cb(zone_number)

    def update_zone_status_cb(self, zone_number):
        '''Callback zone status to connected client.'''
        _LOGGER.debug(str.format('Zone callback to {}...', self._callback_zone_state_change))
        if self._callback_zone_state_change is not None:
            self._callback_zone_state_change(zone_number)

    def update_zone_status(self, zone_number, zone_status):
        '''Updates the zone status.'''
        #ZONE_OPEN = 'O'
        #ZONE_ALARM = 'A'
        _status = zone_status[:1]
        _in_alarm = zone_status[1:2]
        #_fire = status[2:3]
        #_supervision_lost = status[3:4]
        #_low_battery = status[4:5]
        _zone_info = {'open': (_status == 'O'),
                        'fault': False,
                        'alarm': (_in_alarm == 'A'),
                        'tamper': False}
        self._alarm_state['zone'][zone_number]['status'] = _zone_info
        _LOGGER.debug(str.format('Zone {0} status updated.', zone_number))
        #Zone status changed, who needs to know about this?
        _ignore = self.update_zone_status_cb(zone_number)

    def update_area_name_cb(self, area_number):
        '''Callback area name to connected client.'''
        _LOGGER.debug(str.format('Area name callback to {}...', self._callback_area_name))
        if self._callback_area_name is not None:
            self._callback_area_name(area_number)

    def update_area_name(self, area_number, area_name):
        '''Sets the name of the area/partition.'''
        self._alarm_state['partition'][area_number]['name'] = area_name
        _ignore = self.update_area_name_cb(area_number)

    def update_area_armed_cb(self, area_number):
        '''Callback area armed to connected client.'''
        _LOGGER.debug('Area status callback to %s...', self._callback_area_armed)
        if self._callback_area_armed is not None:
            self._callback_area_armed(area_number)

    def update_area_stay_armed_cb(self, area_number):
        '''Callback area stay armed to connected client.'''
        _LOGGER.debug('Area status callback to %s...', self._callback_area_stay_armed)
        if self._callback_area_stay_armed is not None:
            self._callback_area_stay_armed(area_number)

    def update_area_disarmed_cb(self, area_number):
        '''Callback area disarmed to connected client.'''
        _LOGGER.debug('Area status callback to %s...', self._callback_area_disarmed)
        if self._callback_area_disarmed is not None:
            self._callback_area_disarmed(area_number)

    def update_area_status(self, area_number, area_status):
        '''Updates the area status.'''
        _status = area_status[:1]
        if _status in ['A']:
            self._alarm_state['partition'][area_number]['status']['armed_away'] = (_status == 'A')
            _ignore = self.update_area_armed_cb(area_number)
        elif _status in ['S']:
            self._alarm_state['partition'][area_number]['status']['armed_stay'] = (_status == 'S')
            _ignore = self.update_area_stay_armed_cb(area_number)
        elif _status in ['D']:
            self._alarm_state['partition'][area_number]['status']['alpha'] = (_status == 'D')
            _ignore = self.update_area_disarmed_cb(area_number)
        _LOGGER.debug('Area %d status updated.', area_number)

    def monitor_response_queue(self):
        '''Wait for responses from the Paradox Alarm and decode them (as thread).'''
        _LOGGER.debug(str.format('Wait for alarm responses/events on the queue...'))
        self._shutdown = False  #Force endless loop
        while not self._shutdown:
            try:
                response = self._from_alarm.get_nowait()
                _LOGGER.debug(str.format('Response found:{0}', response))
                self.decode_response(response)
                self._from_alarm.task_done()
                time.sleep(0.1)
            except Empty:
                time.sleep(5)

        _LOGGER.debug(str.format('Stop monitoring response/event queue...'))
