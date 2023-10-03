#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2019-2022.

"""
Main module for carburetor
"""

from sys import argv

import gi

gi.require_versions({"Adw": "1"})
from gi.repository import Adw

from . import actions
from . import ui


class Application(Adw.Application):
    """
    main window of carburetor
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args, application_id="io.frama.tractor.carburetor", **kwargs
        )
        self.window = None
        self.prefs = None
        self.about = None

    def do_startup(self, *args, **kwargs) -> None:
        Adw.Application.do_startup(self)
        actions.do_startup(self)

    def do_activate(self, *args, **kwargs) -> None:
        if not self.window:
            ui.css()
            window = ui.get("MainWindow")
            self.add_window(window)
            self.window = window
        self.window.present()


def main() -> None:
    """
    main entrance of app
    """
    ui.initialize_builder()
    app = Application()
    app.run(argv)


if __name__ == "__main__":
    main()
