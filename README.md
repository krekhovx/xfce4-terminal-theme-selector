# xfce4-terminal-theme-selector

`xfce4-terminal-theme-selector` - simple curses-based theme selector for
xfce4-terminal. It allows you to easily switch themes from the command line,
providing a convenient way to change themes without keeping the preferences
dialog open.

## Features

- Preview themes in real-time.
- Useful for users who prefer TUI tools.
- Switch themes directly from the command line.

## Installation

There are multiple options:

- Debian‑based systems:
  Make sure these packages are installed:
  `xfce4-terminal` `python3-gi` `python3-gi-cairo` `gir1.2-xfconf-0`

- You can install the package from this Git repository using `pip`:
```
python3 -m pip install git+https://github.com/krekhovx/xfce4-terminal-theme-selector
```
If you encounter an error due to an externally managed environment, create a
virtual environment using `python3 -m venv`

After installation, simply run the `xfce4-terminal-theme-selector` command.

- Alternatively, you can run `./bin/xfce4-terminal-theme-selector-local`
  from the cloned repository without installation.

## FAQ
You may find it useful to read
[FAQ](https://github.com/krekhovx/xfce4-terminal-theme-selector/blob/master/FAQ.md)
