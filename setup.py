'''Used to install when cloned.'''
#!/usr/bin/env python3
from setuptools import setup

setup(name='pyparadox',
      version='0.1.2',
      description='A python3 library for running asynchronous communications with Paradox alarm control panel modules.',
      author='Paul Burger',
      author_email='PollieXmas@icloud.com',
      url='https://github.com/PollieKrismis/pyparadox.git',
      license='MIT',
      packages=['pyparadox'],
      install_requires=['pyserial'],
      classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3.4','Programming Language :: Python :: 3.5']
  )

