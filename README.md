# MarkedUp

MarkedUp is a simple Qt4 application for editing various markup languages with real-time rendering.

I wrote this because I only touch Markdown once in a while, and I'm always forgetting syntax.

## Screenshot!

![Alt text](http://static.velvetcache.org/pages/2010/08/05/markedup-the-power-of-python/marked-up-edit.png)

## Requirements

* [PyQt4](http://www.riverbankcomputing.co.uk/news) With WebKit support
* Packages for the dialects you want (see below)
* A modern Python installation (2.x series)

## Dialects

MarkedUp speaks several dialects of markup.  It will detect which ones your system supports at run-time.

### Implemented

* [Markdown](http://daringfireball.net/projects/markdown/)
  * via [python-markdown2](http://code.google.com/p/python-markdown2/)
  * *easy_install markdown2*
* [Textile](http://www.textism.com/tools/textile/)
  * via [PyTextile](http://github.com/jsamsa/python-textile)
  * *easy_install textile*
* [BBCode](http://www.phpbb.com/community/faq.php?mode=bbcode)
  * via [postmarkup](http://code.google.com/p/postmarkup/)
  * *easy_install postmarkup*
* [Creole](http://www.wikicreole.org/)
  * via [python-creole](http://code.google.com/p/python-creole/)
  * *easy_install **python-creole***

### Coming Soon

* None - Suggest one and I'll build it in!

## Features

* Instant Preview
* Four Different Languages
* Custom Stylesheets
* Export Rendered HTML

## Installing

    # git clone git://github.com/jmhobbs/MarkedUp.git
    # sudo python setup.py install

It's that easy.
