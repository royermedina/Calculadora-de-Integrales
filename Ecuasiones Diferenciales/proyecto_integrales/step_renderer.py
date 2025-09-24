"""
Clase especializada para renderizar pasos matemáticos con LaTeX
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from io import BytesIO
from PIL import Image, ImageTk
from sympy import *

class StepRenderer:
    """Clase especializada para renderizar pasos matemáticos con LaTeX"""
    
    def __init__(self, root):
        self.root = root
        self._img_cache = []  # cache para imágenes LaTeX
    
    def _latex_to_photoimage(self, latex_str, dpi=150, fontsize=14, pad=0.03):
        """Convierte LaTeX a imagen PhotoImage para Tkinter"""
        try:
            fig = plt.figure(figsize=(0.01, 0.01), dpi=dpi)
            fig.patch.set_alpha(0)
            if not (latex_str.strip().startswith("$") and latex_str.strip().endswith("$")):
                latex_str = f"${latex_str}$"
            txt = fig.text(0, 0, latex_str, fontsize=fontsize, color='white')
            fig.canvas.draw()
            bbox = txt.get_window_extent()
            w, h = bbox.width / dpi, bbox.height / dpi
            fig.set_size_inches(w + 2*pad, h + 2*pad)
            txt.set_position((pad, pad))
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=dpi, transparent=True,
                        bbox_inches='tight', pad_inches=0.0, facecolor='none')
            plt.close(fig)
            buf.seek(0)
            img = Image.open(buf)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error renderizando LaTeX: {e}")
            return None
    
    def crear_panel_resultados(self, parent):
        """Panel de resultados paso a paso con LaTeX y scroll horizontal"""
        result_frame = tk.Frame(parent, bg='#21262d', relief='solid', bd=1)
        result_frame.pack(side='right', fill='both', expand=True)
        result_frame.configure(width=450)

        tk.Label(result_frame, text="📋 Solución Paso a Paso",
                 font=("Segoe UI", 14, "bold"),
                 fg='#f0f6fc', bg='#21262d').pack(pady=8)

        # Crear un frame para el canvas y scrollbars
        canvas_container = tk.Frame(result_frame, bg='#21262d')
        canvas_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        # Canvas principal
        self.steps_canvas = tk.Canvas(canvas_container, bg='#0d1117', highlightthickness=0)
        
        # Scrollbars - vertical a la derecha, horizontal abajo
        v_scrollbar = ttk.Scrollbar(canvas_container, orient='vertical', command=self.steps_canvas.yview)
        h_scrollbar = ttk.Scrollbar(result_frame, orient='horizontal', command=self.steps_canvas.xview)
        
        # Frame interno
        self.steps_inner = tk.Frame(self.steps_canvas, bg='#0d1117')

        # Configurar scroll
        def configure_scroll_region(event):
            # Actualizar la región de scroll para incluir todo el contenido
            self.steps_canvas.update_idletasks()
            bbox = self.steps_canvas.bbox("all")
            if bbox:
                self.steps_canvas.configure(scrollregion=bbox)
                # Asegurar que el contenido interno tenga el ancho correcto
                content_width = bbox[2] - bbox[0]
                canvas_width = self.steps_canvas.winfo_width()
                if content_width > canvas_width:
                    self.steps_canvas.itemconfig(self.canvas_window, width=content_width)
                else:
                    self.steps_canvas.itemconfig(self.canvas_window, width=canvas_width)

        self.steps_inner.bind("<Configure>", configure_scroll_region)
        
        # Crear ventana en canvas
        self.canvas_window = self.steps_canvas.create_window((0, 0), window=self.steps_inner, anchor="nw")
        
        # Configurar scrollbars
        self.steps_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configurar redimensionado
        def configure_canvas_width(event):
            canvas_width = self.steps_canvas.winfo_width()
            if canvas_width > 1:  # Evitar division por cero
                # Obtener el ancho del contenido
                bbox = self.steps_canvas.bbox("all")
                if bbox:
                    content_width = bbox[2] - bbox[0]
                    # Usar el mayor entre el ancho del canvas y el contenido
                    final_width = max(canvas_width, content_width)
                    self.steps_canvas.itemconfig(self.canvas_window, width=final_width)
                else:
                    self.steps_canvas.itemconfig(self.canvas_window, width=canvas_width)
                # Actualizar la región de scroll
                self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all"))

        self.steps_canvas.bind("<Configure>", configure_canvas_width)
        
        # Empaquetar widgets correctamente
        # Canvas y scrollbar vertical en su contenedor
        self.steps_canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Scrollbar horizontal en el frame principal (abajo)
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Empaquetar el contenedor del canvas
        canvas_container.pack(fill='both', expand=True)
        
        # Configurar el scroll horizontal para que funcione correctamente
        def on_mousewheel(event):
            # Scroll horizontal con Shift + rueda del mouse
            if event.state & 0x1:  # Shift key
                self.steps_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            else:
                self.steps_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mousewheel para scroll
        self.steps_canvas.bind("<MouseWheel>", on_mousewheel)
        self.steps_inner.bind("<MouseWheel>", on_mousewheel)
        
        # Función para actualizar scroll después de agregar contenido
        def update_scroll():
            self.steps_canvas.update_idletasks()
            bbox = self.steps_canvas.bbox("all")
            if bbox:
                self.steps_canvas.configure(scrollregion=bbox)
                # Asegurar que el contenido tenga el ancho correcto
                content_width = bbox[2] - bbox[0]
                canvas_width = self.steps_canvas.winfo_width()
                if content_width > canvas_width:
                    self.steps_canvas.itemconfig(self.canvas_window, width=content_width)
                else:
                    self.steps_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.update_scroll = update_scroll
        
        return result_frame
    
    def mostrar_pasos_detallados(self, pasos, resultado, funcion_str, variable_str):
        """Mostrar los pasos con formato profesional y LaTeX con fuentes más pequeñas"""
        # Limpia pasos previos
        for w in self.steps_inner.winfo_children():
            w.destroy()
        self._img_cache.clear()

        header = tk.Label(self.steps_inner, text="SOLUCIÓN PASO A PASO",
                          font=("Segoe UI", 12, "bold"), fg='#58a6ff', bg='#0d1117')
        header.pack(anchor='w', pady=(0, 6))

        for paso in pasos:
            card = tk.Frame(self.steps_inner, bg='#0d1117',
                            highlightbackground='#30363d', highlightthickness=1)
            card.pack(fill='x', padx=2, pady=4)

            tk.Label(card, text=paso.get('titulo', ''), font=("Segoe UI", 9, "bold"),
                     fg='#f0f6fc', bg='#0d1117').pack(anchor='w', padx=6, pady=(6, 2))

            # Fórmula - Priorizar LaTeX si está disponible
            formula_latex = paso.get('formula_latex')
            formula_text = paso.get('formula')
            if formula_latex:
                img = self._latex_to_photoimage(formula_latex, fontsize=12)
                if img:
                    label_img = tk.Label(card, image=img, bg='#0d1117')
                    label_img.pack(anchor='w', padx=8, pady=3)
                    self._img_cache.append(img)
                else:
                    # Fallback a texto si LaTeX falla
                    tk.Label(card, text=formula_text or formula_latex, font=("Consolas", 9),
                             fg='#fbbf24', bg='#0d1117', wraplength=400).pack(anchor='w', padx=8, pady=3)
            elif formula_text:
                tk.Label(card, text=formula_text, font=("Consolas", 9),
                         fg='#fbbf24', bg='#0d1117', wraplength=400).pack(anchor='w', padx=8, pady=3)

            # Explicación
            if paso.get('explicacion'):
                tk.Label(card, text="💡 " + paso['explicacion'],
                         font=("Segoe UI", 8), fg='#9ca3af', bg='#0d1117',
                         wraplength=400, justify='left').pack(anchor='w', padx=8, pady=(0, 6))

        # Resultado final
        if resultado is not None:
            try:
                x = Symbol(variable_str)
                f = parse_expr(funcion_str)
                res_ltx = latex(Integral(f, x)) + "=" + latex(resultado) + "+C"
            except Exception:
                res_ltx = None

            card = tk.Frame(self.steps_inner, bg='#0d1117',
                            highlightbackground='#10b981', highlightthickness=2)
            card.pack(fill='x', padx=2, pady=8)
            tk.Label(card, text="🏆 RESULTADO FINAL",
                     font=("Segoe UI", 10, "bold"),
                     fg='#10b981', bg='#0d1117').pack(anchor='w', padx=6, pady=(6, 2))

            if res_ltx:
                img = self._latex_to_photoimage(res_ltx, fontsize=11)
                if img:
                    label_img = tk.Label(card, image=img, bg='#0d1117')
                    label_img.pack(anchor='w', padx=8, pady=6)
                    self._img_cache.append(img)
                else:
                    # Fallback a texto
                    tk.Label(card, text=f"∫ {funcion_str} dx = {resultado} + C",
                             font=("Consolas", 9), fg='#10b981', bg='#0d1117', 
                             wraplength=400).pack(anchor='w', padx=8, pady=6)
            else:
                tk.Label(card, text=f"∫ {funcion_str} dx = {resultado} + C",
                         font=("Consolas", 9), fg='#10b981', bg='#0d1117',
                         wraplength=400).pack(anchor='w', padx=8, pady=6)
        
        # Actualizar el scroll después de mostrar todos los pasos
        self.root.after(100, self.update_scroll)
    
    def limpiar_pasos(self):
        """Limpiar todos los pasos mostrados"""
        for w in self.steps_inner.winfo_children():
            w.destroy()
        self._img_cache.clear()
