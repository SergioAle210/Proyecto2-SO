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
