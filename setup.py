# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
	name='MarkedUp',
	version='1.1.0',
	description='Markup File Editor',
	author='John Hobbs',
	author_email='john@velvetcache.org',
	url='http://github.com/jmhobbs/MarkedUp',
	packages=['markedup'],
	scripts=['MarkedUp'],
	data_files=[
		( '/usr/share/markedup/', [ 'resource/icon.64x64.png', 'resource/style.css', 'resource/welcome.md' ] )
	]
)
