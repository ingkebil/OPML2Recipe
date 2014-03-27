OPML2Recipe
===========

Plugin for Calibre: imports an OPML file as a news recipe.

The calibre OPML Import Plugin is (is under review and will soon be) distributed from the MobileRead Forums with the other calibre plugins.

Main Features
-------------

Import RSS feeds as an OPML file from feedly or google reader.
This plugin will create a recipe for each group and each remaining feed.
So far a restart is required to have the imported RSS feeds show up in custom news sources.

Version History
---------------
* Version 1.0.1: MessageBox appears on succesful completion.
* Version 1.0.0: Created a working import plugin + configuration of oldest article and max articles.

Special Notes
-------------

Requires calibre version 0.7.53 or later.
A restart is still required once the RSS feeds have been imported!

Installation Notes
------------------

Download the zip file, unpack it and zip only the contents of the OPML2Recipe directory. Install the plugin: preferences -> plugins -> load from file. Selet the newly created zip file.
Restart calibre.
Customize the plugin via Preferences -> Plugins or through the configure button of the plugin.

Usage
-----

Set the max articles and oldest article preferences. If not set, the defaults will be used.
Hit the 'import' button, select the OPML files you want to import.
Restart calibre to have the imported RSS feeds show up in custom news sources.
