#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import markdown2

from PyQt4 import QtCore, QtGui, QtWebKit

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

class MarkedUp ( QtGui.QMainWindow ):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		self.setWindowTitle( "MarkedUp" )
		self.resize( 800, 600 )
		self.setMinimumWidth( 500 )

		self.layout = QtGui.QVBoxLayout()

		self.wrapper = QtGui.QWidget()
		self.wrapper.setLayout( self.layout )
		self.setCentralWidget( self.wrapper )

		self.textArea = QtGui.QTextEdit()
		self.textArea.setAcceptRichText( False )
		self.textArea.setText( welcome_text )
		self.textArea.setMinimumHeight( 200 )
		self.layout.addWidget( self.textArea )

		self.webview = QtWebKit.QWebView()
		self.webview.setMinimumHeight( 200 )
		self.layout.addWidget( self.webview )

		QtCore.QObject.connect( self.textArea, QtCore.SIGNAL( 'textChanged()' ), self.update_view )

		self.build_menu()
		self.update_view()

	def build_menu ( self ):
		action = QtGui.QAction( QtGui.QIcon( 'icons/exit.png' ), 'Quit', self )
		action.setShortcut( 'Ctrl+Q' )
		action.setStatusTip( 'Quit application' )
		self.connect( action, QtCore.SIGNAL( 'triggered()' ), QtCore.SLOT( 'close()' ) )

		menubar = self.menuBar()
		file_menu = menubar.addMenu( '&File' )
		file_menu.addAction( action )

	def update_view ( self ):
		self.statusBar().showMessage( 'Rendering...' )
		self.webview.setHtml(
			'%s%s%s' % (
				base_html_pre,
				markdown.convert( self.textArea.toPlainText() ),
				base_html_post
			)
		);
		self.statusBar().showMessage( '' )

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	markedup = MarkedUp()
	markedup.show()
	sys.exit( app.exec_() )