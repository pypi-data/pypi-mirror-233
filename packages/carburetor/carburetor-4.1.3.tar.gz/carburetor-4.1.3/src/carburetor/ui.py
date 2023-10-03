#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022.

"""
handle ui related stuff
"""

import gi

gi.require_versions({"Gtk": "4.0"})
from gi.repository import Gdk, Gtk

from . import config
from . import handler

builder = Gtk.Builder(scope_object_or_map=handler)
ui_dir = config.s_data_dir + "/ui"


def initialize_builder() -> None:
    """
    connect builder to files and handlers
    """
    builder.add_from_file(ui_dir + "/about.ui")
    builder.add_from_file(ui_dir + "/preferences.ui")
    builder.add_from_file(ui_dir + "/main.ui")


def get(obj: str):
    """
    get object from ui
    """
    return builder.get_object(obj)


def css() -> None:
    """
    apply css to ui
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(ui_dir + "/style.css")
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
