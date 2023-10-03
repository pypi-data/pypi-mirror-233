#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2022.

"""
actions for carburetor
"""

import os
import re
import signal

import gi

gi.require_versions({"Adw": "1"})
from gi.repository import Gio, Adw

from . import config
from . import tasks
from . import ui


def add(name: str, function, app) -> None:
    """
    adds functions to app as actions
    """
    action = Gio.SimpleAction.new(name, None)
    action.connect("activate", function, app)
    app.add_action(action)


def do_startup(app) -> None:
    """
    actions to do when starting the app up
    """
    add("preferences", on_preferences, app)
    add("about", on_about, app)
    add("quit", on_quit, app)
    add("connect", on_connect, app)
    add("new_id", on_new_id, app)
    add("check_connection", on_check, app)
    add("toggle_proxy", on_toggle_proxy, app)
    add("cancel", on_cancel, app)
    add("save", on_save, app)


def on_preferences(*argv) -> None:
    """
    show the preferences window
    """
    app = argv[2]
    if not app.prefs:
        prefs_window = ui.get("PreferencesWindow")
        prefs_window.set_transient_for(app.window)
        app.prefs = prefs_window
    app.prefs.show()


def on_about(*argv) -> None:
    """
    show the about window
    """
    app = argv[2]
    if not app.about:
        about_dialog = ui.get("AboutDialog")
        about_dialog.set_transient_for(app.window)
        app.about = about_dialog
    app.about.show()


def on_quit(*argv) -> None:
    """
    exit the app
    """
    app = argv[2]
    app.quit()


def on_connect(*argv) -> None:
    """
    clicking on connect button
    """
    app = argv[2]
    button = ui.get("SplitButton")
    button.set_sensitive(False)
    progress_bar = ui.get("ProgressBar")
    set_progress(0)
    progress_bar.show()
    cancel_button = ui.get("CancelButton")
    cancel_button.set_visible(True)
    page = ui.get("MainPage")
    page.set_icon_name("image-loading-symbolic")
    if tasks.is_running():
        text_stopping = config._("Disconnecting…")
        page.set_title(text_stopping)
        action = "stop"
    else:
        text_starting = config._("Connecting…")
        page.set_title(text_starting)
        action = "start"
    tasks.connect(action, app)


def on_new_id(*_, **__) -> None:
    """
    clicking on new id button
    """
    if tasks.is_running():
        tasks.new_id()
        toast = config._("You have a new identity!")
    else:
        toast = config._("Tractor is not running!")
    notify(toast)


def on_check(*_, **__) -> None:
    """
    checks if tractor is connected or not
    """
    tasks.is_connected()


def on_toggle_proxy(*_, **__) -> None:
    """
    toggle proxy mode on system
    """
    if tasks.is_proxy_set():
        tasks.set_proxy("unset")
        toast = "Proxy has been unset"
    else:
        tasks.set_proxy("set")
        toast = "Proxy has been set"
    notify(toast)


def on_cancel(*_, **__) -> None:
    """
    abort the connection
    """
    dconf = config.dconf
    pid = dconf.get_int("pid")
    os.killpg(os.getpgid(pid), signal.SIGTERM)
    dconf.reset("pid")


def on_save(*_, **__) -> None:
    """
    clicking on save button in bridges
    """
    textview = ui.get("BridgesTextView")
    buff = textview.get_buffer()
    text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), 0)
    regex = re.compile(r"^( )*([Bb][Rr][Ii][Dd][Gg][Ee])?( )*", re.MULTILINE)
    bridges_file = tasks.get_bridges_file()
    if text == regex.sub("Bridge ", text):
        with open(bridges_file, "w", encoding="utf-8") as file:
            file.write(text)
    else:
        dialog = ui.get("BridgErrorDialog")
        dialog.show()


def set_description(text: str) -> None:
    """
    set description on main page
    """
    page = ui.get("MainPage")
    page.set_description(text)


def set_progress(percentage: int) -> None:
    """
    set progressbar percentage
    """
    progress_bar = ui.get("ProgressBar")
    fraction = float(percentage) / 100
    progress_bar.set_fraction(fraction)


def notify(text: str) -> None:
    """
    show toast
    """
    overlay = ui.get("ToastOverlay")
    toast = Adw.Toast()
    toast.set_title(text)
    overlay.add_toast(toast)


def set_to_stopped(app) -> None:
    """
    set status to stopped
    """
    page = ui.get("MainPage")
    page.set_icon_name("process-stop-symbolic")
    page.set_title(config._("Stopped"))
    page.set_description("")
    button = ui.get("SplitButton")
    text_start = config._("_Connect")
    style = button.get_style_context()
    style.remove_class("destructive-action")
    style.add_class("suggested-action")
    button.set_label(text_start)
    action_menu = button.get_popover()
    action_menu.set_sensitive(False)
    button = ui.get("CancelButton")
    button.set_visible(False)
    dconf = config.dconf
    dconf.reset("pid")
    if app:  # don't run on startup
        notify(config._("Tractor is stopped"))


def set_to_running(app) -> None:
    """
    set status to connected
    """
    page = ui.get("MainPage")
    page.set_icon_name("security-high-symbolic")
    page.set_title(config._("Running"))
    page.set_description("")
    button = ui.get("SplitButton")
    text_stop = config._("_Disconnect")
    style = button.get_style_context()
    style.remove_class("suggested-action")
    style.add_class("destructive-action")
    button.set_label(text_stop)
    action_menu = button.get_popover()
    action_menu.set_sensitive(True)
    button = ui.get("CancelButton")
    button.set_visible(False)
    if app:  # don't run on startup
        notify(config._("Tractor is running"))


def set_run_status(app=None) -> None:
    """
    set status of conection
    """
    if tasks.is_running():
        set_to_running(app)
    else:
        set_to_stopped(app)
    button = ui.get("SplitButton")
    button.set_sensitive(True)
    progress_bar = ui.get("ProgressBar")
    progress_bar.hide()


def set_pluginrow_sensivity(row=None) -> None:
    """
    set row sensitive if a plugable transport is set
    """
    if not row:
        row = ui.get("PluginRow")
    bridgetype = config.dconf.get_int("bridge-type")
    if bridgetype > 1:
        row.set_sensitive(True)
    else:
        row.set_sensitive(False)


def setup_pluginbutton(button=None) -> None:
    """
    set plugin button label and chooser
    """
    if not button:
        button = ui.get("PluginButton")
    dconf = config.dconf
    filename = Gio.File.new_for_path(dconf.get_string("plugable-transport"))
    if filename.query_exists():
        basename = filename.get_basename()
        button.set_label(basename)
    chooser = ui.get("PluginChooser")
    chooser.set_initial_file(filename)
    button.chooser = chooser
