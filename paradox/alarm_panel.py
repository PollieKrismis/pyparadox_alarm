"""Replicates a Paradox Alarm panel and allows interfacing to it."""
import logging
import time
from queue import Queue
from alarm_defaults import PARADOX_MODELS
from alarm_serial_comms import ParadoxSerialComms
from alarm_state import AlarmState

_LOGGER = logging.getLogger(__name__)
COMMAND_ERR = "Cannot run this command while disconnected. Please run start() first."


class ParadoxAlarmPanel:
    """This class represents an Paradox alarm panel."""

    def __init__(self, paradox_model='EVO48', comm_module='PRT3',
                 username='user', password='user',
                 prt_port='/dev/ttyUSB0', prt_speed=57600):
        self._paradox_model = paradox_model
        self._username = username
        self._password = password
        self._prt_port = prt_port
        self._prt_speed = prt_speed

        #Setup default panel state
        self._panel = None
        self._max_areas = PARADOX_MODELS[self._paradox_model]['MaxAreas']
        self._max_zones = PARADOX_MODELS[self._paradox_model]['MaxZones']
        self._alarm_state = AlarmState.get_initial_alarm_state(self._max_zones, self._max_areas)
        #Setup queues to be used to submit/receive data to/from the panel
        self._to_alarm = Queue()
        self._from_alarm = Queue()




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

        loggingconfig = {'level': 'DEBUG',
            'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
            'datefmt': '%a, %d %b %Y %H:%M:%S'}

        logging.basicConfig(**loggingconfig)

    @ property
    def port(self):
        """Returns the ip or usb port used to connect to the alarm panel."""
        return self._prt_port

    @property
    def paradox_model(self):
        """Returns the model of the alarm panel being connected to."""
        return self._paradox_model

    @property
    def callback_zone_state_change(self):
        return self._zoneStateChangeCallback

    @callback_zone_state_change.setter
    def callback_zone_state_change(self, value):
        self._zoneStateChangeCallback = value

    @property
    def callback_partition_state_change(self):
        return self._partitionStateChangeCallback

    @callback_partition_state_change.setter
    def callback_partition_state_change(self, value):
        self._partitionStateChangeCallback = value

    def _defaultCallback(self, data):
        """This is the callback that occurs when the client doesn't subscribe."""
        _LOGGER.debug("Callback has not been set by client.")

    def start(self):
        """Connect to the Paradox Alarm and start listening for events to occur."""
        _LOGGER.info(str.format("Connecting to Paradox on host: {0}, port: {1}",
                                self._prt_port, self._prt_speed))
        self._panel = ParadoxSerialComms(self._to_alarm, self._from_alarm,
                                        self._prt_port, self._prt_speed)
        self._panel.start()
        #Allow for a list of areas and zones to be passed rather than simply requesting all
        self.request_all_labels(self._max_areas, self._max_zones)
        time.sleep(1) #Why do we need this?
        self.monitor_response_queue() #Start processing the responses
        self._to_alarm.join() #Allow some time for all the requests to be serviced
        self.request_all_statuses(self._max_areas, self._max_zones)

    def stop(self):
        """Shut down and close our connection to the Paradox Alarm."""
        if self._panel:
            _LOGGER.info("Disconnecting from the Paradox Alarm...")
            self._panel.stop()
        else:
            _LOGGER.error(COMMAND_ERR)

    def request_all_labels(self, area_total, zone_total):
        """Submits requests for all area and zone labels."""
        _LOGGER.info(str.format("Requesting {0} zone labels...", zone_total))
        for i in range(1, zone_total + 1):
            self.submit_zone_label_request(i)
            time.sleep(0.1)

    def request_all_statuses(self, area_total, zone_total):
        """Submits requests for all area and zone statuses."""
        _LOGGER.info(str.format("Requesting {0} zone statuses...", zone_total))

        for i in range(1, zone_total + 1):
            self.submit_zone_status_request(i)
            time.sleep(0.1)

    def submit_area_label_request(self, area_num):
        """Places an area label request on the request queue."""
        self.submit_request("AL" + str(area_num).zfill(3))

    def submit_zone_label_request(self, zone_num):
        """Places a zone label request on the request queue."""
        self.submit_request("ZL" + str(zone_num).zfill(3))

    def submit_area_status_request(self, area_num):
        """Places an area label request on the request queue."""
        self.submit_request("RA" + str(area_num).zfill(3))

    def submit_zone_status_request(self, zone_num):
        """Places a zone label request on the request queue."""
        self.submit_request("RZ" + str(zone_num).zfill(3))

    def submit_request(self, request):
        """Places a request on the request queue."""
        self._to_alarm.put(request, timeout=10)

    def decode_response(self, response):
        """Decode the Paradox Alarm response."""
        _msg_type = response
        if response[:1] == "G":
            print("Event Group")
        elif response[:2] == "ZL":
            print("Zone Label")
            self.set_zone_name(int(response[2:5]), response[5:])
        elif _msg_type == "RZ":
            print("Zone Status")
            self.update_zone_status(response[1:4], response[5:])
        else:
            print("To be defined")

    def set_zone_name(self, number, name):
        """Sets the name of the zone."""
        self._alarm_state['zone'][number]['name'] = name

    def update_zone_status(self, number, status):
        """Updates the zone status."""
        self._alarm_state['zone'][number]['status'] = status #this must be an update statement!!
        return True

    def monitor_response_queue(self):
        """Wait for responses from the Paradox Alarm and decode them."""
        print("checking response queue...")
        i = 0
        while i < self._max_zones:
            #items = from_alarm.qsize()
            #if items > 0:
            try:
                response = self._from_alarm.get_nowait()
            except self._from_alarm.empty():
                time.sleep(2)
                i += 1

            self.decode_response(response)
            print("Response found:{}".format(response))
            self._from_alarm.task_done()
            time.sleep(2)
            i += 1

        print("queue empty?")

    def alarm_state(self):
        """Returns the alarm state dictionary."""
        return self._alarm_state
