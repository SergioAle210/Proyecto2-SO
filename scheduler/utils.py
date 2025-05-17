from scheduler.fifo import Proceso


def leer_procesos(path):
    procesos = []
    with open(path, "r") as f:
        for linea in f:
            if linea.strip():
                pid, bt, at, pr = linea.strip().split(",")
                procesos.append(
                    Proceso(pid.strip(), bt.strip(), at.strip(), pr.strip())
                )
    return procesos


def calcular_metricas(procesos):
    total_wt = 0
    total_tat = 0
    n = len(procesos)

    for p in procesos:
        wt = p.start_time - p.at
        tat = p.end_time - p.at
        total_wt += wt
        total_tat += tat

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    return avg_wt, avg_tat
