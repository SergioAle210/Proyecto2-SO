def round_robin(procesos, quantum):
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo, index, completados, n = 0, 0, 0, len(procesos)
    queue, resultado, timeline = [], [], []

    while completados < n:
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

        run = min(quantum, actual.remaining)

        timeline.extend((actual.pid, t) for t in range(tiempo, tiempo + run))
        actual.timeline.append((tiempo, run))

        tiempo += run
        actual.remaining -= run

        while index < n and procesos[index].at <= tiempo:
            queue.append(procesos[index])
            index += 1

        if actual.remaining:
            queue.append(actual)
        else:
            actual.end_time = tiempo
            actual.finished = True
            resultado.append(actual)
            completados += 1

    return resultado, timeline
