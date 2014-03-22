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

from PyQt4.Qt import QDialog, QVBoxLayout, QPushButton, QMessageBox, QLabel

#from calibre_plugins.opml.config import prefs
#
#class DemoDialog(QDialog):
#
#    def __init__(self, gui, icon, do_user_config):
#        QDialog.__init__(self, gui)
#        self.gui = gui
#        self.do_user_config = do_user_config
#
#        # The current database shown in the GUI
#        # db is an instance of the class LibraryDatabase2 from database.py
#        # This class has many, many methods that allow you to do a lot of
#        # things.
#        self.db = gui.current_db
#
#        self.l = QVBoxLayout()
#        self.setLayout(self.l)
#
#        self.label = QLabel(prefs['hello_world_msg'])
#        self.l.addWidget(self.label)
#
#        self.setWindowTitle('OPML Importer')
#        self.setWindowIcon(icon)
#
#        self.about_button = QPushButton('About', self)
#        self.about_button.clicked.connect(self.about)
#        self.l.addWidget(self.about_button)
#
#        self.conf_button = QPushButton(
#                'Configure this plugin', self)
#        self.conf_button.clicked.connect(self.config)
#        self.l.addWidget(self.conf_button)
#
#        self.resize(self.sizeHint())
#
#    def about(self):
#        # Get the about text from a file inside the plugin zip file
#        # The get_resources function is a builtin function defined for all your
#        # plugin code. It loads files from the plugin zip file. It returns
#        # the bytes from the specified file.
#        #
#        # Note that if you are loading more than one file, for performance, you
#        # should pass a list of names to get_resources. In this case,
#        # get_resources will return a dictionary mapping names to bytes. Names that
#        # are not found in the zip file will not be in the returned dictionary.
#        text = get_resources('about.txt')
#        QMessageBox.about(self, 'About the Interface Plugin Demo',
#                text.decode('utf-8'))
#
#    def config(self):
#        self.do_user_config(parent=self)
#        # Apply the changes
#        self.label.setText(prefs['hello_world_msg'])
#

import xml.etree.ElementTree as ET

class OPML(object):

    def __init__(self):
        self.doc = None # xml document
        self.outlines = None # parsed outline objects

    def load(self, filename):
        tree = ET.parse(filename)
        self.doc = tree.getroot()

    def parse(self):
        self.outlines = self.doc.findall(u'body/outline')
        
        return self.outlines

    def unload(self):
        #self.doc.freeDoc()
        pass

if __name__ == '__main__':
    o = OPML();
    o.load('/media/sf_Kenny/Downloads/feedly.opml')
    o.parse()
    print(len(o.outlines))
    for outline in o.outlines:
        print(dir(outline))
    o.unload()

