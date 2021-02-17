# i3-swap-focus

i3 script to toggle between last windows

### Requirements

* [i3ipc](https://github.com/altdesktop/i3ipc-python)
* Some tool to send data over an unix socket (``ncat`` or ``openbsd-netcat`` recommended)

### Install

```
pip install i3_swap_focus
```

### i3 config example

```
exec --no-startup-id i3_swap_focus
# Using ncat
bindsym $mod+Tab exec echo "swap_focus" | ncat --send-only -U "$XDG_RUNTIME_DIR/i3/swap_focus.sock"
# Using openbsd nc
bindsym $mod+Tab exec echo "swap_focus" | nc -w0 -U "$XDG_RUNTIME_DIR/i3/event-listener.sock"
```

### Arch Users

It looks like last ncat version has segfaults issues when using Unix sockets (https://github.com/nmap/nmap/issues/2154 still unpatched in arch). Try using `openbsd-netcat` instead. Alternatively, you can use this [ncat static build](https://github.com/ernw/static-toolbox/actions?query=workflow%3ANmap) from ERNW.
