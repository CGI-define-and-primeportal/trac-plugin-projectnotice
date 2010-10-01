#!/usr/bin/env python

from setuptools import find_packages, setup

version='0.1'

setup(name='ProjectNoticePlugin',
      version=version,
      description="Apply a notice to a project",
      long_description="This plugin allows you to apply a textual notice to a project.",
      author='Adam Piper',
      author_email='adam.piper@logica.com',
      url='',
      keywords='trac plugin project notice',
      license="BSD-3",
      install_requires = [ 'Trac>=0.11'],
      packages=find_packages(exclude=['ez_setup', 'examples', '*tests*']),
      include_package_data=True,
      package_data={ 'projectnotice': [
          'templates/*.html',
          'htdocs/css/*.css',
          ] },
      zip_safe=True,
      entry_points={'trac.plugins': [
            'projectnotice.api = projectnotice.api',
            'projectnotice.web_ui = projectnotice.web_ui'
            ]},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Trac',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: 3 Clause BSD (BSD-3)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Bug Tracking',
          'Topic :: System :: Project Notice',
          'Topic :: System :: Systems Administration',
          ],
      )
