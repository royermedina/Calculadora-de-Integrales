"""
Clase principal que coordina todas las funcionalidades de la aplicación
"""
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from math_solver import MathSolver
from ui_manager import UIManager
from step_renderer import StepRenderer
from graph_manager import GraphManager

class MainApp:
    """Clase principal que coordina todas las funcionalidades de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        
        # Inicializar componentes
        self.ui_manager = UIManager(root)
        self.math_solver = MathSolver()
        
        # Crear panel de resultados usando StepRenderer
        main_container = None
        for child in root.winfo_children():
            if isinstance(child, tk.Frame) and child.cget('bg') == '#0d1117':
                main_container = child
                break
        
        if main_container:
            self.step_renderer = StepRenderer(root)
            result_frame = self.step_renderer.crear_panel_resultados(main_container)
        
        # Crear GraphManager
        self.graph_manager = GraphManager(
            self.ui_manager.graph_frame, 
            self.ui_manager.btn_cerrar_grafico
        )
        
        # Establecer referencias cruzadas
        self.ui_manager.set_step_renderer(self.step_renderer)
        self.ui_manager.set_graph_manager(self.graph_manager)
        self.ui_manager.set_main_app(self)
        
        # Variables de estado
        self.pasos_actuales = []
    
    def resolver_integral(self):
        """Resolver la integral paso a paso"""
        try:
            funcion_str = self.ui_manager.get_funcion_str()
            if not funcion_str:
                messagebox.showerror("Error", "Ingresa una función para integrar")
                return
            
            # Parsear la función
            x = Symbol(self.ui_manager.get_variable_str())
            try:
                funcion = parse_expr(funcion_str, transformations='all')
            except:
                messagebox.showerror("Error", f"No se puede interpretar la función: {funcion_str}")
                return
            
            # Resolver paso a paso usando MathSolver
            pasos, resultado = self.math_solver.resolver_integral_general(funcion, x)
            self.pasos_actuales = pasos
            
            # Mostrar resultados usando StepRenderer
            self.step_renderer.mostrar_pasos_detallados(
                pasos, resultado, funcion_str, self.ui_manager.get_variable_str()
            )
            
            # Si es definida, calcular valor numérico
            if self.ui_manager.get_tipo_integral() == "definida" and resultado:
                self.calcular_integral_definida(funcion, x, resultado)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def calcular_integral_definida(self, funcion, variable, antiderivada):
        """Calcular integral definida con pasos"""
        try:
            limite_inf_str, limite_sup_str = self.ui_manager.get_limites()
            limite_inf = parse_expr(limite_inf_str)
            limite_sup = parse_expr(limite_sup_str)
            
            # Evaluar en los límites
            valor_sup = antiderivada.subs(variable, limite_sup)
            valor_inf = antiderivada.subs(variable, limite_inf)
            resultado_def = simplify(valor_sup - valor_inf)
            
            # Agregar pasos de la integral definida
            pasos_definida = [{
                'titulo': 'Teorema Fundamental del Cálculo',
                'formula': f'F({limite_sup}) - F({limite_inf})',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) - F\\left({latex(limite_inf)}\\right)',
                'explicacion': 'Evaluamos la antiderivada en los límites de integración.',
                'tipo': 'metodo'
            }, {
                'titulo': 'Evaluación en límite superior',
                'formula': f'F({limite_sup}) = {valor_sup}',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) = {latex(valor_sup)}',
                'explicacion': f'Sustituimos x = {limite_sup} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': 'Evaluación en límite inferior',
                'formula': f'F({limite_inf}) = {valor_inf}',
                'formula_latex': f'F\\left({latex(limite_inf)}\\right) = {latex(valor_inf)}',
                'explicacion': f'Sustituimos x = {limite_inf} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': 'RESULTADO NUMÉRICO',
                'formula': f'{resultado_def}',
                'formula_latex': f'{latex(resultado_def)}',
                'explicacion': 'Resultado de la integral definida.',
                'tipo': 'resultado'
            }]
            
            # Agregar estos pasos a la visualización
            for paso in pasos_definida:
                self.pasos_actuales.append(paso)
            
            # Actualizar visualización
            self.step_renderer.mostrar_pasos_detallados(
                self.pasos_actuales, None, 
                self.ui_manager.get_funcion_str(), 
                self.ui_manager.get_variable_str()
            )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en integral definida: {str(e)}")
    
    def graficar_funcion(self):
        """Crear gráfico de la función y su integral"""
        funcion_str = self.ui_manager.get_funcion_str()
        self.graph_manager.crear_grafico(funcion_str, self.pasos_actuales)
    
    def exportar_solucion(self):
        """Exportar solución completa a PDF (gráficas + pasos)."""
        if not self.pasos_actuales:
            messagebox.showwarning("Advertencia", "Primero resuelve una integral")
            return
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivo PDF", "*.pdf")],
                title="Guardar PDF"
            )
            if not filename:
                return

            funcion_str = self.ui_manager.get_funcion_str()
            x = Symbol(self.ui_manager.get_variable_str())
            funcion = parse_expr(funcion_str, transformations='all')

            with PdfPages(filename) as pdf:
                # Página de gráficas
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
                fig.patch.set_facecolor('white')
                fig.subplots_adjust(hspace=0.35, top=0.95, bottom=0.08, left=0.1, right=0.98)
                x_vals = np.linspace(-5, 5, 1000)
                func_lamb = lambdify(x, funcion, 'numpy')
                with np.errstate(all='ignore'):
                    y_vals = func_lamb(x_vals)
                    y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
                ax1.plot(x_vals, y_vals, color='#2563eb', linewidth=2, label=f'f(x) = {funcion}')
                ax1.axhline(0, color='#9ca3af', linewidth=0.8)
                ax1.axvline(0, color='#9ca3af', linewidth=0.8)
                ax1.grid(True, alpha=0.3)
                ax1.set_title('Función Original')
                ax1.legend()

                try:
                    F = simplify(integrate(funcion, x))
                    F_lamb = lambdify(x, F, 'numpy')
                    with np.errstate(all='ignore'):
                        yI = F_lamb(x_vals)
                        yI = np.where(np.isfinite(yI), yI, np.nan)
                    ax2.plot(x_vals, yI, color='#16a34a', linewidth=2, label=f'∫f(x)dx = {F}')
                    ax2.axhline(0, color='#9ca3af', linewidth=0.8)
                    ax2.axvline(0, color='#9ca3af', linewidth=0.8)
                    ax2.grid(True, alpha=0.3)
                    ax2.set_title('Función Integral')
                    ax2.legend()
                except Exception:
                    ax2.text(0.5, 0.5, 'Integral no graficable', transform=ax2.transAxes,
                             ha='center', va='center')
                pdf.savefig(fig)
                plt.close(fig)

                # Páginas de pasos
                def nueva_pagina():
                    fig_steps = plt.figure(figsize=(8.27, 11.69))
                    fig_steps.patch.set_facecolor('white')
                    ax = fig_steps.add_axes([0.06, 0.04, 0.88, 0.92])
                    ax.axis('off')
                    return fig_steps, ax

                fig_s, ax_s = nueva_pagina()
                y = 0.96
                header = f"Solución Paso a Paso — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                ax_s.text(0.5, y, header, ha='center', va='top', fontsize=14, weight='bold')
                y -= 0.05
                tipo = self.ui_manager.get_tipo_integral()
                ax_s.text(0.06, y, f"Función: {funcion_str}  |  Tipo: {tipo}", fontsize=10)
                y -= 0.03

                for i, paso in enumerate(self.pasos_actuales, 1):
                    if y < 0.08:
                        pdf.savefig(fig_s)
                        plt.close(fig_s)
                        fig_s, ax_s = nueva_pagina()
                        y = 0.96
                    ax_s.text(0.06, y, f"Paso {i}: {paso.get('titulo','')}", fontsize=11, weight='bold')
                    y -= 0.03
                    formula_ltx = paso.get('formula_latex')
                    formula_txt = paso.get('formula')
                    if formula_ltx:
                        ax_s.text(0.08, y, f"${formula_ltx}$", fontsize=11)
                        y -= 0.035
                    elif formula_txt:
                        ax_s.text(0.08, y, str(formula_txt), fontsize=10, color='#374151')
                        y -= 0.03
                    explic = paso.get('explicacion')
                    if explic:
                        ax_s.text(0.08, y, explic, fontsize=9)
                        y -= 0.03
                    y -= 0.01

                pdf.savefig(fig_s)
                plt.close(fig_s)

            messagebox.showinfo("Éxito", f"PDF guardado en: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")
    
    def limpiar_todo(self):
        """Limpiar toda la interfaz"""
        # Limpiar campos de entrada
        self.ui_manager.funcion_var.set("")
        self.ui_manager.variable_var.set("x")
        self.ui_manager.limite_inf_var.set("0")
        self.ui_manager.limite_sup_var.set("1")
        self.ui_manager.tipo_integral.set("indefinida")
        
        # Limpiar pasos
        self.step_renderer.limpiar_pasos()
        self.pasos_actuales = []
        
        # Actualizar preview
        self.ui_manager.actualizar_preview()
        
        # Cerrar gráfico si existe
        self.graph_manager.cerrar_grafico()
        
        # Ocultar límites
        self.ui_manager.limites_frame.pack_forget()

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
