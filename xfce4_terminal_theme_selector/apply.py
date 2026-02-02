"""
Simple curses-based theme selector for xfce4-terminal.

SPDX-FileCopyrightText: Kirill Rekhov <krekhov.dev@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later

This module provides functions to manage, save, and apply themes
for xfce4-terminal using Xfconf.
"""

import gi # GObject Introspection
gi.require_version("Xfconf", "0")

# For access and change Xfce settings via Xfconf
from gi.repository import Xfconf

CHANNEL = "xfce4-terminal"

DEFAULTS = {
    "color-background": "#000000",
    "color-background-vary": False,
    "color-bold": "",
    "color-bold-is-bright": True,
    "color-bold-use-default": True,
    "color-cursor": "",
    "color-cursor-foreground": "",
    "color-cursor-use-default": True,
    "color-foreground": "#ffffff",
    "color-palette": (
        "#000000;#aa0000;#00aa00;#aa5500;#0000aa;#aa00aa;#00aaaa;#aaaaaa;"
        "#555555;#ff5555;#55ff55;#ffff55;#5555ff;#ff55ff;#55ffff;#ffffff"
    ),
    "color-selection": "",
    "color-selection-background": "",
    "color-selection-use-default": True,
    "color-use-theme": False,
    "tab-activity-color": "#aa0000"
}

_saved_state = None

Xfconf.init() # Initialize Xfconf globally (only once required)
_channel = Xfconf.Channel.get(CHANNEL)

def normalize_value(name, value):
    if isinstance(value, gi.repository.Xfconf.Channel):
        return DEFAULTS[name]

    if name == "color-palette":
        if isinstance(value, str):
            return tuple(value.split(";"))
        if isinstance(value, (list, tuple)):
            return tuple(value)
        return tuple(DEFAULTS["color-palette"].split(";"))

    if isinstance(value, str):
        v = value.strip().lower()
        if v == "true":
            return True
        if v == "false":
            return False

    return value

def xfconf_safe_get(name):
    key = "/" + name

    try:
        if name == "color-palette":
            s = _channel.get_string(key)
            if not s:
                return DEFAULTS["color-palette"].split(";")
            return s.split(";")

        if (name.endswith("-use-default")
            or name.endswith("-vary")
            or name.endswith("-is-bright")
            or name == "color-use-theme"):
            return _channel.get_bool(key)

        return _channel.get_string(key)
    except Exception:
        return None

def xfconf_set(name, value):
    key = "/" + name
    value = normalize_value(name, value)

    if name == "color-palette":
        if isinstance(value, (list, tuple)):
            value = ";".join(value)
        _channel.set_string(key, value)
        return

    if isinstance(value, bool):
        _channel.set_bool(key, value)
        return

    if isinstance(value, int):
        _channel.set_int(key, value)
        return

    _channel.set_string(key, str(value))

def read_current_state():
    state = {}
    for key, default_value in DEFAULTS.items():
        val = xfconf_safe_get(key)
        if val is None:
            val = default_value
        state[key] = val
    return state

def restore_state():
    global _saved_state
    if not _saved_state:
        return
    for key, val in _saved_state.items():
        xfconf_set(key, val)

def apply_preview(theme_props):
    clean = {k.lstrip("/"): v for k, v in theme_props.items()}
    for name, default_value in DEFAULTS.items():
        xfconf_set(name, clean.get(name, default_value))

def apply_theme(theme_props):
    global _saved_state
    _saved_state = read_current_state() # Save current state
    clean = {k.lstrip("/"): v for k, v in theme_props.items()}
    for name, default_value in DEFAULTS.items():
        xfconf_set(name, clean.get(name, default_value))
