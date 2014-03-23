#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2014, Kenny Billiau <kennybilliau@gmail.com>'
__docformat__ = 'restructuredtext en'

if False:
    # This is here to keep my python error checker from complaining about
    # the builtin functions that will be defined by the plugin loading system
    # You do not need this code in your plugins
    get_icons = get_resources = None

import time

from PyQt4.Qt import (QDialog, QGridLayout, QPushButton, QMessageBox, QLabel,
        QWidget, QVBoxLayout, QLineEdit, QIcon, QDialogButtonBox, QTimer,
        QScrollArea, QSize)

from calibre_plugins.opml.config import prefs

class Path(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ll = ll = QGridLayout()
        self.setLayout(self.ll)

        self.labell = QLabel('Title:')
        ll.addWidget(self.labell, 0, 0, 1, 1)
        self.title_edit = QLineEdit(self)
        self.title_edit.setPlaceholderText('Enter path to OPML')
        ll.addWidget(self.title_edit, 0, 1, 1, 1)

    @property
    def title(self):
        return unicode(self.title_edit.text())

class DemoDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        # The current database shown in the GUI
        # db is an instance of the class LibraryDatabase2 from database.py
        # This class has many, many methods that allow you to do a lot of
        # things.
        self.db = gui.current_db

        self.l = QVBoxLayout()
        self.setLayout(self.l)

        self.label = QLabel(prefs['hello_world_msg'])
        self.l.addWidget(self.label)

        self.setWindowTitle('OPML Importer')
        self.setWindowIcon(icon)

        self.import_button = QPushButton('Import', self)
        self.import_button.clicked.connect(self.import_opml)
        self.l.addWidget(self.import_button)

        self.conf_button = QPushButton(
                'Configure this plugin', self)
        self.conf_button.clicked.connect(self.config)
        self.l.addWidget(self.conf_button)

        self.resize(self.sizeHint())

    def import_opml(self):
        opml = OPML();
        opml.load('/media/sf_Kenny/Downloads/feedly.opml')
        outlines = opml.parse()
        opml.import_recipes(outlines)

    def config(self):
        self.do_user_config(parent=self)
        # Apply the changes
        self.label.setText(prefs['hello_world_msg'])


# http://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
from calibre.web.feeds.recipes import compile_recipe, custom_recipes
from calibre.gui2 import error_dialog

class OPML(object):

    def __init__(self):
        self.doc = None # xml document
        self.outlines = None # parsed outline objects
        self.oldest_article = 7
        self.max_articles = 100

    def load(self, filename):
        tree = ET.parse(filename)
        self.doc = tree.getroot()

    def parse(self):
        self.outlines = self.doc.findall(u"body/outline")

        for outline in self.outlines: # check for groups
            if ('type' not in outline.attrib):
                feeds = [] # title, xmlUrl
                for feed in outline.iter('outline'):
                    if 'type' in feed.attrib:
                        feeds.append( (feed.get('title'), feed.get('xmlUrl')) )
                outline.set('xmlUrl', feeds)
        
        return self.outlines

    def import_recipes(self, outlines):
        for outline in outlines:
            src, title = self.options_to_profile(dict(
                title=repr(outline.get('title')),
                feeds=repr(outline.get('xmlUrl')),
                oldest_article=self.oldest_article,
                max_articles=self.max_articles,
                base_class='AutomaticNewsRecipe'
            ))
            try:
                compile_recipe(src)
                error_dialog(None, 'Works', src).exec_()
            except Exception as err:
                error_dialog(None, _('Invalid input'),
                    _('<p>Could not create recipe. Error:<br>%s')%str(err)).exec_()

    def options_to_profile(self, recipe):
        classname = 'BasicUserRecipe'+str(int(time.time()))
        title = recipe.get('title').strip()
        if not title:
            title = classname
        oldest_article = self.oldest_article
        max_articles   = self.max_articles
        if not isinstance(recipe.get('feeds'), str):
            feeds = [i.user_data for i in recipe.get('feeds').items()]
        else:
            feeds = recipe.get('feeds')

        src = '''\
class %(classname)s(%(base_class)s):
    title          = %(title)s
    oldest_article = %(oldest_article)d
    max_articles_per_feed = %(max_articles)d
    auto_cleanup = True

    feeds          = %(feeds)s
'''%dict(classname=classname, title=repr(title),
                 feeds=repr(feeds), oldest_article=oldest_article,
                 max_articles=max_articles,
                 base_class='AutomaticNewsRecipe')
        return src, title

    def add_profile(self, clicked):
        if self.stacks.currentIndex() == 0:
            src, title = self.options_to_profile()

            try:
                compile_recipe(src)
            except Exception as err:
                error_dialog(self, _('Invalid input'),
                        _('<p>Could not create recipe. Error:<br>%s')%str(err)).exec_()
                return

if __name__ == '__main__':
    opml = OPML();
    opml.load('/media/sf_Kenny/Downloads/feedly.opml')
    outlines = opml.parse()
    print(len(opml.outlines))
    opml.import_recipes(outlines)

