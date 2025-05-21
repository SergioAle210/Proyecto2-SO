class MutexSimulador:
    def __init__(self, procesos, recursos, acciones):
        self.procesos = {p.pid: p for p in procesos}
        self.recursos = recursos
        self.acciones = acciones
        self.ciclo = 0
        self.finalizados = set()

    def ejecutar(self):
        tiempo_total = max(a.ciclo for a in self.acciones) + 10
        while self.ciclo <= tiempo_total:
            acciones_en_ciclo = [a for a in self.acciones if a.ciclo == self.ciclo]

            for accion in acciones_en_ciclo:
                proceso = self.procesos[accion.pid]
                recurso = self.recursos[accion.recurso]

                if accion.tipo in ["READ", "WRITE"]:
                    if recurso.contador > 0:
                        recurso.contador -= 1
                        proceso.estado = "ACCESSED"
                        proceso.historial.append((self.ciclo, "ACCESSED"))
                    else:
                        proceso.estado = "WAITING"
                        proceso.historial.append((self.ciclo, "WAITING"))
                        recurso.cola_espera.append(proceso)

            # Liberar recursos al final del ciclo
            for recurso in self.recursos.values():
                if recurso.cola_espera:
                    siguiente = recurso.cola_espera.pop(0)
                    recurso.contador -= 1
                    siguiente.estado = "ACCESSED"
                    siguiente.historial.append((self.ciclo, "ACCESSED"))

            self.ciclo += 1

        # Marcar procesos terminados
        for p in self.procesos.values():
            if p.estado == "ACCESSED":
                p.estado = "DONE"
                p.historial.append((self.ciclo, "DONE"))

        return list(self.procesos.values())
