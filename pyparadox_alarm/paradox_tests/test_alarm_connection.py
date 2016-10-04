'''Some code to help test Paradox alarm interface.'''

import logging
import time
from pyparadox_alarm.alarm_panel import ParadoxAlarmPanel

_LOGGER = logging.getLogger(__name__)

loggingconfig = {'level': 'DEBUG',
    'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
    'datefmt': '%a, %d %b %Y %H:%M:%S'}

logging.basicConfig(**loggingconfig)

TEST_TOT_AREA = 1
TEST_TOT_ZONE = 6
TEST_TOT_WAIT = TEST_TOT_ZONE * 3
_LOGGER.warn('Start')
panel = ParadoxAlarmPanel()

_LOGGER.info('Start test:')
_LOGGER.info('Alarm State before:')
#print(panel.alarm_state['zone'])
print(panel.alarm_state)
panel.start()
panel.request_all_labels(TEST_TOT_AREA, TEST_TOT_ZONE)
time.sleep(TEST_TOT_WAIT) #Wait because we're using threading
_LOGGER.info('Alarm State after:')
print(panel.alarm_state)
_LOGGER.info('Disconnecting...')
panel.stop()
_LOGGER.info('Waiting for all to stop:')
time.sleep(10)
_LOGGER.info('End test:')
