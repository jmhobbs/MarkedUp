# -*- coding: utf-8 -*-

class Parser ( object ):

	def __init__ ( self ):
		self.parsers = {}

		try:
			import markdown2
			self.parsers['markdown'] = markdown2.markdown
		except ImportError, e:
			pass

		try:
			import textile
			self.parsers['textile'] = textile.textile
		except ImportError, e:
			pass

		try:
			from postmarkup import render_bbcode
			self.parsers['bbcode'] = render_bbcode
		except ImportError, e:
			pass

		try:
			from creole import creole2html
			self.parsers['creole'] = creole2html
		except ImportError, e:
			pass

	def get_available_parsers ( self ):
		return self.parsers.keys()

	def parse ( self, markup, parser ):
		return self.parsers[parser]( markup )

if __name__ == "__main__":
	x = Parser()
	print "Parsers:", x.get_available_parsers()
	print "MARKDOWN"
	print x.parse( "**Bold**", "markdown" ).strip()
	print "TEXTILE"
	print x.parse( "*Bold*", "textile" ).strip()
	print "BBCODE"
	print x.parse( "[b]Bold[/b]", "bbcode" ).strip()
	print "CREOLE"
	print x.parse( u'**Bold**', "creole" ).strip()
