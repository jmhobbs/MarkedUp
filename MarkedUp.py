#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import markdown2

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

style_path = "%s/style.css" % os.path.dirname( os.path.abspath( __file__ ) )

welcome_text = """# Welcome To Markdownr

This is a markdown composition tool written for Qt4.

I hope it is useful to you!
"""

base_html_pre = """<html>
<head>
	<link rel="stylesheet" type="text/css" href="file://%s" />
</head>
<body>
""" % style_path

base_html_post = "</body></html>"

################################################################################

markdown = markdown2.Markdown()

################################################################################

class MarkedUp ( QApplication ):

	def __init__ ( self, argv ):
		QApplication.__init__( self, argv )

		self.window = QWidget()
		self.window.setWindowTitle( "MarkedUp" )
		self.window.resize( 800, 600 )
		self.window.setMinimumWidth( 500 )

		self.layout = QVBoxLayout()
		self.window.setLayout( self.layout )

		self.textArea = QTextEdit()
		self.textArea.setAcceptRichText( False )
		self.textArea.setText( welcome_text )
		self.textArea.setMinimumHeight( 200 )
		self.layout.addWidget( self.textArea )

		self.webview = QWebView()
		self.webview.setMinimumHeight( 200 )
		self.layout.addWidget( self.webview )

		QObject.connect( self.textArea, SIGNAL('textChanged()'), self.update_view )

		self.update_view()
		self.window.show()

	def update_view ( self ):
		self.webview.setHtml(
			'%s%s%s' % (
				base_html_pre,
				markdown.convert( self.textArea.toPlainText() ),
				base_html_post
			)
		);

if __name__ == "__main__":
	app = MarkedUp( sys.argv )
	sys.exit( app.exec_() )