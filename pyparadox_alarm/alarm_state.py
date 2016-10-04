'''Class that defines a dictionary to be used to mirror the alarm state.'''
#Derived from https://github.com/Cinntax/pyenvisalink/blob/master/pyenvisalink/alarm_state.py

class AlarmState:
    '''Helper class for alarm state functionality.'''

    @staticmethod
    def get_initial_alarm_state(max_zones, max_partitions):
        '''Builds the proper alarm state collection.'''

        _alarm_state = {'partition': {}, 'zone': {}}

        for i in range(1, max_partitions + 1):
            #Are all these dictionary items needed by Home Assistant?
            _default_area_label = 'Area ' + str(i) + ' label default'
            _alarm_state['partition'][i] = {'status': {'alarm': False, 'alarm_in_memory': False,
                                                        'armed_away': False, 'ac_present': False,
                                                        'armed_bypass': False, 'chime': False,
                                                        'armed_zero_entry_delay': False,
                                                        'alarm_fire_zone': False, 'trouble': False,
                                                        'ready': False, 'fire': False,
                                                        'armed_stay': False, 'alpha': False,
                                                        'beep': False,
                                                        'exit_delay': False, 'entry_delay': False,},
                                            'name': _default_area_label}
        for j in range(1, max_zones + 1):
            _default_zone_label = 'Zone ' + str(j) + ' label default'
            _alarm_state['zone'][j] = {'status': {'open': False, 'fault': False, 'alarm': False,
                                                    'tamper': False},
                                       'last_fault': 0,
                                       'name': _default_zone_label}

        return _alarm_state
