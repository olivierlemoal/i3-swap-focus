#!/usr/bin/env python3

# Use following config in i3 :
# exec --no-startup-id "python /usr/local/bin/i3_swap_focus.py"
# bindsym $mod+Tab exec echo "swap_focus" | ncat --send-only -U "$XDG_RUNTIME_DIR/i3/swap_focus.sock"

import os
import asyncio
from i3ipc.aio import Connection

socket = '{XDG_RUNTIME_DIR}/i3/swap_focus.sock'.format_map(os.environ)
window_stack = []


async def on_unix_connect(i3, reader, writer):
    while True:
        cmd = await reader.readline()
        cmd = cmd.strip()
        if not cmd:
            break

        if cmd == b'swap_focus' and window_stack:
            cmd = '[con_id=%s] focus' % window_stack.pop()
            await i3.command(cmd)


def on_window(conn, event):
    if event.container.window_instance == "scratchpad":
        return
    if event.change == 'focus':
        if not window_stack or event.container.id != window_stack[0]:
            window_stack.insert(0, event.container.id)
            if len(window_stack) > 2:
                del window_stack[2:]


async def main():
    if os.path.exists(socket):
        os.unlink(socket)

    i3 = await Connection(auto_reconnect=True).connect()
    server = await asyncio.start_unix_server(lambda r, w: on_unix_connect(i3, r, w), socket)

    await i3.get_workspaces()

    i3.on('window::focus', on_window)
    await i3.main()
    await server.wait_closed()

asyncio.run(main())
