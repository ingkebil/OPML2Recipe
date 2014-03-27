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

from PyQt4.Qt import (QDialog, QGridLayout, QPushButton, QLabel,
        QWidget, QVBoxLayout, QLineEdit, QAbstractListModel)

from calibre_plugins.opml.config import prefs

# http://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
from calibre.web.feeds.recipes import compile_recipe
from calibre.gui2 import error_dialog, choose_files
from calibre.web.feeds.recipes.collection import add_custom_recipe
from calibre.gui2.dialogs.message_box import MessageBox
from calibre.web.feeds.recipes.model import RecipeModel

class CustomRecipeModel(QAbstractListModel):

    def __init__(self, recipe_model):
        QAbstractListModel.__init__(self)
        self.recipe_model = recipe_model

    def add(self, title, script):
        self.recipe_model.add_custom_recipe(title, script)
        self.reset()

class OldestArticle(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ll = ll = QGridLayout()
        self.setLayout(self.ll)

        self.labell = QLabel('Oldest article:')
        ll.addWidget(self.labell, 0, 0, 1, 1)
        self.oldest_article_edit = QLineEdit(self)
        self.oldest_article_edit.setPlaceholderText(prefs['oldest_article'])
        ll.addWidget(self.oldest_article_edit, 0, 1, 1, 1)
        
    @property
    def oldest_article(self):
        return int(self.oldest_article_edit.text() or prefs['oldest_article'])       

class MaxArticles(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ll = ll = QGridLayout()
        self.setLayout(self.ll)

        self.labell = QLabel('Max articles:')
        ll.addWidget(self.labell, 0, 0, 1, 1)
        self.max_articles_edit = QLineEdit(self)
        self.max_articles_edit.setPlaceholderText(prefs['max_articles'])
        ll.addWidget(self.max_articles_edit, 0, 1, 1, 1)
        
    @property
    def max_articles(self):
        return int(self.max_articles_edit.text() or prefs['max_articles'])       

class OPMLDialog(QDialog):

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

        self.setWindowTitle('OPML Importer')
        self.setWindowIcon(icon)

        self.oldest_article = oldest_article = OldestArticle(self)
        self.l.addWidget(self.oldest_article)

        self.max_articles = max_articles = MaxArticles(self)
        self.l.addWidget(self.max_articles)

        self.import_button = QPushButton('Import', self)
        self.import_button.clicked.connect(self.import_opml)
        self.l.addWidget(self.import_button)

        self.conf_button = QPushButton(
                'Configure this plugin', self)
        self.conf_button.clicked.connect(self.config)
        self.l.addWidget(self.conf_button)

        self.resize(self.sizeHint())

    def config(self):
         self.do_user_config(parent=self)
         # Apply the changes
         self.oldest_article.oldest_article_edit.setPlaceholderText(prefs['oldest_article'])
         self.max_articles.max_articles_edit.setPlaceholderText(prefs['max_articles'])

    def import_opml(self):
        opml_files = choose_files(self, 'OPML chooser dialog',
                _('Select OPML file'), filters=[(_('OPML'), ['opml'])] )

        if not opml_files:
            return
        
        opml = OPML(self.oldest_article.oldest_article, self.max_articles.max_articles);
        for opml_file in opml_files:
            opml.load(opml_file)
            outlines = opml.parse()
            opml.import_recipes(outlines)

        # show a messagebox statingthat import finished
        msg_box = MessageBox(MessageBox.INFO, "Finished", "OPML to Recipe conversion complete", parent=self,
                    show_copy_button=False)
        msg_box.exec_()

class OPML(object):

    def __init__(self, oldest_article = 7, max_articles = 100):
        self.doc = None # xml document
        self.outlines = None # parsed outline objects
        self.oldest_article = oldest_article
        self.max_articles = max_articles

    def load(self, filename):
        tree = ET.parse(filename)
        self.doc = tree.getroot()

    def parse(self):
        self.outlines = self.doc.findall(u"body/outline")

        for outline in self.outlines: # check for groups
            #if ('type' not in outline.attrib):
                feeds = [] # title, url
                for feed in outline.iter('outline'):
                    if 'type' in feed.attrib:
                        feeds.append( (feed.get('title'), feed.get('xmlUrl')) )
                outline.set('xmlUrl', feeds)
        
        return self.outlines

    def import_recipes(self, outlines):
        nr = 0
        recipe_model = CustomRecipeModel(RecipeModel())
        for outline in outlines:
            src, title = self.options_to_profile(dict(
                nr=nr,
                title=unicode(outline.get('title')),
                feeds=outline.get('xmlUrl'),
                oldest_article=self.oldest_article,
                max_articles=self.max_articles,
                base_class='AutomaticNewsRecipe'
            ))
            try:
                compile_recipe(src)
                add_custom_recipe(title, src)
            except Exception as err:
                # error dialog should be placed somewhere where it can have a parent
                # Left it here as this way only failing feeds will silently fail
                error_dialog(None, _('Invalid input'),
                    _('<p>Could not create recipe. Error:<br>%s')%str(err)).exec_()
            nr+=1

            recipe_model.add(title, src)


    def options_to_profile(self, recipe):
        classname = 'BasicUserRecipe'+str(recipe.get('nr'))+str(int(time.time()))
        title = recipe.get('title').strip()
        if not title:
            title = classname
        oldest_article = self.oldest_article
        max_articles   = self.max_articles
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

if __name__ == '__main__':
    opml = OPML();
    opml.load('/media/sf_Kenny/Downloads/feedly.opml')
    outlines = opml.parse()
    print(len(opml.outlines))
    opml.import_recipes(outlines)


