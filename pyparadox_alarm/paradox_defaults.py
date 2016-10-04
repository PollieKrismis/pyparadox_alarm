'''Default values specific to a Paradox Alarm Panel.'''

#Message prefixes
AREA_LABEL_REQUEST = 'AL'
AREA_STATUS_REQUEST = 'AR'
ZONE_LABEL_REQUEST = 'ZL'
ZONE_STATUS_REQUEST = 'RZ'
ZONE_OPEN = 'O'
ZONE_ALARM = 'A'
AREA_DISARMED = 'D'

#Default values to be used if none are specified or for auto discovery.
PARADOX_MODELS = {
    'EVO48' :
    {'model' : 'EVO48', 'max zones' : 48, 'max areas' : 4, 'max users' : 99, 'baudrate' : 57600},
    'EVO96' :
    {'model' : 'EVO96', 'max zones' : 96, 'max areas' : 8, 'max users' : 999, 'baudrate' : 57600},
    'EVO192' :
    {'model' : 'EVO192', 'max zones' : 192, 'max areas' : 8, 'max users' : 999, 'baudrate' : 57600},
    'DGP-848' :
    {'model' : 'DGP-848', 'max zones' : 48, 'max areas' : 4, 'max users' : 96, 'baudrate' : 57600},
    'DGP-NE96' :
    {'model' : 'DGP-NE96', 'max zones' : 96, 'max areas' : 8, 'max users' : 999, 'baudrate' : 57600}
    }


