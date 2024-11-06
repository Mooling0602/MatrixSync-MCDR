import threading
import matrix_sync.config

from mcdreforged.api.all import *

psi = ServerInterface.psi()
tLock = threading.Lock()
lock_is_None = matrix_sync.config.lock_is_None
cleaned = False
sync_task = None