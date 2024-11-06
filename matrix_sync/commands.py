import asyncio
import json
import matrix_sync.config

from mcdreforged.api.all import *
from matrix_sync.globals import *
from matrix_sync.token import get_tip_read
from matrix_sync.sync.receiver import getMsg

psi = ServerInterface.psi()

# Help tips.
def help() -> RTextList:
    return RTextList(
        psi.rtr("matrix_sync.help_tips.title") + "\n",
        psi.rtr("matrix_sync.help_tips.start_command") + "\n",
        psi.rtr("matrix_sync.help_tips.stop_command") + "\n",
        psi.rtr("matrix_sync.help_tips.closetip_command") + "\n"
    )

# Manually run sync processes.
def manualSync():
    if not tLock.locked():
        start_room_msg()
        psi.say(psi.rtr("matrix_sync.manual_sync.start_tip"))
        read = asyncio.run(get_tip_read())
        if not read:
            return RTextList(
                psi.rtr("matrix_sync.manual_sync.start_sync") + "\n",
                psi.rtr("matrix_sync.old_msg_sync") + "\n",
                psi.rtr("matrix_sync.old_msg_sync2") + "\n",
                psi.rtr("matrix_sync.old_msg_sync3") + "\n",
                psi.rtr("matrix_sync.old_msg_sync4") + "\n",
                psi.rtr("matrix_sync.old_msg_sync5") + "\n"
            )
        else:
            return psi.rtr("matrix_sync.manual_sync.start_sync")
    else:
        return psi.rtr("matrix_sync.manual_sync.start_error")

# Manually stop sync processes.
def stopSync(src):
    global sync_task
    if src.is_console:
        try:
            if sync_task is not None:
                sync_task.cancel()
                return psi.rtr("matrix_sync.manual_sync.stop_sync")
            else:
                return psi.rtr("matrix_sync.manual_sync.not_running")
        except Exception:
            return psi.rtr("matrix_sync.manual_sync.stop_error")
    else:
        return psi.rtr("matrix_sync.manual_sync.stop_denied")
    
def closeTip():
    TOKEN_FILE = matrix_sync.config.TOKEN_FILE
    with open(TOKEN_FILE, "r") as f:
        existing_data = json.load(f)
    existing_data["tip_read"] = True
    with open(TOKEN_FILE, "w") as f:
        json.dump(existing_data, f)
    return psi.rtr("matrix_sync.on_tip_read")

# Sub thread to receive room messages from matrix without block main MCDR thread.
@new_thread('MatrixReceiver')
def start_room_msg():
    with tLock:
        asyncio.run(on_room_msg())

async def on_room_msg():
    global sync_task
    if sync_task is not None and not sync_task.done():
        sync_task.cancel()
        await sync_task
    sync_task = asyncio.create_task(getMsg())
    await sync_task