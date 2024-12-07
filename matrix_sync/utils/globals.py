import threading


tLock = threading.Lock()
report_matrix = False
cleaned = False
sync_task = None