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

markdown = markdown2.Markdown()

app = QApplication( sys.argv )

window = QWidget()
layout = QVBoxLayout()

window.setLayout( layout )
window.setWindowTitle( "Markdownr" )
window.resize( 800, 600 )
window.setMinimumWidth( 500 )

text = QTextEdit()
text.setAcceptRichText( False )
text.setText( welcome_text )
text.setMinimumHeight( 200 )
layout.addWidget( text )

web = QWebView()
web.setMinimumHeight( 200 )
layout.addWidget( web )

def updateHTML ():
	web.setHtml( '%s%s%s' % ( base_html_pre, markdown.convert( text.toPlainText() ), base_html_post ) );

QObject.connect( text, SIGNAL('textChanged()'), updateHTML )

updateHTML()

window.show()

sys.exit( app.exec_() )