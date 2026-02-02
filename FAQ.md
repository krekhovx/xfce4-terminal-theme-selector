# Frequently Asked Questions
- [Why did I write this project?](#why-did-i-write-this-project)
- [Why is this convenient?](#why-is-this-convenient)
- [Which commands are useful when working with this project?](#which-commands-are-useful-when-working-with-this-project)
- [Where did I get the logic for working with themes?](#where-did-i-get-the-logic-for-working-with-themes)
- [Where can you get themes for xfce4-terminal?](#where-can-you-get-themes-for-xfce4-terminal)
- [How can you help?](#how-can-you-help)

<a name="why-did-i-write-this-project"></a>
## Why did I write this project?
I love xfce4-terminal and use it a lot. A long time ago, I saw a YouTube video
where an engineer compared different terminals. That’s where I noticed Kitty and
its ability to switch themes directly from the command line. This inspired me,
and I created this [issue](https://gitlab.xfce.org/apps/xfce4-terminal/-/issues/364).

The developers explained that they were unlikely to add such a feature directly
into xfce4-terminal, but they pointed out that it could be implemented as an
external tool using Xfconf, which supports changing properties at runtime. So I
decided to create my own project and implement this idea as a standalone
application.

<a name="why-is-this-convenient"></a>
## Why is this convenient?
Yes, I know about GUI (Terminal Preferences -> Colors -> Presets), but the
dialog stays open while selecting themes, which makes it harder to fully see the
terminal and preview changes. A TUI tool is more convenient for me, because I
can switch themes directly from the command line and immediately see the result.

I also like using tmux: on one pane I run xfce4-terminal-theme-selector, and on
another I open files like ~/.bashrc to adjust or test things while switching
themes.

<a name="which-commands-are-useful-when-working-with-this-project"></a>
## Which commands are useful when working with this project?
Lists all available xfce4-terminal properties:
```
$ xfconf-query -c xfce4-terminal -l
```

Lists the same properties, but with their current values:
```
$ xfconf-query -c xfce4-terminal -l -v
```

<a name="where-did-i-get-the-logic-for-working-with-themes"></a>
## Where did I get the logic for working with themes?
I took the xfce4-terminal source code and started reading through it. Along the
way, I found several files that turned out to be useful - they are responsible
for storing and processing the terminal’s properties:
```
terminal/terminal-preferences.c
terminal/terminal-preferences-dialog.c
```

Functions:
```
terminal_preferences_load_rc_file
terminal_preferences_dialog_presets_load
terminal_preferences_dialog_presets_changed
```

`terminal_preferences_load_rc_file` - loads the old xfce4-terminal configuration
file, reads all properties, transfers them into the properties object, and
migrates the old color palette format if necessary.

`terminal_preferences_dialog_presets_load` - finds all color scheme files
(in system and user directories), reads their names, and populates the dropdown
list in the preferences dialog.

`terminal_preferences_dialog_presets_changed` - when the user selects a preset,
it reads the scheme file and applies its values (colors) to the properties
object.

<a name="where-can-you-get-themes-for-xfce4-terminal"></a>
## Where can you get themes for xfce4-terminal?
You can create your own themes or look for existing ones on GitHub or elsewhere.
Personally, I collect my favorite themes
[here](https://github.com/krekhovx/dotfiles-debian/tree/master/.local/share/xfce4/terminal/colorschemes).

Many themes for GNOME Terminal, Konsole, or Alacritty can be adapted for
xfce4-terminal if you convert their format (usually it’s enough to map the
palette and basic colors to the structure used by xfce4-terminal).

<a name="how-can-you-help"></a>
## How can you help?
Just use it and report any problems, and feel free to suggest new ideas.
