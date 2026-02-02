"""
Simple curses-based theme selector for xfce4-terminal.

SPDX-FileCopyrightText: Kirill Rekhov <krekhov.dev@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later

This module provides a simple interface for selecting and
applying themes for xfce4-terminal.
"""

from .apply import apply_theme, read_current_state, restore_state
from .themes import load_themes, get_theme_properties
from .ui import run_ui, show_no_themes

def main():
    themes = load_themes()
    if not themes:
        show_no_themes()
        return

    themes = sorted(themes, key=lambda t: t["name"])
    saved = read_current_state()
    idx = run_ui(themes, saved)

    if idx < 0:
        restore_state()
        return

    theme = themes[idx]
    props = get_theme_properties(theme['config'])
    apply_theme(props)

if __name__ == '__main__':
    main()
