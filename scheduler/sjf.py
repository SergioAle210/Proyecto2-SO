class Proceso:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.start_time = None
        self.end_time = None
        self.finished = False


def sjf(procesos):
    procesos = sorted(procesos, key=lambda p: p.at)  # Ordenamos por llegada
    tiempo = 0
    completados = 0
    n = len(procesos)
    resultado = []

    while completados < n:
        disponibles = [p for p in procesos if p.at <= tiempo and not p.finished]
        if disponibles:
            actual = min(disponibles, key=lambda p: p.bt)  # Proceso con menor BT
            actual.start_time = tiempo
            tiempo += actual.bt
            actual.end_time = tiempo
            actual.finished = True
            resultado.append(actual)
            completados += 1
        else:
            tiempo += 1  # Si no hay disponibles, avanzamos un ciclo

    return resultado
