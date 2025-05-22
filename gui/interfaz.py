import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import random
from copy import deepcopy

from scheduler.utils import leer_procesos, calcular_metricas
from scheduler.fifo import fifo
from scheduler.sjf import sjf
from scheduler.srt import srt
from scheduler.round_robin import round_robin
from scheduler.priority import priority

from sync.sync_utils import (
    leer_procesos as leer_procesos_sync,
    leer_recursos,
    leer_acciones,
)
from sync.mutex import MutexSimulador
from sync.semaforo import SemaforoSimulador


class SimuladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistemas Operativos - UVG 2025")
        self.root.geometry("1200x800")

        self.procesos = []
        self.recursos = {}
        self.acciones = []
        self.colors = {}

        self.modo_var = tk.StringVar(value="calendarizacion")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.top_frame = tk.Frame(container)
        self.top_frame.pack(fill="x")

        self.left_panel = tk.Frame(self.top_frame)
        self.left_panel.pack(side="left", fill="y", padx=10)

        self.control_panel = tk.Frame(self.top_frame)
        self.control_panel.pack(side="left", fill="y", expand=True)

        # Modo de simulación
        tk.Label(
            self.left_panel, text="Modo de Simulación:", font=("Arial", 12, "bold")
        ).pack(pady=5)
        ttk.Radiobutton(
            self.left_panel,
            text="Calendarización",
            variable=self.modo_var,
            value="calendarizacion",
            command=self.actualizar_modo,
        ).pack(anchor="w")
        ttk.Radiobutton(
            self.left_panel,
            text="Sincronización",
            variable=self.modo_var,
            value="sincronizacion",
            command=self.actualizar_modo,
        ).pack(anchor="w")

        self.sync_selector = tk.Frame(self.left_panel)
        self.sync_tipo = tk.StringVar(value="mutex")
        ttk.Label(self.sync_selector, text="Tipo de sincronización:").pack(pady=5)
        ttk.Radiobutton(
            self.sync_selector, text="Mutex", variable=self.sync_tipo, value="mutex"
        ).pack(anchor="w")
        ttk.Radiobutton(
            self.sync_selector,
            text="Semáforo",
            variable=self.sync_tipo,
            value="semaforo",
        ).pack(anchor="w")

        self.algoritmos = {
            "FIFO": fifo,
            "SJF": sjf,
            "SRT": srt,
            "Round Robin": round_robin,
            "Priority": priority,
        }

        self.simulacion_frame = tk.Frame(self.left_panel)
        tk.Label(
            self.simulacion_frame,
            text="Seleccione uno o más algoritmos:",
            font=("Arial", 11),
        ).pack(pady=5)
        self.algoritmo_vars = {}
        for nombre in self.algoritmos:
            var = tk.BooleanVar(value=(nombre == "FIFO"))
            self.algoritmo_vars[nombre] = var
            ttk.Checkbutton(
                self.simulacion_frame,
                text=nombre,
                variable=var,
                command=self.actualizar_vista,
            ).pack(anchor="w", padx=10)

        self.quantum_frame = tk.Frame(self.simulacion_frame)
        self.quantum_label = tk.Label(self.quantum_frame, text="Quantum:")
        self.quantum_label.pack(side="left")
        self.quantum_entry = tk.Entry(self.quantum_frame, width=5)
        self.quantum_entry.insert(0, "3")
        self.quantum_entry.pack(side="left")
        self.quantum_frame.pack(pady=5)
        self.quantum_frame.pack_forget()

        self.boton_cargar = ttk.Button(
            self.control_panel, text="Cargar Procesos", command=self.cargar_procesos
        )
        self.boton_cargar.pack(pady=5)
        self.boton_simular = ttk.Button(
            self.control_panel, text="Simular", command=self.simular
        )
        self.boton_simular.pack(pady=5)
        self.boton_limpiar = ttk.Button(
            self.control_panel, text="Limpiar Procesos", command=self.limpiar_procesos
        )
        self.boton_limpiar.pack(pady=5)

        # Canvas con scroll horizontal y vertical bien posicionado
        self.canvas_frame = tk.Frame(container)
        self.canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.canvas_frame, bg="white", scrollregion=(0, 0, 5000, 2000)
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scroll_x = tk.Scrollbar(
            self.canvas_frame, orient="horizontal", command=self.canvas.xview
        )
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.scroll_y = tk.Scrollbar(
            self.canvas_frame, orient="vertical", command=self.canvas.yview
        )
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.canvas.config(
            xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set
        )

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # Leyenda de colores
        self.leyenda_frame = tk.Frame(container)
        self.leyenda_frame.pack(fill="x", pady=5)

        # Tabla de resumen
        self.tabla_frame = tk.Frame(container)
        self.tabla_frame.pack(fill="x", pady=10)

        self.tablas_contenedor = tk.Frame(self.tabla_frame)
        self.tablas_contenedor.pack(fill="x")

        self.frame_procesos = tk.Frame(self.tablas_contenedor)
        self.frame_procesos.pack(side="left", padx=10, fill="y")
        tk.Label(
            self.frame_procesos, text="Procesos", font=("Arial", 10, "bold")
        ).pack()
        self.tabla_procesos = tk.Text(
            self.frame_procesos, height=6, width=40, bg="#f4f4f4"
        )
        self.tabla_procesos.pack()

        self.frame_recursos = tk.Frame(self.tablas_contenedor)
        self.frame_recursos.pack(side="left", padx=10, fill="y")
        tk.Label(
            self.frame_recursos, text="Recursos", font=("Arial", 10, "bold")
        ).pack()
        self.tabla_recursos = tk.Text(
            self.frame_recursos, height=6, width=40, bg="#f4f4f4"
        )
        self.tabla_recursos.pack()

        self.frame_acciones = tk.Frame(self.tablas_contenedor)
        self.frame_acciones.pack(side="left", padx=10, fill="y")
        tk.Label(
            self.frame_acciones, text="Acciones", font=("Arial", 10, "bold")
        ).pack()
        self.tabla_acciones = tk.Text(
            self.frame_acciones, height=6, width=40, bg="#f4f4f4"
        )
        self.tabla_acciones.pack()

        self.frame_recursos.pack_forget()
        self.frame_acciones.pack_forget()

        # Métricas (fuera del área de canvas)
        self.metricas_label = tk.Label(
            container, text="", font=("Arial", 10), justify="left", anchor="w"
        )
        self.metricas_label.pack(fill="x", pady=(5, 0))

        self.actualizar_modo()

    def actualizar_modo(self):
        modo = self.modo_var.get()
        if modo == "calendarizacion":
            self.simulacion_frame.pack(fill="x", pady=10)
            self.sync_selector.pack_forget()
            self.frame_acciones.pack_forget()
            self.frame_recursos.pack_forget()
        else:
            self.simulacion_frame.pack_forget()
            self.sync_selector.pack(fill="x", pady=10)
            self.frame_acciones.pack(side="left", padx=10)
            self.frame_recursos.pack(side="left", padx=10)

    def actualizar_vista(self):
        if self.algoritmo_vars["Round Robin"].get():
            self.quantum_frame.pack(pady=5)
        else:
            self.quantum_frame.pack_forget()

    def cargar_procesos(self):
        modo = self.modo_var.get()
        archivo = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
        if not archivo:
            return
        contenido = []
        try:
            if modo == "calendarizacion":
                self.procesos = leer_procesos(archivo)
                contenido = [
                    f"{p.pid}, {p.bt}, {p.at}, {p.priority}" for p in self.procesos
                ]
                self.tabla_procesos.delete("1.0", tk.END)
                self.tabla_procesos.insert(tk.END, "\n".join(contenido))
            else:
                if "procesos" in archivo:
                    self.procesos = leer_procesos_sync(archivo)
                    contenido = [
                        f"{p.pid}, {p.bt}, {p.at}, {p.priority}" for p in self.procesos
                    ]
                    self.tabla_procesos.delete("1.0", tk.END)
                    self.tabla_procesos.insert(tk.END, "\n".join(contenido))
                elif "recursos" in archivo:
                    self.recursos = leer_recursos(archivo)
                    contenido = [
                        f"{r.nombre}, {r.contador}" for r in self.recursos.values()
                    ]
                    self.tabla_recursos.delete("1.0", tk.END)
                    self.tabla_recursos.insert(tk.END, "\n".join(contenido))
                elif "acciones" in archivo:
                    self.acciones = leer_acciones(archivo)
                    contenido = [
                        f"{a.pid}, {a.tipo}, {a.recurso}, {a.ciclo}"
                        for a in self.acciones
                    ]
                    self.tabla_acciones.delete("1.0", tk.END)
                    self.tabla_acciones.insert(tk.END, "\n".join(contenido))
        except Exception as e:
            messagebox.showerror(
                "Error de lectura", f"Ocurrió un error al cargar el archivo:\n{e}"
            )
            return

        self.colors = {p.pid: self.generar_color() for p in self.procesos}
        self.actualizar_leyenda()

    def limpiar_procesos(self):
        self.procesos = []
        self.recursos = {}
        self.acciones = []
        self.canvas.delete("all")
        self.tabla_procesos.delete("1.0", tk.END)
        self.tabla_recursos.delete("1.0", tk.END)
        self.tabla_acciones.delete("1.0", tk.END)
        self.metricas_label.config(text="")
        for widget in self.leyenda_frame.winfo_children():
            widget.destroy()
        messagebox.showinfo(
            "Limpieza",
            "Se han limpiado los procesos, recursos, acciones, canvas y leyenda.",
        )

    def generar_color(self):
        return f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}"

    def simular(self):
        self.canvas.delete("all")
        self.mostrar_metricas("", clear=True)
        modo = self.modo_var.get()
        if modo == "calendarizacion":
            if not self.procesos:
                messagebox.showwarning("Error", "Primero carga un archivo de procesos.")
                return
            for nombre, activo in self.algoritmo_vars.items():
                if activo.get():
                    funcion = self.algoritmos[nombre]
                    if nombre == "Round Robin":
                        try:
                            quantum = int(self.quantum_entry.get())
                            if quantum <= 0:
                                raise ValueError
                        except ValueError:
                            messagebox.showerror(
                                "Error",
                                "Quantum inválido. Ingrese un número entero > 0.",
                            )
                            continue
                        resultado = funcion(deepcopy(self.procesos), quantum)
                    else:
                        resultado = funcion(deepcopy(self.procesos))
                    self.dibujar_gantt(resultado, nombre)
                    avg_wt, avg_tat = calcular_metricas(resultado)
                    self.mostrar_metricas(
                        f"{nombre}: Tiempo de Espera Promedio: {avg_wt:.2f} ciclos | Turnaround: {avg_tat:.2f} ciclos"
                    )

        else:
            if not self.procesos or not self.recursos or not self.acciones:
                messagebox.showerror(
                    "Error", "Faltan procesos, recursos o acciones para simular."
                )
                return
            tipo = self.sync_tipo.get()
            if tipo == "mutex":
                simulador = MutexSimulador(self.procesos, self.recursos, self.acciones)
            else:
                simulador = SemaforoSimulador(
                    self.procesos, self.recursos, self.acciones
                )
            resultado = simulador.ejecutar()
            self.dibujar_sync(resultado)

    def dibujar_gantt(self, procesos, nombre_algoritmo=""):
        escala = 25
        x = 10
        # Calcular desplazamiento vertical en función de los algoritmos ya dibujados
        num_algoritmos_previos = self.metricas_label.cget("text").count("\n") + 1
        y_offset = self.canvas.bbox("all")[3] + 30 if self.canvas.bbox("all") else 40

        if nombre_algoritmo:
            self.canvas.create_text(
                10,
                y_offset - 20,
                anchor="nw",
                text=f"Algoritmo: {nombre_algoritmo}",
                font=("Arial", 10, "bold"),
            )

        timeline = []
        for p in procesos:
            for t in range(p.start_time, p.end_time):
                timeline.append((p.pid, t))

        for pid, ciclo in timeline:
            self.root.update()
            color = self.colors.get(pid, "#cccccc")
            self.canvas.create_rectangle(
                x, y_offset, x + escala, y_offset + 60, fill=color, outline="black"
            )
            self.canvas.create_text(
                x + escala // 2, y_offset + 30, text=pid, font=("Arial", 9)
            )
            self.canvas.create_text(
                x, y_offset + 70, text=str(ciclo), anchor="n", font=("Arial", 8)
            )
            x += escala
            time.sleep(0.03)

        if timeline:
            self.canvas.create_text(
                x,
                y_offset + 70,
                text=str(timeline[-1][1] + 1),
                anchor="n",
                font=("Arial", 8),
            )

    def dibujar_sync(self, procesos):
        escala = 25
        x = 10
        y_offset = self.canvas.bbox("all")[3] + 30 if self.canvas.bbox("all") else 40

        for p in procesos:
            for ciclo, estado in p.historial:
                self.root.update()
                color = "green" if estado == "ACCESSED" else "red"
                self.canvas.create_rectangle(
                    x, y_offset, x + escala, y_offset + 60, fill=color, outline="black"
                )
                self.canvas.create_text(
                    x + escala // 2, y_offset + 30, text=p.pid, font=("Arial", 9)
                )
                self.canvas.create_text(
                    x, y_offset + 70, text=str(ciclo), anchor="n", font=("Arial", 8)
                )
                x += escala
                time.sleep(0.05)

        if procesos and procesos[0].historial:
            self.canvas.create_text(
                x,
                y_offset + 70,
                text=str(procesos[0].historial[-1][0] + 1),
                anchor="n",
                font=("Arial", 8),
            )

    def mostrar_metricas(self, texto, clear=False):
        if clear:
            self.metricas_label.config(text="")
        else:
            actual = self.metricas_label.cget("text")
            nuevo = actual + "\n" + texto if actual else texto
            self.metricas_label.config(text=nuevo)

    def actualizar_leyenda(self):
        for widget in self.leyenda_frame.winfo_children():
            widget.destroy()
        for pid, color in self.colors.items():
            cubo = tk.Frame(self.leyenda_frame, bg=color, width=20, height=20)
            cubo.pack(side="left", padx=5, pady=5)
            etiqueta = tk.Label(self.leyenda_frame, text=pid)
            etiqueta.pack(side="left", padx=(0, 10))

    def limpiar_procesos(self):
        self.procesos = []
        self.recursos = {}
        self.acciones = []
        self.canvas.delete("all")
        self.tabla_procesos.delete("1.0", tk.END)
        self.tabla_recursos.delete("1.0", tk.END)
        self.tabla_acciones.delete("1.0", tk.END)
        self.metricas_label.config(text="")

        for widget in self.leyenda_frame.winfo_children():
            widget.pack_forget()
            widget.destroy()

        messagebox.showinfo(
            "Limpieza",
            "Se han limpiado los procesos, recursos, acciones, canvas y leyenda.",
        )
