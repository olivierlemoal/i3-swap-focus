#! /usr/bin/env python3

import os
import asyncio
import argparse
import signal
import atexit
from i3ipc.aio import Connection

pid_file = '{XDG_RUNTIME_DIR}/swap_focus.pid'.format_map(os.environ)
window_stack = []

config = {}

async def on_signal(i3):
    if window_stack:
        window_id = window_stack.pop()
        if config["stay_in_workspace"]:
            current_workspace = (await i3.get_tree()).find_focused().workspace().id
            container = (await i3.get_tree()).find_by_id(window_id)
            if not container:
                window_stack.append(window_id)
                return
            window_workspace = container.workspace().id
            if current_workspace != window_workspace:
                window_stack.append(window_id)
                return
        cmd = f'[con_id={window_id}] focus'
        await i3.command(cmd)


def exit_handler():
    os.remove(pid_file)


def on_window(conn, event):
    if "ignore_focus" in event.container.marks:
        return
    if event.change == 'focus':
        if not window_stack or event.container.id != window_stack[0]:
            window_stack.insert(0, event.container.id)
            if len(window_stack) > 2:
                del window_stack[2:]


async def run():
    with open(pid_file, 'w') as file:
        file.write(str(os.getpid()))
    atexit.register(exit_handler)

    i3 = await Connection(auto_reconnect=True).connect()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGUSR1, lambda: asyncio.create_task(on_signal(i3)))
    i3.on('window::focus', on_window)
    await i3.main()

def main():
    parser = argparse.ArgumentParser(description='i3 script to toggle between last windows.')
    parser.add_argument('--stay-in-workspace', action=argparse.BooleanOptionalAction, default=False, help="Do not switch focus if window is on a different workspace")
    config["stay_in_workspace"] = parser.parse_args().stay_in_workspace
    asyncio.run(run())

main()
