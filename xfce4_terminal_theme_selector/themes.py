"""
Simple curses-based theme selector for xfce4-terminal.

SPDX-FileCopyrightText: Kirill Rekhov <krekhov.dev@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later

This module loads and parses xfce4-terminal themes from configuration files.
"""

import configparser
import os

def load_themes():
    theme_dir = os.path.expanduser('~/.local/share/xfce4/terminal/colorschemes')
    themes = []

    try:
        files = os.listdir(theme_dir)
    except (FileNotFoundError, PermissionError):
        return []

    for filename in os.listdir(theme_dir):
        if filename.endswith('.theme'):
            theme_path = os.path.join(theme_dir, filename)
            config = configparser.ConfigParser()
            try:
                config.read(theme_path)
                if 'Scheme' in config:
                    theme_name = config['Scheme'].get('Name', 'Unknown')
                    themes.append({
                        'name': theme_name,
                        'path': theme_path,
                        'config': config
                    })
            except configparser.ParsingError:
                continue

    return themes

def get_theme_properties(cfg):
    props = {}
    scheme = cfg['Scheme']

    mapping = {
        # Colors
        'colorbackground': '/color-background',
        'colorbackgroundvary': '/color-background-vary',
        'colorbold': '/color-bold',
        'colorboldisbright': '/color-bold-is-bright',
        'colorboldusedefault': '/color-bold-use-default',
        'colorcursor': '/color-cursor',
        'colorcursorforeground': '/color-cursor-foreground',
        'colorcursorusedefault': '/color-cursor-use-default',
        'colorforeground': '/color-foreground',
        'colorpalette': '/color-palette',
        'colorselection': '/color-selection',
        'colorselectionbackground': '/color-selection-background',
        'colorselectionusedefault': '/color-selection-use-default',
        'colorusetheme': '/color-use-theme',

        # Command / Dropdown
        'commandloginshell': '/command-login-shell',
        'dropdownheight': '/dropdown-height',
        'dropdownwidth': '/dropdown-width',

        # Font
        'fontname': '/font-name',

        # Misc
        'miscalwaysshowtabs': '/misc-always-show-tabs',
        'miscbell': '/misc-bell',
        'miscbellurgent': '/misc-bell-urgent',
        'miscbordersdefault': '/misc-borders-default',
        'miscconfirmclose': '/misc-confirm-close',
        'misccopyonselect': '/misc-copy-on-select',
        'misccursorblinks': '/misc-cursor-blinks',
        'misccursorshape': '/misc-cursor-shape',
        'misccycletabs': '/misc-cycle-tabs',
        'miscdefaultgeometry': '/misc-default-geometry',
        'mischighlighturls': '/misc-highlight-urls',
        'miscinheritgeometry': '/misc-inherit-geometry',
        'miscmenubardefault': '/misc-menubar-default',
        'miscmiddleclickopensuri': '/misc-middle-click-opens-uri',
        'miscmouseautohide': '/misc-mouse-autohide',
        'miscmousewheelzoom': '/misc-mouse-wheel-zoom',
        'miscnewtabadjacent': '/misc-new-tab-adjacent',
        'miscrewraponresize': '/misc-rewrap-on-resize',
        'miscrightclickaction': '/misc-right-click-action',
        'miscsearchdialogopacity': '/misc-search-dialog-opacity',
        'miscshowrelaunchdialog': '/misc-show-relaunch-dialog',
        'miscshowunsafepastedialog': '/misc-show-unsafe-paste-dialog',
        'miscslimtabs': '/misc-slim-tabs',
        'misctabclosebuttons': '/misc-tab-close-buttons',
        'misctabclosemiddleclick': '/misc-tab-close-middle-click',
        'misctabposition': '/misc-tab-position',
        'misctoolbardefault': '/misc-toolbar-default',

        # Scrolling
        'scrollingunlimited': '/scrolling-unlimited',

        # Shortcuts
        'shortcutsnomenukey': '/shortcuts-no-menukey',
        'shortcutsnomnemonics': '/shortcuts-no-mnemonics',

        # Tabs & Title
        'tabactivitycolor': '/tab-activity-color',
        'titlemode': '/title-mode'
    }

    for key, val in scheme.items():
        k = key.lower()

        if k in mapping:
            props[mapping[k]] = val

    return props
