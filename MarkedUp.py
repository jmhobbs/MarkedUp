#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit

from markedup.parsing import Parser
from markedup.curry import Curry

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
		menubar = self.menuBar()
		file_menu = menubar.addMenu( '&File' )

		action = QtGui.QAction( QtGui.QIcon( 'icons/exit.png' ), 'Quit', self )
		action.setShortcut( 'Ctrl+Q' )
		action.setStatusTip( 'Quit application' )
		self.connect( action, QtCore.SIGNAL( 'triggered()' ), QtCore.SLOT( 'close()' ) )
		file_menu.addAction( action )

		markup_menu = menubar.addMenu( '&Markup' )

		self.markup_menu_items = {}

		for lwm in self.parser.get_available_parsers():
			self.markup_menu_items[lwm] = QtGui.QAction( self.parser.full_name( lwm ), self )
			self.markup_menu_items[lwm].setCheckable( True )
			self.connect( self.markup_menu_items[lwm], QtCore.SIGNAL( 'triggered()' ), Curry( self.set_format, lwm ) )
			markup_menu.addAction( self.markup_menu_items[lwm] )

	def set_format ( self, lwm ):
		self.file_format = lwm
		for key, item in self.markup_menu_items.items():
			item.setChecked( key == lwm )
		self.update_view( False )

	def update_view ( self, is_signal=True ):
		self.statusBar().showMessage( 'Rendering...' )

		if is_signal and self.saved:
			self.saved = False
			self.setWindowTitle( "MarkedUp - %s (Modified)" % os.path.basename( self.file ) )

		self.webview.setHtml(
			'%s%s%s' % (
				base_html_pre,
				self.parser.parse( unicode( self.textArea.toPlainText() ), self.file_format ),
				base_html_post
			),
			self.base_url
		);
		self.statusBar().showMessage( '' )

	def open_file ( self, path ):
		self.statusBar().showMessage( 'Loading %s' % path )

		self.saved = True
		self.file = path
		with open( self.file, 'r' ) as handle:
			self.textArea.setText( handle.read() )

		self.statusBar().showMessage( 'Loaded %s' % path )
		self.setWindowTitle( "MarkedUp - %s " % os.path.basename( path ) )

		if ".md" == path[-3:] or ".markdown" == path[-9:]:
			self.set_format( 'markdown' )
		else:
			self.statusBar().showMessage( 'Could not guess file format.' )


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	markedup = MarkedUp()
	markedup.show()
	sys.exit( app.exec_() )