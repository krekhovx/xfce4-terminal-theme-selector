# xfce4-terminal-theme-selector

`xfce4-terminal-theme-selector` - simple curses-based theme selector for
`xfce4-terminal`. It allows you to easily switch themes from the command line,
providing a convenient way to change themes without keeping the preferences
dialog open. It solves issue
[#364](https://gitlab.xfce.org/apps/xfce4-terminal/-/issues/364)
(which upstream didn’t plan to implement). Would love feedback from XFCE users.

<div align="center">
<img src="https://github.com/krekhovx/xfce4-terminal-theme-selector/blob/master/assets/main.gif">
</div>

## Features

- Preview themes in real-time.
- Useful for users who prefer TUI tools.
- Switch themes directly from the command line.

## Installation

There are multiple options:

- Debian-based systems
  ([Package Tracker](https://tracker.debian.org/pkg/xfce4-terminal-theme-selector)):
```
sudo apt install xfce4-terminal-theme-selector
```

- You can install the package from this Git repository using `pip`:
```
python3 -m pip install git+https://github.com/krekhovx/xfce4-terminal-theme-selector
```
If you encounter an error due to an externally managed environment, create a
virtual environment using `python3 -m venv`

After installation, simply run the `xfce4-terminal-theme-selector` command.

- Alternatively, you can run `./bin/xfce4-terminal-theme-selector-local`
  from the cloned repository without installation.

## Contribution
PRs and issues are welcome! Have an idea for a new feature or improvement for
`xfce4-terminal-theme-selector`? Open an issue or fork the project and contribute.

## FAQ
You may find it useful to read
[FAQ](https://github.com/krekhovx/xfce4-terminal-theme-selector/blob/master/FAQ.md)
