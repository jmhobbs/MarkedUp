#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit

from markedup.parsing import Parser

base_html_pre = '<html><head><link rel="stylesheet" type="text/css" href="style.css" /></head><body>'
base_html_post = '</body></html>'

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
		self.textArea.setMinimumHeight( 200 )
		self.layout.addWidget( self.textArea )

		self.webview = QtWebKit.QWebView()
		self.webview.setMinimumHeight( 200 )
		self.layout.addWidget( self.webview )

		self.base_url = QtCore.QUrl( "file://%s/" % os.path.dirname( os.path.abspath( __file__ ) ) )

		self.parser = Parser()
		self.build_menu()

		self.file = None
		self.saved = True
		self.file_format = None
		self.open_file( "%s/welcome.md" % os.path.dirname( os.path.abspath( __file__ ) ) )

		QtCore.QObject.connect( self.textArea, QtCore.SIGNAL( 'textChanged()' ), self.update_view )

	def build_menu ( self ):
		action = QtGui.QAction( QtGui.QIcon( 'icons/exit.png' ), 'Quit', self )
		action.setShortcut( 'Ctrl+Q' )
		action.setStatusTip( 'Quit application' )
		self.connect( action, QtCore.SIGNAL( 'triggered()' ), QtCore.SLOT( 'close()' ) )

		menubar = self.menuBar()
		file_menu = menubar.addMenu( '&File' )
		file_menu.addAction( action )

	def update_view ( self, is_signal=True ):
		self.statusBar().showMessage( 'Rendering...' )

		if is_signal and self.saved:
			self.saved = False
			self.setWindowTitle( "MarkedUp - %s (Modified)" % os.path.basename( self.file ) )

		self.webview.setHtml(
			'%s%s%s' % (
				base_html_pre,
				self.parser.parse( self.textArea.toPlainText(), self.file_format ),
				base_html_post
			),
			self.base_url
		);
		self.statusBar().showMessage( '' )

	def open_file ( self, path ):
		self.statusBar().showMessage( 'Loading %s' % path )
		if ".md" == path[-3:] or ".markdown" == path[-9:]:
			self.file_format = 'markdown'
		else:
			self.statusBar().showMessage( 'Unknown File Format: %s' % path )
			return False

		self.saved = True
		self.file = path
		with open( self.file, 'r' ) as handle:
			self.textArea.setText( handle.read() )

		self.update_view( False )
		self.statusBar().showMessage( 'Loaded %s' % path )
		self.setWindowTitle( "MarkedUp - %s " % os.path.basename( path ) )

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	markedup = MarkedUp()
	markedup.show()
	sys.exit( app.exec_() )