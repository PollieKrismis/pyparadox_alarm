import logging
import time
from alarm_panel import ParadoxAlarmPanel
#from paradox import *
#import paradox

_LOGGER = logging.getLogger(__name__)

loggingconfig = {'level': 'DEBUG',
                 'format': '%(asctime)s %(levelname)s <%(name)s %(module)s %(funcName)s> %(message)s',
                 'datefmt': '%a, %d %b %Y %H:%M:%S'}

logging.basicConfig(**loggingconfig)

_LOGGER.warn('Start')
panel = ParadoxAlarmPanel()

_LOGGER.info('Start test:')
_LOGGER.info('Alarm State before:')
#print(panel.alarm_state['zone'])
print(panel.alarm_state())
panel.start()
sleep(20)
_LOGGER.info('Alarm State after:')
print(panel.alarm_state())
