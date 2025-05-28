def srt(procesos):
    """
    Shortest Remaining Time (preemptivo).
    Devuelve:  (lista_procesos_finales, timeline)
    timeline = [(pid, ciclo)]  ó  [(pid, inicio, dur)] si quieres bloques.
    """
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo, completados, n = 0, 0, len(procesos)
    timeline = []

    while completados < n:
        disponibles = [p for p in procesos if p.at <= tiempo and p.remaining > 0]

        if disponibles:
            actual = min(disponibles, key=lambda p: p.remaining)

            if actual.first_run:
                actual.start_time = tiempo
                actual.first_run = False

            actual.remaining -= 1
            timeline.append((actual.pid, tiempo))
            tiempo += 1

            if actual.remaining == 0:
                actual.end_time = tiempo
                actual.finished = True
                completados += 1
        else:
            tiempo += 1

    return procesos, timeline
