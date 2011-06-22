# -*- coding: utf-8 -*-

class ParserNotFoundError ( RuntimeError ):
	
	def __init__ ( self, parser ):
		RuntimeError.__init__( self, "Parser '%s' not found." % parser )

class Parser ( object ):

	def __init__ ( self ):
		self.parsers = {}

		try:
			import markdown	
			self.parsers['markdown'] = markdown.markdown
		except ImportError:
			try:
				import markdown2
				self.parsers['markdown'] = markdown2.markdown
			except ImportError:
				pass

		try:
			import textile
			self.parsers['textile'] = textile.textile
		except ImportError:
			pass

		try:
			from postmarkup import render_bbcode
			self.parsers['bbcode'] = render_bbcode
		except ImportError:
			pass

		try:
			from creole import creole2html
			self.parsers['creole'] = creole2html
		except ImportError:
			pass

	def get_available_parsers ( self ):
		return self.parsers.keys()

	def parse ( self, markup, parser ):
		if parser in self.parsers.keys():
			return self.parsers[parser]( markup )
		else:
			raise ParserNotFoundError( parser )

	def full_name ( self, parser ):
		names = {
			'markdown': 'Markdown',
			'textile': 'Textile',
			'bbcode': 'BBCode',
			'creole': 'Creole'
		}
		return names[parser]

if __name__ == "__main__":
	x = Parser()
	print "Parsers:", x.get_available_parsers()
	print "MARKDOWN"
	try:
		print x.parse( "**Bold**", "markdown" ).strip()
	except ParserNotFoundError:
		print "Parser Not Intalled"
	print "TEXTILE"
	try:
		print x.parse( "*Bold*", "textile" ).strip()
	except ParserNotFoundError:
		print "Parser Not Intalled"
	print "BBCODE"
	try:
		print x.parse( "[b]Bold[/b]", "bbcode" ).strip()
	except ParserNotFoundError:
		print "Parser Not Intalled"
	print "CREOLE"
	try:
		print x.parse( u'**Bold**', "creole" ).strip()
	except ParserNotFoundError:
		print "Parser Not Intalled"

