class Proceso:
    def __init__(self, pid, bt, at, priority):
        self.pid = pid
        self.bt = int(bt)
        self.at = int(at)
        self.priority = int(priority)
        self.remaining = int(bt)
        self.start_time = None
        self.end_time = None
        self.first_run = True


def round_robin(procesos, quantum):
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0
    queue = []
    completados = 0
    resultado = []
    n = len(procesos)
    index = 0

    while completados < n:
        # Agregar procesos que ya llegaron
        while index < n and procesos[index].at <= tiempo:
            queue.append(procesos[index])
            index += 1

        if not queue:
            tiempo += 1
            continue

        actual = queue.pop(0)

        if actual.first_run:
            actual.start_time = tiempo
            actual.first_run = False

        ejecutar = min(quantum, actual.remaining)
        tiempo += ejecutar
        actual.remaining -= ejecutar

        # Agregar nuevos procesos que hayan llegado durante la ejecución
        while index < n and procesos[index].at <= tiempo:
            queue.append(procesos[index])
            index += 1

        if actual.remaining > 0:
            queue.append(actual)
        else:
            actual.end_time = tiempo
            resultado.append(actual)
            completados += 1

    return resultado
