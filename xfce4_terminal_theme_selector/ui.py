"""
Simple curses-based theme selector for xfce4-terminal.

SPDX-FileCopyrightText: Kirill Rekhov <krekhov.dev@gmail.com>
SPDX-License-Identifier: GPL-3.0-or-later

This module provides a curses-based user interface for selecting
and previewing xfce4-terminal themes.
"""

import curses
from . import apply
from .apply import apply_preview, restore_state
from .themes import get_theme_properties

def show_no_themes():
    def ui(stdscr):
        stdscr.clear()
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()

        msg1 = "No color schemes found."
        msg2 = "Check your ~/.local/share/xfce4/terminal/colorschemes"

        text_w = max(len(msg1), len(msg2))
        box_w = text_w + 6
        box_h = 6

        x = (w - box_w) // 2
        y = (h - box_h) // 2

        stdscr.addch(y, x, curses.ACS_ULCORNER)
        stdscr.addch(y, x + box_w - 1, curses.ACS_URCORNER)
        stdscr.addch(y + box_h - 1, x, curses.ACS_LLCORNER)
        stdscr.addch(y + box_h - 1, x + box_w - 1, curses.ACS_LRCORNER)

        stdscr.addstr(y + 2, x + (box_w - len(msg1)) // 2, msg1)
        stdscr.addstr(y + 3, x + (box_w - len(msg2)) // 2, msg2)

        stdscr.hline(y, x + 1, curses.ACS_HLINE, box_w - 2)
        stdscr.hline(y + box_h - 1, x + 1, curses.ACS_HLINE, box_w - 2)
        stdscr.vline(y + 1, x, curses.ACS_VLINE, box_h - 2)
        stdscr.vline(y + 1, x + box_w - 1, curses.ACS_VLINE, box_h - 2)

        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(ui)

def run_ui(themes, saved_state, active_theme_name="unknown"):
    search_mode = False
    search_text = ""
    apply._saved_state = saved_state

    header_path = "All color schemes: ~/.local/share/xfce4/terminal/colorschemes/*.theme"
    header_qty = f"Quantity: {len(themes)}"

    selected_row = -1 # -1 = Active theme
    visible_offset = 0 # Scroll start index

    def display_menu(stdscr):
        nonlocal selected_row, visible_offset
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Header
        stdscr.addstr(1, 3, header_path[: w - 4])
        stdscr.addstr(2, 3, header_qty[: w - 4])
        stdscr.hline(3, 0, curses.ACS_HLINE, w)

        # Active theme
        if selected_row == -1:
            stdscr.addstr(4, 1, ("> Active theme (" + active_theme_name + ")")[: w - 4])
        else:
            stdscr.addstr(4, 1, ("  Active theme (" + active_theme_name + ")")[: w - 4])

        base_y = 5
        max_visible = h - base_y - 2
        if max_visible < 1:
            max_visible = 1

        # Clamp visible_offset to the valid scroll range
        if visible_offset > len(themes) - max_visible:
            visible_offset = max(0, len(themes) - max_visible)

        slice_start = visible_offset
        slice_end = slice_start + max_visible
        if slice_end > len(themes):
            slice_end = len(themes)

        visible_themes = themes[slice_start : slice_end]

        # Themes
        for idx, t in enumerate(visible_themes):
            y = base_y + idx
            if y >= h:
                break

            real_idx = slice_start + idx
            prefix = "> " if selected_row == real_idx else "  "
            s = (prefix + t["name"])[: w - 4]

            if selected_row == real_idx:
                stdscr.attron(curses.A_REVERSE)

            stdscr.addstr(y, 1, s)

            if selected_row == real_idx:
                stdscr.attroff(curses.A_REVERSE)

        # Footer
        footer_text = "Search (/)  Down/Up (↓/j, ↑/k)  Accept (Enter)  Quit (q)"

        footer_y = h - 2
        stdscr.hline(footer_y, 0, curses.ACS_HLINE, w)

        if not search_mode:
            stdscr.addstr(footer_y + 1, 3, footer_text[: w - 2])
        else:
            stdscr.addstr(footer_y + 1, 3, "/" + search_text)

        stdscr.refresh()

    def main(stdscr):
        nonlocal selected_row, visible_offset, search_mode, search_text

        curses.set_escdelay(1)
        curses.curs_set(0)
        restore_state()

        while True:
            display_menu(stdscr)
            key = stdscr.getch()

            h, _ = stdscr.getmaxyx()
            base_y = 5
            max_visible = h - base_y - 2
            if max_visible < 1:
                max_visible = 1

            if search_mode:
                if key == 27:
                    search_mode = False
                    search_text = ""
                    continue
                if key in (10, 13):
                    search_mode = False
                    if not search_text:
                        continue
                    for i, t in enumerate(themes):
                        if search_text.lower() in t["name"].lower():
                            selected_row = i
                            props = get_theme_properties(themes[i]["config"])
                            apply_preview(props)
                            visible_offset = max(0, i - 1)
                            break
                    continue

                if key in (curses.KEY_BACKSPACE, 127, 8):
                    search_text = search_text[: - 1]
                    if not search_text:
                        search_mode = False
                    continue

                if 32 <= key <= 126:
                    search_text += chr(key)
                    continue

            if key == ord("/"):
                search_mode = True
                search_text = ""
                continue

            if key in (curses.KEY_UP, ord("k")):
                if selected_row > -1:
                    selected_row -= 1

                    if selected_row == -1:
                        restore_state()
                    else:
                        props = get_theme_properties(themes[selected_row]["config"])
                        apply_preview(props)

                if selected_row < visible_offset:
                    visible_offset = selected_row
            elif key in (curses.KEY_DOWN, ord("j")):
                if selected_row < len(themes) - 1:
                    selected_row += 1
                    props = get_theme_properties(themes[selected_row]["config"])
                    apply_preview(props)

                if selected_row >= visible_offset + max_visible:
                    visible_offset = selected_row - max_visible + 1

            if selected_row == -1:
                visible_offset = 0

            if visible_offset < 0:
                visible_offset = 0

            max_offset = max(0, len(themes) - max_visible)
            if visible_offset > max_offset:
                visible_offset = max_offset

            if key in (10, 13, curses.KEY_ENTER):
                return selected_row

            if key == ord("q"):
                restore_state()
                return -1

        return -1

    return curses.wrapper(main)
