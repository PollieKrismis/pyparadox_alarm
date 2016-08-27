import logging
import json
import re
import time
from pyparadox-alarm.alarm_panel import ParadoxAlarmPanel

_LOGGER = logging.getLogger(__name__)

loggingconfig = {'level': 'DEBUG',
                 'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
                 'datefmt': '%a, %d %b %Y %H:%M:%S'}

logging.basicConfig(**loggingconfig)


panel = ParadoxAlarmPanel()

_LOGGER.info('Start test:')
_LOGGER.info('Alarm State before:')
print(alarmState['zone'])
panel.start()
sleep(20)
_LOGGER.info('Alarm State after:')
print(alarmState['zone'])