#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2023.

"""
handlers for ui events
"""

from gi.repository import Gio, GLib, Gtk, GObject

from . import actions
from . import config
from . import tasks


class Country(GObject.Object):
    """
    prepare factory for countries
    """

    __gtype_name__ = "Country"

    def __init__(self, country_id: str, country_name: str):
        super().__init__()
        self._country_id = country_id
        self._country_name = country_name

    @GObject.Property
    def country_id(self) -> str:
        """
        return ids
        """
        return self._country_id

    @GObject.Property
    def country_name(self) -> str:
        """
        return names
        """
        return self._country_name


class BridgeType(GObject.Object):
    """
    Prepare factory for bridge types
    """

    __gtype_name__ = "BridgeType"

    def __init__(self, type_id: int, type_name: str):
        super().__init__()
        self._bridgetype_id = type_id
        self._bridgetype_name = type_name

    @GObject.Property
    def type_id(self) -> int:
        """
        return ids
        """
        return self._bridgetype_id

    @GObject.Property
    def type_name(self) -> str:
        """
        return names
        """
        return self._bridgetype_name


def on_mainpage_realize(window):
    """
    First setups
    """
    if window:
        actions.set_run_status()


def on_factory_setup(factory, list_item):
    """
    set labels for dropdown
    """
    del factory
    label = Gtk.Label()
    list_item.set_child(label)


def on_factory_bind(factory, list_item):
    """
    set country names as labels
    """
    del factory
    label = list_item.get_child()
    country = list_item.get_item()
    label.set_text(country.country_name)


def on_exitcountry_change(combo, _):
    """
    set exit country in dconf
    """
    country = combo.get_selected_item()
    node = country.country_id
    config.dconf.set_string("exit-node", node)


def on_exitcountry_realize(combo):
    """
    sets up exit node comborow
    """
    _ = config._
    nodes = {
        "au": _("Austria"),
        "bg": _("Bulgaria"),
        "ca": _("Canada"),
        "ch": _("Switzerland"),
        "cz": _("Czech"),
        "de": _("Germany"),
        "es": _("Spain"),
        "fi": _("Finland"),
        "fr": _("France"),
        "ie": _("Ireland"),
        "md": _("Moldova"),
        "nl": _("Netherlands"),
        "no": _("Norway"),
        "pl": _("Poland"),
        "ro": _("Romania"),
        "sc": _("Seychelles"),
        "se": _("Sweden"),
        "sg": _("Singapore"),
        "su": _("Russia"),
        "ua": _("Ukraine"),
        "uk": _("United Kingdom"),
        "us": _("United States"),
    }

    country_ids = list(nodes.keys())
    country_names = list(nodes.values())

    node = config.dconf.get_string("exit-node")
    if node == "ww":
        index = 0
    else:
        country_name = nodes[node]
        index = sorted(country_names).index(country_name) + 1

    # Define and populate the model
    model = Gio.ListStore(item_type=Country)
    model.append(Country(country_id="ww", country_name=_("Auto (Best)")))
    for country_name in sorted(country_names):
        country_id = country_ids[country_names.index(country_name)]
        model.append(Country(country_id=country_id, country_name=country_name))

    combo.set_model(model)

    combo.set_selected(index)


def on_actionacceptconnection_realize(switch):
    """
    bind accept-connection
    """
    config.dconf.bind(
        "accept-connection",
        switch,
        "active",
        Gio.SettingsBindFlags.DEFAULT,
    )


def on_actionsocksport_realize(spin):
    """
    bind socks-port
    """
    port = config.dconf.get_int("socks-port")
    spin.set_text(str(port))
    config.dconf.bind(
        "socks-port", spin, "value", Gio.SettingsBindFlags.DEFAULT
    )


def on_actiondnsport_realize(spin):
    """
    bind socks-port
    """
    port = config.dconf.get_int("dns-port")
    spin.set_text(str(port))
    config.dconf.bind("dns-port", spin, "value", Gio.SettingsBindFlags.DEFAULT)


def on_actionhttpport_realize(spin):
    """
    bind http-port
    """
    port = config.dconf.get_int("http-port")
    spin.set_text(str(port))
    config.dconf.bind(
        "http-port", spin, "value", Gio.SettingsBindFlags.DEFAULT
    )


def on_bt_factory_setup(factory, list_item):
    """
    set labels for dropdown
    """
    del factory
    label = Gtk.Label()
    list_item.set_child(label)


def on_bt_factory_bind(factory, list_item):
    """
    set bridgetype names as labels
    """
    del factory
    label = list_item.get_child()
    bridge_type = list_item.get_item()
    label.set_text(bridge_type.type_name)


def on_bridgetype_change(combo, _):
    """
    set bridge type in dconf
    """
    bridgetype = combo.get_selected_item()
    type_id = bridgetype.type_id
    config.dconf.set_int("bridge-type", type_id)
    actions.set_pluginrow_sensivity()


def on_bridgetypecombo_realize(combo):
    """
    create and set model for bridge type
    """
    bridgetype = config.dconf.get_int("bridge-type")
    _ = config._
    # Define and populate the model
    model = Gio.ListStore(item_type=BridgeType)
    model.append(BridgeType(type_id=0, type_name=_("None")))
    model.append(BridgeType(type_id=1, type_name=_("Vanilla")))
    model.append(BridgeType(type_id=2, type_name=_("Obfuscated")))
    combo.set_model(model)
    combo.set_selected(bridgetype)


def on_pluginrow_realize(row):
    """
    set row sensitive if a plugable transport is set
    """
    actions.set_pluginrow_sensivity(row)


def on_bridgetextview_realize(view):
    """
    show bridges list
    """
    buff = view.get_buffer()
    bridges_file = tasks.get_bridges_file()
    with open(bridges_file, encoding="utf-8") as file:
        text = file.read()
        buff.set_text(str(text))


def on_savebutton_clicked(*_, **__):  # TODO: Move this to actions
    """
    save bridges
    """
    actions.on_save()


def on_dialog_realize(dialog):
    """
    Add OK button to dialog
    """
    dialog.add_response("ok", config._("_OK"))
    #  These two lines are here becuase Cambalache has no support of
    #  translation for AdwMessageDialog yet. To be removed afterward
    dialog.set_heading(config._("Can not save the bridges"))
    dialog.set_body(config._("Please check the syntax of bridges"))


def on_pluginbutton_realize(button):
    """
    setup plugin button
    """
    actions.setup_pluginbutton(button)


def on_pluginbutton_clicked(button):
    """
    open file chooser
    """
    button.chooser.open(callback=on_pluginchooser_response)


def on_pluginchooser_response(chooser, task):
    """
    get plugin file and update plugin button
    """
    try:
        file = chooser.open_finish(task)
    except GLib.GError:
        # gtk-dialog-error-quark: Dismissed by user
        pass
    else:
        config.dconf.set_string("plugable-transport", file.get_path())
        actions.setup_pluginbutton()


def on_about_realize(window):
    """
    insert translators
    """
    window.set_translator_credits(config._("translator-credits"))
