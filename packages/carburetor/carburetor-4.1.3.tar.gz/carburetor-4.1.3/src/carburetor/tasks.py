#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2022.

"""
tasks to be done async
"""

import re

from subprocess import PIPE, Popen

from gi.repository import GLib

from . import config
from . import actions


def connect(action: str, app) -> None:
    """
    connect or disconnect
    """
    task = Popen(
        [config.COMMAND, action],
        stdout=PIPE,
        start_new_session=True,
    )
    if action == "start":
        config.dconf.set_int("pid", task.pid)
    app.io_in = GLib.io_add_watch(task.stdout, GLib.IO_IN, set_progress)
    GLib.io_add_watch(task.stdout, GLib.IO_HUP, thread_finished, app)


def set_progress(stdout, *_) -> bool:
    """
    set progress output on page desription
    """
    try:
        line = stdout.readline().decode("utf-8")
        valid = re.compile(r".*\[notice\] ")
        if "notice" in line:
            percentage = line.split(" ")[5]
            notice = valid.sub("", line)[:-9]
            actions.set_description(notice)
            actions.set_progress(int(percentage[:-1]))
    except ValueError:
        return False
    return True


def thread_finished(stdout, condition, app) -> bool:
    """
    things to do after process finished
    """
    if condition:
        GLib.source_remove(app.io_in)
        stdout.close()
        actions.set_run_status(app)
        return False
    return True


def new_id() -> None:
    """
    get new identity
    """
    with Popen([config.COMMAND, "newid"], stdout=PIPE) as task:
        task.wait()


def set_proxy(action: str) -> None:
    """
    set or unset proxy
    """
    with Popen([config.COMMAND, action], stdout=PIPE) as task:
        task.wait()


def get_bridges_file() -> str:
    """
    get bridges file
    """
    with Popen([config.COMMAND, "bridgesfile"], stdout=PIPE) as task:
        bridges = task.stdout.read()
        bridges_file = bridges.decode("utf-8").strip("\n")
        return bridges_file


def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    if val in ("n", "no", "f", "false", "off", "0"):
        return 0
    raise ValueError(f"invalid truth value {(val,)}")


def is_proxy_set() -> bool:
    """
    checks if proxy was already set
    """
    with Popen([config.COMMAND, "isset"], stdout=PIPE) as check:
        output = strtobool(check.stdout.read().decode("utf-8").strip("\n"))
        return output


def is_running() -> bool:
    """
    check if tractor is running or not
    """
    with Popen([config.COMMAND, "isrunning"], stdout=PIPE) as check:
        output = strtobool(check.stdout.read().decode("utf-8").strip("\n"))
        return output


def is_connected() -> bool:
    """
    check if tractor is connected or not
    """
    check = Popen([config.COMMAND, "isconnected"], stdout=PIPE)
    GLib.io_add_watch(check.stdout, GLib.IO_IN, return_connection_status)


def return_connection_status(stdout, *_) -> bool:
    """
    return connection status
    """
    result = stdout.readline().decode("utf-8")
    if "True" in result:
        toast = config._("Tractor is connected")
    else:
        toast = config._("Tractor couldn't connect")
    actions.notify(toast)
    return True
