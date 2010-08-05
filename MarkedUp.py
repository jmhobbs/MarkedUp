#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from PyQt4 import QtCore, QtGui, QtWebKit

from markedup.parsing import Parser
from markedup.curry import Curry

BASE_HTML_PRE = '<html><head><link rel="stylesheet" type="text/css" href="style.css" /></head><body>'
BASE_HTML_POST = '</body></html>'

class MarkedUp ( QtGui.QMainWindow ):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)

		# This is the file path to the currently edited file (None == New File)
		self.file = None
		# This tracks wether modifications have been made since the last save.
		# TODO: It would be cooler to do something with a hash or something, so that
		#       if you edit it back to the original state it would no longer be "unsaved"
		self.saved = False
		# This tracks the current editing language
		self.currentMarkupLanguage = None

		# Prep the window
		self.setWindowTitle( "MarkedUp - [New File] (unsaved)" )
		self.resize( 800, 600 )
		self.setMinimumWidth( 500 )

		# Our central feature is a two-tab widget with editor and view source
		self.tabs = QtGui.QTabWidget()
		self.setCentralWidget( self.tabs )

		# The editor has live preview, so we split this up
		self.splitter = QtGui.QSplitter( QtCore.Qt.Vertical )
		self.tabs.addTab( self.splitter, "Edit" )

		# Source viewer is a standalone tab
		self.sourceArea = QtGui.QTextEdit()
		self.sourceArea.setAcceptRichText( False )
		self.sourceArea.setReadOnly( True )
		self.tabs.addTab( self.sourceArea, "Source" )

		# We only bother updating the source code when it get's switched to
		QtCore.QObject.connect( self.tabs, QtCore.SIGNAL( 'currentChanged(int)' ), self.update_source )

		# Set up the edit box
		self.editArea = QtGui.QTextEdit()
		self.editArea.setAcceptRichText( False )
		self.editArea.setMinimumHeight( 200 )
		self.splitter.addWidget( self.editArea )

		# We render real-time into the WebKit engine
		self.webView = QtWebKit.QWebView()
		self.webView.setMinimumHeight( 200 )
		self.splitter.addWidget( self.webView )

		# To allow for custom styles/images, we get a base URL located in the same directory as the script
		self.base_url = QtCore.QUrl( "file://%s/resource/" % os.path.dirname( os.path.abspath( __file__ ) ) )

		# This Parser object will handle all the markup enumeration and parsing
		self.parser = Parser()

		# Build the toolbar
		self.build_toolbar()

		# We need to default to a language, in case out loading fails
		self.set_markup_language( self.parser.get_available_parsers()[0] )

		# On opening up the system, let's display a welcome message
		# TODO:  If they pass in a CLI file, we should open that instead.
		self.open_file( "%s/resource/welcome.md" % os.path.dirname( os.path.abspath( __file__ ) ) )

		# Any time the text changes, we need to re-parse and update our view
		QtCore.QObject.connect( self.editArea, QtCore.SIGNAL( 'textChanged()' ), self.update_view )

	def build_toolbar ( self ):
		"""Generates the top menu bar."""
		menubar = self.menuBar()
		file_menu = menubar.addMenu( '&File' )

		action = QtGui.QAction( 'Quit', self )
		action.setShortcut( 'Ctrl+Q' )
		action.setStatusTip( 'Quit MarkedUp' )
		self.connect( action, QtCore.SIGNAL( 'triggered()' ), QtCore.SLOT( 'close()' ) )
		file_menu.addAction( action )

		markup_menu = menubar.addMenu( '&Markup' )
		self.markup_menu_items = {}
		# Use the parser object to get the available parsers, and add them to the menu
		for lwm in self.parser.get_available_parsers():
			self.markup_menu_items[lwm] = QtGui.QAction( self.parser.full_name( lwm ), self )
			self.markup_menu_items[lwm].setCheckable( True )
			self.connect( self.markup_menu_items[lwm], QtCore.SIGNAL( 'triggered()' ), Curry( self.set_markup_language, lwm ) )
			markup_menu.addAction( self.markup_menu_items[lwm] )

	def set_markup_language ( self, lwm ):
		"""Set the current editor language."""
		self.currentMarkupLanguage = lwm
		for key, item in self.markup_menu_items.items():
			item.setChecked( key == lwm )
		self.update_view( False )

	def update_view ( self, is_signal=True ):
		"""Parses the content in the edit area and sticks it into the WebKit view."""
		self.statusBar().showMessage( 'Rendering...' )

		if is_signal and self.saved:
			self.saved = False
			self.setWindowTitle( "MarkedUp - %s (unsaved)" % os.path.basename( self.file ) )

		self.webView.setHtml(
			'%s%s%s' % (
				BASE_HTML_PRE,
				self.parser.parse(
					unicode( self.editArea.toPlainText() ),
					self.currentMarkupLanguage
				),
				BASE_HTML_POST
			),
			self.base_url
		);
		self.statusBar().showMessage( '' )

	def update_source ( self, index ):
		"""Updates the source view, if needed."""
		if index == 1:
			self.sourceArea.setPlainText( self.parser.parse( unicode( self.editArea.toPlainText() ), self.currentMarkupLanguage ) )

	def open_file ( self, path ):
		"""Opens a file, detects language (if possible) and loads it into the editor."""
		self.statusBar().showMessage( 'Loading %s' % path )

		try:
			with open( path, 'r' ) as handle:
				self.editArea.setText( handle.read() )
		except IOError, e:
			self.statusBar().showMessage( str( e ) )
			return

		self.saved = True
		self.file = path

		self.statusBar().showMessage( 'Loaded %s' % path )
		self.setWindowTitle( "MarkedUp - %s " % os.path.basename( path ) )

		if ".md" == path[-3:] or ".markdown" == path[-9:]:
			self.set_markup_language( 'markdown' )
		else:
			self.statusBar().showMessage( 'Could not guess file format.' )


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	markedup = MarkedUp()
	markedup.show()
	sys.exit( app.exec_() )