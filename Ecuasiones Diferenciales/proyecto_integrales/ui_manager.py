"""
Clase especializada para manejar la interfaz de usuario
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import *

class UIManager:
    """Clase especializada para manejar la interfaz de usuario"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Solucionador Avanzado de Integrales")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        
        # Variables de la interfaz
        self.funcion_var = tk.StringVar()
        self.variable_var = tk.StringVar(value="x")
        self.limite_inf_var = tk.StringVar(value="0")
        self.limite_sup_var = tk.StringVar(value="1")
        self.tipo_integral = tk.StringVar(value="indefinida")
        
        # Referencias a otros componentes
        self.step_renderer = None
        self.graph_manager = None
        
        self.crear_interfaz_profesional()
    
    def crear_interfaz_profesional(self):
        """Crear interfaz estilo Wolfram Alpha"""
        
        # Header principal
        self.crear_header()
        
        # Contenedor principal con 3 paneles
        main_container = tk.Frame(self.root, bg='#0d1117')
        main_container.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Panel izquierdo - Entrada
        self.crear_panel_entrada(main_container)
        
        # Panel central - Visualización
        self.crear_panel_visualizacion(main_container)
        
        # Panel derecho - Resultados (será manejado por StepRenderer)
        # Este se creará cuando se inicialice StepRenderer
    
    def crear_header(self):
        """Crear el header principal"""
        header_frame = tk.Frame(self.root, bg='#161b22', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🧮 Solucionador Avanzado de Integrales", 
                              font=("Segoe UI", 20, "bold"), fg='#58a6ff', bg='#161b22')
        title_label.pack(pady=12)
        
        subtitle_label = tk.Label(header_frame, text="Resolución paso a paso con fórmulas LaTeX", 
                                 font=("Segoe UI", 10), fg='#7d8590', bg='#161b22')
        subtitle_label.pack()
    
    def crear_panel_entrada(self, parent):
        """Panel de entrada de datos"""
        entrada_frame = tk.Frame(parent, bg='#21262d', relief='solid', bd=1)
        entrada_frame.pack(side='left', fill='y', padx=(0, 8))
        entrada_frame.configure(width=350)
        entrada_frame.pack_propagate(False)
        
        # Título del panel
        tk.Label(entrada_frame, text="📝 Configuración", font=("Segoe UI", 14, "bold"), 
                fg='#f0f6fc', bg='#21262d').pack(pady=12)
        
        # Función principal
        func_frame = tk.LabelFrame(entrada_frame, text="Función a integrar", 
                                  font=("Segoe UI", 10, "bold"), fg='#f0f6fc', bg='#21262d')
        func_frame.pack(fill='x', padx=15, pady=8)
        
        self.entry_funcion = tk.Entry(func_frame, textvariable=self.funcion_var, 
                                     font=("Consolas", 12), bg='#0d1117', fg='#f0f6fc',
                                     insertbackground='white', relief='solid', bd=1)
        self.entry_funcion.pack(fill='x', padx=8, pady=8)
        self.entry_funcion.bind('<KeyRelease>', self.actualizar_preview)
        
        # Panel de botones matemáticos mejorado
        self.crear_panel_botones_matematicos(entrada_frame)
        
        # Configuraciones adicionales
        self.crear_configuraciones(entrada_frame)
        
        # Botones de acción
        self.crear_botones_accion(entrada_frame)
    
    def crear_panel_botones_matematicos(self, parent):
        """Panel de botones matemáticos con fuentes más pequeñas"""
        botones_frame = tk.LabelFrame(parent, text="🔧 Biblioteca de Funciones", 
                                     font=("Segoe UI", 10, "bold"), fg='#f0f6fc', bg='#21262d')
        botones_frame.pack(fill='x', padx=15, pady=8)
        
        # Categorías de botones
        categorias = [
            ("Básicas", [("x²", "x**2"), ("x³", "x**3"), ("√x", "sqrt(x)"), ("1/x", "1/x"), ("e^x", "exp(x)")]),
            ("Trigonométricas", [("sen(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("tan(x)", "tan(x)"), ("ln(x)", "log(x)")]),
            ("Especiales", [("√(25-x²)", "sqrt(25-x**2)"), ("√(9-x²)", "sqrt(9-x**2)"), ("√(1-x²)", "sqrt(1-x**2)")]),
            ("Operadores", [("+", "+"), ("-", "-"), ("×", "*"), ("÷", "/"), ("()", "()")])
        ]
        
        for categoria, botones in categorias:
            cat_frame = tk.Frame(botones_frame, bg='#21262d')
            cat_frame.pack(fill='x', pady=1)
            
            tk.Label(cat_frame, text=categoria, font=("Segoe UI", 8, "bold"), 
                    fg='#7d8590', bg='#21262d').pack(anchor='w')
            
            btn_container = tk.Frame(cat_frame, bg='#21262d')
            btn_container.pack(fill='x')
            
            for texto, valor in botones:
                btn = tk.Button(btn_container, text=texto, 
                               command=lambda v=valor: self.insertar_funcion(v),
                               bg='#30363d', fg='#f0f6fc', font=("Segoe UI", 8),
                               relief='solid', bd=1, cursor='hand2',
                               activebackground='#40464d')
                btn.pack(side='left', padx=1, pady=1, fill='x', expand=True)
        
        # Botón limpiar
        tk.Button(botones_frame, text="🗑️ Limpiar", command=self.limpiar_entrada,
                 bg='#da3633', fg='white', font=("Segoe UI", 9, "bold"),
                 relief='solid', bd=1, cursor='hand2').pack(fill='x', padx=5, pady=4)
    
    def crear_configuraciones(self, parent):
        """Configuraciones adicionales con fuentes más pequeñas"""
        config_frame = tk.LabelFrame(parent, text="⚙️ Configuración", 
                                   font=("Segoe UI", 10, "bold"), fg='#f0f6fc', bg='#21262d')
        config_frame.pack(fill='x', padx=15, pady=8)
        
        # Variable
        var_frame = tk.Frame(config_frame, bg='#21262d')
        var_frame.pack(fill='x', padx=5, pady=4)
        tk.Label(var_frame, text="Variable:", fg='#f0f6fc', bg='#21262d', font=("Segoe UI", 9)).pack(side='left')
        tk.Entry(var_frame, textvariable=self.variable_var, width=8, 
                bg='#0d1117', fg='#f0f6fc', insertbackground='white', font=("Consolas", 10)).pack(side='right')
        
        # Tipo de integral
        tipo_frame = tk.Frame(config_frame, bg='#21262d')
        tipo_frame.pack(fill='x', padx=5, pady=4)
        tk.Label(tipo_frame, text="Tipo:", fg='#f0f6fc', bg='#21262d', font=("Segoe UI", 9)).pack(side='left')
        
        combo = ttk.Combobox(tipo_frame, textvariable=self.tipo_integral, 
                            values=["indefinida", "definida"], width=12, font=("Segoe UI", 9))
        combo.pack(side='right')
        combo.bind("<<ComboboxSelected>>", self.toggle_limites)
        
        # Límites (ocultos inicialmente)
        self.limites_frame = tk.Frame(config_frame, bg='#21262d')
        
        tk.Label(self.limites_frame, text="Límite inferior:", fg='#f0f6fc', bg='#21262d', font=("Segoe UI", 9)).pack(anchor='w')
        tk.Entry(self.limites_frame, textvariable=self.limite_inf_var, 
                bg='#0d1117', fg='#f0f6fc', insertbackground='white', font=("Consolas", 9)).pack(fill='x', pady=2)
        
        tk.Label(self.limites_frame, text="Límite superior:", fg='#f0f6fc', bg='#21262d', font=("Segoe UI", 9)).pack(anchor='w')
        tk.Entry(self.limites_frame, textvariable=self.limite_sup_var,
                bg='#0d1117', fg='#f0f6fc', insertbackground='white', font=("Consolas", 9)).pack(fill='x', pady=2)
    
    def crear_botones_accion(self, parent):
        """Botones de acción principales con fuentes ajustadas"""
        botones_frame = tk.Frame(parent, bg='#21262d')
        botones_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Button(botones_frame, text="🧮 RESOLVER", command=self.on_resolver_clicked,
                 bg='#238636', fg='white', font=("Segoe UI", 12, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=8).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="📊 GRAFICAR", command=self.on_graficar_clicked,
                 bg='#0969da', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=6).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="💾 EXPORTAR", command=self.on_exportar_clicked,
                 bg='#a855f7', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=6).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="🗑️ LIMPIAR TODO", command=self.on_limpiar_clicked,
                 bg='#da3633', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=6).pack(fill='x', pady=2)
    
    def crear_panel_visualizacion(self, parent):
        """Panel central para gráficos con botón de cerrar"""
        viz_frame = tk.Frame(parent, bg='#21262d', relief='solid', bd=1)
        viz_frame.pack(side='left', fill='both', expand=True, padx=(0, 8))
        
        # Header con título y botón cerrar
        header_viz = tk.Frame(viz_frame, bg='#21262d')
        header_viz.pack(fill='x', pady=8)
        
        tk.Label(header_viz, text="📊 Visualización", font=("Segoe UI", 14, "bold"), 
                fg='#f0f6fc', bg='#21262d').pack(side='left', padx=10)
        
        # Botón para cerrar gráfico
        self.btn_cerrar_grafico = tk.Button(header_viz, text="✖ Cerrar", 
                                           command=self.cerrar_grafico,
                                           bg='#da3633', fg='white', font=("Segoe UI", 8),
                                           relief='solid', bd=1, cursor='hand2')
        
        # Preview de la integral
        self.integral_preview = tk.Label(viz_frame, text="∫ f(x) dx", 
                                       font=("Times New Roman", 16), 
                                       fg='#58a6ff', bg='#0d1117', relief='solid', bd=1)
        self.integral_preview.pack(fill='x', padx=10, pady=(0, 8))
        
        # Marco para gráficos
        self.graph_frame = tk.Frame(viz_frame, bg='#0d1117')
        self.graph_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Placeholder para gráfico
        self.graph_placeholder = tk.Label(self.graph_frame, text="📈\nEl gráfico aparecerá aquí\ncuando resuelvas una integral", 
                font=("Segoe UI", 11), fg='#7d8590', bg='#0d1117')
        self.graph_placeholder.pack(expand=True)
    
    def insertar_funcion(self, funcion):
        """Insertar función en el campo de entrada"""
        if funcion == "()":
            pos = self.entry_funcion.index(tk.INSERT)
            self.entry_funcion.insert(pos, "()")
            self.entry_funcion.icursor(pos + 1)
        else:
            self.entry_funcion.insert(tk.END, funcion)
        self.actualizar_preview()
    
    def limpiar_entrada(self):
        """Limpiar campo de entrada"""
        self.entry_funcion.delete(0, tk.END)
        self.actualizar_preview()
    
    def actualizar_preview(self, event=None):
        """Actualizar el preview de la integral"""
        funcion = self.funcion_var.get()
        if funcion:
            if self.tipo_integral.get() == "definida":
                preview = f"∫[{self.limite_inf_var.get()}]^[{self.limite_sup_var.get()}] {funcion} dx"
            else:
                preview = f"∫ {funcion} dx"
        else:
            preview = "∫ f(x) dx"
        
        self.integral_preview.config(text=preview)
    
    def toggle_limites(self, event=None):
        """Mostrar/ocultar campos de límites"""
        if self.tipo_integral.get() == "definida":
            self.limites_frame.pack(fill='x', padx=5, pady=5)
        else:
            self.limites_frame.pack_forget()
        self.actualizar_preview()
    
    def cerrar_grafico(self):
        """Cerrar el gráfico actual y mostrar placeholder"""
        if self.graph_manager:
            self.graph_manager.cerrar_grafico()
    
    def set_step_renderer(self, step_renderer):
        """Establecer referencia al StepRenderer"""
        self.step_renderer = step_renderer
    
    def set_graph_manager(self, graph_manager):
        """Establecer referencia al GraphManager"""
        self.graph_manager = graph_manager
    
    def set_main_app(self, main_app):
        """Establecer referencia a la aplicación principal"""
        self.main_app = main_app
    
    # Callbacks para los botones (delegarán a MainApp)
    def on_resolver_clicked(self):
        """Callback para el botón resolver"""
        if hasattr(self, 'main_app'):
            self.main_app.resolver_integral()
    
    def on_graficar_clicked(self):
        """Callback para el botón graficar"""
        if hasattr(self, 'main_app'):
            self.main_app.graficar_funcion()
    
    def on_exportar_clicked(self):
        """Callback para el botón exportar"""
        if hasattr(self, 'main_app'):
            self.main_app.exportar_solucion()
    
    def on_limpiar_clicked(self):
        """Callback para el botón limpiar todo"""
        if hasattr(self, 'main_app'):
            self.main_app.limpiar_todo()
    
    def get_funcion_str(self):
        """Obtener la función como string"""
        return self.funcion_var.get().strip()
    
    def get_variable_str(self):
        """Obtener la variable como string"""
        return self.variable_var.get()
    
    def get_tipo_integral(self):
        """Obtener el tipo de integral"""
        return self.tipo_integral.get()
    
    def get_limites(self):
        """Obtener los límites de integración"""
        return self.limite_inf_var.get(), self.limite_sup_var.get()
