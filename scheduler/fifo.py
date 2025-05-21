def fifo(procesos):
    """
    Algoritmo First In First Out (FIFO).
    Ejecuta los procesos en el orden en que llegan (por Arrival Time).
    """
    # Ordenamos por tiempo de llegada (AT)
    procesos = sorted(procesos, key=lambda p: p.at)
    tiempo = 0

    for p in procesos:
        if tiempo < p.at:
            tiempo = p.at
        p.start_time = tiempo
        tiempo += p.bt
        p.end_time = tiempo

    return procesos
