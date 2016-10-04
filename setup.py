'''Used to install when cloned.'''
#!/usr/bin/env python3
from setuptools import setup

setup(name='pyparadox_alarm',
      version='1.0.0',
      description='A python3 library for running asynchronous communications with Paradox alarm control panel modules.',
      author='Paul Burger',
      author_email='PollieXmas@icloud.com',
      url='https://github.com/PollieKrismis/pyparadox_alarm.git',
      license='MIT',
      packages=['pyparadox_alarm'],
      install_requires=['pyserial'],
      classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3.4','Programming Language :: Python :: 3.5']
  )

