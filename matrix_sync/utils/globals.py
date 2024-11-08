import threading

from . import config
from mcdreforged.api.all import *

psi = ServerInterface.psi()
tLock = threading.Lock()
lock_is_None = config.lock_is_None
cleaned = False
sync_task = None