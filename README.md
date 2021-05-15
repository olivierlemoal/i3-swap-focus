# i3-swap-focus

i3/sway script to toggle between last windows. For older Python version (<3.7), use this [branch](https://github.com/olivierlemoal/i3-swap-focus/tree/python-3.6-support).

### Requirements

* [i3ipc](https://github.com/altdesktop/i3ipc-python)

## Install

```
pip install --upgrade i3-swap-focus
```

### i3/sway config example

```
exec i3-swap-focus
bindsym $mod+Tab exec pkill -USR1 -F "${XDG_RUNTIME_DIR}/swap_focus.pid"
```

## Features

### Ignore windows

To ignore some windows (e.g windows that belong to scratchpad), just mark them with ``ignore_focus`` in your config :

```
# Put a term in scratchpad
exec alacritty --class scratchpad_term

# i3 :
for_window [instance="scratchpad_term"] mark "ignore_focus", move scratchpad

# sway :
for_window [app_id="scratchpad_term"] mark "ignore_focus", move scratchpad
```

### Stay in workspace

This script accepts a ``--stay-in-workspace`` flag if you do not wish to focus on a different workspace :
```
exec i3-swap-focus --stay-in-workspace
```
