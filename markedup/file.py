# -*- coding: utf-8 -*-

import os.path

class MarkedUpFile ( object ):

	def __init__ ( self, path=None ):

		self.language = None
		self.path = None

		if path:
			self.set_path( path )

	def set_path ( self, path ):
		self.path = os.path.abspath( path )
		if '.md' == self.path[-3:] or '.markdown' == self.path[-9:]:
			self.language = 'markdown'
		elif '.bbcode' == self.path[-7:]:
			self.language = 'bbcode'
		elif '.textile' == self.path[-8:]:
			self.language = 'textile'
		else:
			self.language = None

	def get_contents ( self ):
		with open( self.path, 'r' ) as handle:
			contents = handle.read()
		return contents

	def put_contents ( self, contents ):
		with open( self.path, 'w' ) as handle:
			handle.write( contents )