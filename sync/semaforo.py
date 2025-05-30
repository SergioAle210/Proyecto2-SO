class SemaforoSimulador:

    def __init__(self, procesos, recursos, acciones):
        self.procesos = {p.pid: p for p in procesos}
        self.recursos = recursos
        self.acciones = acciones
        self.ciclo = 0

    def ejecutar(self):
        # ordenar acciones
        acciones = sorted(self.acciones, key=lambda a: a.ciclo)
        idx = 0  # siguiente acción a despachar

        #  función de parada
        pendientes_recursos = lambda: any(
            r.en_uso or r.cola_espera for r in self.recursos.values()
        )

        while idx < len(acciones) or pendientes_recursos():
            # 1) despachar todas las acciones de este ciclo
            while idx < len(acciones) and acciones[idx].ciclo == self.ciclo:
                acc = acciones[idx]
                idx += 1
                proc = self.procesos[acc.pid]
                rec = self.recursos[acc.recurso]

                if acc.tipo == "WAIT":  # P()
                    rec.acquire(proc, self.ciclo, auto_release=False)
                elif acc.tipo in ("READ", "WRITE"):
                    rec.acquire(proc, self.ciclo, auto_release=True)
                elif acc.tipo == "SIGNAL":  # V()
                    rec.signal(self.ciclo)

            # 2) final de ciclo: libera auto_release y despierta de la cola
            for rec in self.recursos.values():
                rec.end_cycle(self.ciclo)

            self.ciclo += 1

        # marca de finalización
        for p in self.procesos.values():
            p.marca(self.ciclo, "DONE")
        return list(self.procesos.values())
