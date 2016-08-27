"""Default values specific to a Paradox Alarm Panel."""

#Message prefixes
AREA_LABEL_REQUEST = "AL"
AREA_STATUS_REQUEST = "AR"
ZONE_LABEL_REQUEST = "ZL"
ZONE_STATUS_REQUEST = "RZ"

PARADOX_MODELS = {
    'EVO48' :
    {'Model' : 'EVO48', 'MaxZones' : 12, 'MaxAreas' : 4, 'MaxUsers' : 6, 'Baudrate' : 57600},
    'EVO96' :
    {'Model' : 'EVO96', 'MaxZones' : 96, 'MaxAreas' : 8, 'MaxUsers' : 999, 'Baudrate' : 57600},
    'EVO192' :
    {'Model' : 'EVO192', 'MaxZones' : 192, 'MaxAreas' : 8, 'MaxUsers' : 999, 'Baudrate' : 57600},
    'DGP-848' :
    {'Model' : 'DGP-848', 'MaxZones' : 48, 'MaxAreas' : 4, 'MaxUsers' : 96, 'Baudrate' : 57600},
    'DGP-NE96' :
    {'Model' : 'DGP-NE96', 'MaxZones' : 96, 'MaxAreas' : 8, 'MaxUsers' : 999, 'Baudrate' : 57600}
    }


