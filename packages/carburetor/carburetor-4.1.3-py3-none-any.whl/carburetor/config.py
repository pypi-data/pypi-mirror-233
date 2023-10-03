#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022.


"""
main configurations for carburetor
"""

import ctypes
import gettext
import locale
import os
import sys

import gi

gi.require_versions({"Adw": "1"})
from gi.repository import Gio, GLib, Adw


dconf = Gio.Settings.new("org.tractor")
s_data_dir = os.path.dirname(os.path.abspath(__file__))
locale_dir = s_data_dir + "/locales"
locale.setlocale(locale.LC_ALL, "")
if hasattr(locale, "bindtextdomain"):
    libintl = locale
elif os.name == "nt":
    libintl = ctypes.cdll.LoadLibrary("libintl-8.dll")
elif sys.platform == "darwin":
    libintl = ctypes.cdll.LoadLibrary("libintl.dylib")
libintl.bindtextdomain("carburetor", locale_dir)
gettext.bindtextdomain("carburetor", locale_dir)
libintl.textdomain("carburetor")
gettext.textdomain("carburetor")
_ = gettext.gettext
COMMAND = "tractor"
app_name = _("Carburetor")

GLib.set_application_name(app_name)
Adw.init()
