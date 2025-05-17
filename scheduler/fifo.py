class Proceso:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.start_time = None
        self.end_time = None


def fifo(procesos):
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0
    for p in procesos:
        if tiempo < p.at:
            tiempo = p.at
        p.start_time = tiempo
        tiempo += p.bt
        p.end_time = tiempo
    return procesos
