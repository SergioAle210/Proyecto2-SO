class SemaforoSimulador:
    """
    Semáforo contado:
    – WAIT  : P() / down  (mantiene el recurso hasta SIGNAL)
    – SIGNAL: V() / up
    – READ / WRITE se permiten como accesos rápidos de 1 ciclo si se desea
    """

    def __init__(self, procesos, recursos, acciones):
        self.procesos = {p.pid: p for p in procesos}
        self.recursos = recursos
        self.acciones = acciones
        self.ciclo = 0

    def ejecutar(self):
        tiempo_fin = max(a.ciclo for a in self.acciones) + 5

        while self.ciclo <= tiempo_fin:
            # acciones programadas para este ciclo
            for acc in (a for a in self.acciones if a.ciclo == self.ciclo):
                proc = self.procesos[acc.pid]
                rec = self.recursos[acc.recurso]

                if acc.tipo == "WAIT":  # P()
                    rec.acquire(proc, self.ciclo, auto_release=False)

                elif acc.tipo in ("READ", "WRITE"):  # acceso rápido
                    rec.acquire(proc, self.ciclo, auto_release=True)

                elif acc.tipo == "SIGNAL":  # V()
                    rec.signal(self.ciclo)

            # fin de ciclo: libera los auto_release y atiende cola
            for rec in self.recursos.values():
                rec.end_cycle(self.ciclo)

            self.ciclo += 1

        # marca de finalización
        for p in self.procesos.values():
            p.marca(self.ciclo, "DONE")

        return list(self.procesos.values())
