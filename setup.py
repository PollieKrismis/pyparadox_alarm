'''Used to install when cloned.'''
from setuptools import setup

setup(name='pyparadox-alarm',
      version='0.0.1',
      description='Paradox Interface Library and Server',
      author='Paul Burger',
      author_email='PollieXmas@icloud.com',
      url='https://github.com/PollieKrismis/pyparadox-alarm.git',
      packages=['paradox'],
      install_requires=['pyserial'],
      scripts=['test']
  )
