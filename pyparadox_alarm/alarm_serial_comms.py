'''
Handles the (usb) serial communication to/from the Paradox alarm panel.

Created on 10 Aug 2016

@author: Paul Burger
'''

import threading
from multiprocessing import Lock
import re
import time
import logging
import serial
from serial.serialutil import SerialException

_LOGGER = logging.getLogger(__name__)

class ParadoxSerialComms:
    '''
    This manages serial communication with the paradox alarm panel by acting as message broker.
    It establishes the connection and handle requests and responses using threads.
    The response thread places messages from the alarm panel on the response queue.
    The request thread submit requests found on the request queue to the alarm panel.
    '''
    def __init__(self, request_queue, response_queue, port, speed):
        self._port = port
        self._speed = speed
        self._pipe = None
        self._lock = None
        self._shutdown = None
        self.request_queue = request_queue
        self.response_queue = response_queue

    def connect(self):
        '''
        Opens a serial connection to the Paradox Alarm Panel.
        To do: Add a loop to attempt a connection several times before giving up.
        '''
        self._lock = Lock() #Does this do anything?

        try:
            self._pipe = serial.Serial(self._port, self._speed, timeout=1)
            self._pipe.flushInput() #Gets rid of /X0 after being disconnected for long?
        except SerialException:
            if self._port is None:
                _LOGGER.error(str.format('Port not configured yet.'))
            else:
                self.reconnect()
        else:
            #Connection should now be open
            self._shutdown = False
            _LOGGER.info(str.format("Connected to Paradox on port: {0}, speed: {1}",
                                    self._port, self._speed))

    def reconnect(self):
        '''Re-opens the serial connection to the Paradox Alarm Panel, only if not open.'''
        if self.is_open() is False:
            try:
                self._pipe.open()
            except SerialException:
                if self._port is None:
                    _LOGGER.error(str.format('Port not configured yet.'))
                else:
                    _LOGGER.error(str.format('Unable to re-open serial connection.'))
        else:
            _LOGGER.info(str.format("Reconnect ignored, port {} already open.", self._port))

    def disconnect(self):
        '''Closes the serial connection to the Paradox Alarm Panel..'''
        self._pipe.close()

    def start(self):
        '''Start threads to manage queues.'''
        self.connect() #Open the serial port before starting the threads
        response_thread = threading.Thread(target=self.get_response)
        response_thread.start()
        request_thread = threading.Thread(target=self.submit_request)
        request_thread.start()
        _LOGGER.debug(str.format('Request and Response threads are running...'))

    def submit_request(self):
        '''
        Submit requests found on the request queue.
        To do: Add a submitted queue to track submitted requests.
               The submitted queue can be used to re-submit requests for which there's no response.
        '''
        _LOGGER.debug(str.format('Waiting for requests...'))
        while not self._shutdown:
            request = self.request_queue.get() + "\r"
            _LOGGER.debug(str.format('TX > {0}', request.encode('ascii')))
            with self._lock:
                self._pipe.write(request.encode('ascii'))
                time.sleep(2)
            self.request_queue.task_done() # Notifies join() that each put() had a get()
        _LOGGER.debug(str.format('Stop submitting requests...'))

    def get_response(self):
        '''Listen for messages from the panel and place them on the response queue (as thread).'''
        _LOGGER.debug(str.format('Listening for alarm panel messages/events...'))
        while not self._shutdown:
            try:
                response = self._pipe.readline().decode().strip() #remove white space
                #time.sleep(0.1) #Keep this until we have the timing sorted
            except EOFError:
                response = "" #force it to ignore this response

            if response != "":
                _LOGGER.debug(str.format('RX > {0}', response.encode('ascii')))
                #Responses may be multi-line...
                responses = re.split('\r', response)
                for item in responses:
                    if item != "":
                        self.response_queue.put(item, timeout=10)
        _LOGGER.debug(str.format('Stop listening to alarm panel messages/events...'))
        #self.responseQueue.task_done() # No need for this as we are only using put()

    def stop(self):
        '''
        Stop the response and request threads as elegantly as possible.
        To do: Wait for the queues to be empty?
               Find a better way to stop the request thread.
               .join() will not be reliable as it is acceptable to get out of sync .put()
        '''
        self._shutdown = True # this should kill the "listen" thread, but not the requester thread
        # submit a dummy request to get the requester thread to evaluate shutdown boolean
        self.request_queue.put("Dummy")
        time.sleep(5) #Wait for the the dummy request to be processed before closing the connection
        self.disconnect()
        #This won't work if some requests are pending;Do we need it?
        #self.request_queue.join() #Can't we just kill the thread?
        _LOGGER.debug(str.format('Threads stopped...'))

    def is_open(self):
        '''Returns True if serial connection is open, otherwise false.'''
        #It's best to test it again rather that use the boolean we set ourselves.
        return self._pipe.isOpen()
