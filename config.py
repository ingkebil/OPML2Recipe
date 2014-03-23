#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2014, Kenny Billiau <kennybilliau@gmail.com>'
__docformat__ = 'restructuredtext en'

from PyQt4.Qt import QWidget, QHBoxLayout, QLabel, QLineEdit

from calibre.utils.config import JSONConfig

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/opml')

# Set defaults
prefs.defaults['oldest_article'] = '7'
prefs.defaults['max_articles'] = '100'

class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QHBoxLayout()
        self.setLayout(self.l)

        self.oldest_articlel = QLabel('Oldest article:')
        self.l.addWidget(self.oldest_articlel)

        self.oldest_article_msg = QLineEdit(self)
        self.oldest_article_msg.setText(prefs['oldest_article'])
        self.l.addWidget(self.oldest_article_msg)
        self.oldest_articlel.setBuddy(self.oldest_article_msg)

        self.max_articlesl = QLabel('Max articles:')
        self.l.addWidget(self.max_articlesl)

        self.max_articles_msg = QLineEdit(self)
        self.max_articles_msg.setText(prefs['max_articles'])
        self.l.addWidget(self.max_articles_msg)
        self.max_articlesl.setBuddy(self.max_articles_msg)

    def save_settings(self):
        prefs['oldest_article'] = unicode(self.oldest_article_msg.text())
        prefs['max_articles'] = unicode(self.max_articles_msg.text())

