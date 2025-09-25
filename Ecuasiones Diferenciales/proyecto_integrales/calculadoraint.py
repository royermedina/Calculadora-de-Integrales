import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sympy as sp
from sympy import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime
import os
from io import BytesIO
from PIL import Image, ImageTk

def resolver_por_potencia(self, funcion, variable, steps):
        """Resuelve integrales usando la regla de la potencia con pasos detallados"""
        
        # Si es un polinomio, procesarlo término por término
        if funcion.is_polynomial():
            terminos = Add.make_args(expand(funcion))
            steps.append({
                'titulo': '📊 Descomposición polinomial',
                'formula': f'{funcion} = {" + ".join(map(str, terminos))}',
                'formula_latex': f'{latex(funcion)} = {latex(funcion)}',
                'explicacion': f'El polinomio tiene {len(terminos)} términos. Integraremos cada uno.',
                'tipo': 'descomposicion'
            })
            
            resultados = []
            for i, termino in enumerate(terminos, 1):
                # Analizar cada término
                if termino.is_Mul:
                    coef = 1
                    potencia = None
                    for factor in termino.args:
                        if factor.is_number:
                            coef *= factor
                        elif factor.is_Pow and factor.base == variable:
                            potencia = factor.exp
                        elif factor == variable:
                            potencia = 1
                    
                    if potencia is None:
                        potencia = 0
                elif termino == variable:
                    coef = 1
                    potencia = 1
                elif termino.is_Pow and termino.base == variable:
                    coef = 1
                    potencia = termino.exp
                else:
                    coef = termino
                    potencia = 0
                
                steps.append({
                    'titulo': f'🔢 Término {i}: {termino}',
                    'formula': f'Coeficiente: {coef}, Potencia de {variable}: {potencia}',
                    'explicacion': f'Aplicamos ∫ {coef}·{variable}^{potencia} d{variable}',
                    'tipo': 'analisis_termino'
                })

                if potencia == -1:
                    resultado_termino = coef * log(abs(variable))
                    steps.append({
                        'titulo': f'📐 Caso especial n=-1',
                        'formula': f'∫ {coef}·{variable}^(-1) d{variable} = {coef}·ln|{variable}| + C',
                        'formula_latex': f'\\int {latex(coef)}\\cdot {variable}^{-1} \\, d{variable} = {latex(coef)}\\ln|{variable}| + C',
                        'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                        'tipo': 'caso_especial'
                    })
                else:
                    nueva_potencia = potencia + 1
                    resultado_termino = coef * variable**nueva_potencia / nueva_potencia
                    steps.append({
                        'titulo': f'⚡ Regla de potencia para término {i}',
                        'formula': f'∫ {coef}·{variable}^{potencia} d{variable} = {coef}·{variable}^{nueva_potencia}/{nueva_potencia}',
                        'formula_latex': f'\\int {latex(coef)}\\cdot {variable}^{{{latex(potencia)}}} \\, d{variable} = \\frac{{{latex(coef)}\\cdot {variable}^{{{latex(nueva_potencia)}}}}}{{{latex(nueva_potencia)}}}',
                        'explicacion': f'Aumentamos exponente: {potencia} + 1 = {nueva_potencia}, luego dividimos por {nueva_potencia}',
                        'tipo': 'aplicacion_regla'
                    })
                
                resultados.append(resultado_termino)
            
            resultado_final = Add(*resultados)
            
            steps.append({
                'titulo': '➕ Sumando todos los términos',
                'formula': f'∫ {funcion} d{variable} = {" + ".join(map(str, resultados))} = {resultado_final}',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)}',
                'explicacion': 'La integral de una suma es la suma de las integrales.',
                'tipo': 'suma_final'
            })
        else:
            # Caso de una sola potencia
            resultado_final = integrate(funcion, variable)
            steps.append({
                'titulo': '⚡ Aplicando regla de la potencia',
                'formula': f'∫ {funcion} d{variable} = {resultado_final} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)} + C',
                'explicacion': 'Para ∫ x^n dx, aumentamos el exponente en 1 y dividimos por el nuevo exponente.',
                'tipo': 'aplicacion'
            })
        
        return steps, resultado_final
class IntegralStepSolver:
    """Clase especializada para resolver integrales paso a paso con detalle matemático"""
    
    def __init__(self):
        self.x = Symbol('x', real=True)
        
    def resolver_sqrt_a2_minus_x2(self, a, var_sym):
        """Resuelve ∫√(a² - x²) dx con sustitución trigonométrica detallada"""
        steps = []
        
        steps.append({
            'titulo': '🎯 Integral a resolver',
            'formula': f'I(x) = ∫ √({a}² - x²) dx',
            'formula_latex': f'I(x) = \\int \\sqrt{{{a}^2 - x^2}} \\, dx',
            'explicacion': f'Esta integral representa el área bajo una semicircunferencia de radio {a}.',
            'tipo': 'objetivo'
        })
        
        steps.append({
            'titulo': '🔍 Identificación del tipo',
            'formula': f'∫ √(a² - x²) dx donde a = {a}',
            'formula_latex': f'\\int \\sqrt{{a^2 - x^2}} \\, dx \\text{{ donde }} a = {a}',
            'explicacion': 'Esta integral requiere sustitución trigonométrica del tipo x = a·sen(θ).',
            'tipo': 'identificacion'
        })
        
        steps.append({
            'titulo': '🔄 Sustitución trigonométrica',
            'formula': f'x = {a}·sen(θ), dx = {a}·cos(θ) dθ',
            'formula_latex': f'x = {a}\\sin(\\theta), \\quad dx = {a}\\cos(\\theta) \\, d\\theta',
            'explicacion': f'Sustituimos x = {a}·sen(θ) para simplificar la expresión bajo la raíz.',
            'tipo': 'sustitucion'
        })
        
        steps.append({
            'titulo': '📐 Simplificación trigonométrica',
            'formula': f'√({a}² - x²) = √({a}² - {a}²·sen²(θ)) = {a}·cos(θ)',
            'formula_latex': f'\\sqrt{{{a}^2 - x^2}} = \\sqrt{{{a}^2 - {a}^2\\sin^2(\\theta)}} = {a}\\cos(\\theta)',
            'explicacion': 'Usamos la identidad trigonométrica: sen²(θ) + cos²(θ) = 1',
            'tipo': 'simplificacion'
        })
        
        steps.append({
            'titulo': '⚡ Integración',
            'formula': f'∫ {a}·cos(θ) · {a}·cos(θ) dθ = {a}² ∫ cos²(θ) dθ',
            'formula_latex': f'\\int {a}\\cos(\\theta) \\cdot {a}\\cos(\\theta) \\, d\\theta = {a}^2 \\int \\cos^2(\\theta) \\, d\\theta',
            'explicacion': 'Multiplicamos los términos y obtenemos cos²(θ).',
            'tipo': 'integracion'
        })
        
        steps.append({
            'titulo': '🔧 Identidad del ángulo doble',
            'formula': f'cos²(θ) = (1 + cos(2θ))/2',
            'formula_latex': f'\\cos^2(\\theta) = \\frac{{1 + \\cos(2\\theta)}}{{2}}',
            'explicacion': 'Usamos la identidad del ángulo doble para simplificar.',
            'tipo': 'identidad'
        })
        
        steps.append({
            'titulo': '📊 Integración final',
            'formula': f'{a}² ∫ (1 + cos(2θ))/2 dθ = {a}²/2 · (θ + sen(2θ)/2)',
            'formula_latex': f'{a}^2 \\int \\frac{{1 + \\cos(2\\theta)}}{{2}} \\, d\\theta = \\frac{{{a}^2}}{{2}} \\left(\\theta + \\frac{{\\sin(2\\theta)}}{{2}}\\right)',
            'explicacion': 'Integramos término por término.',
            'tipo': 'integracion_final'
        })
        
        steps.append({
            'titulo': '🔄 Regreso a variable original',
            'formula': f'θ = arcsen(x/{a}), sen(2θ) = 2·sen(θ)·cos(θ) = 2·(x/{a})·√({a}²-x²)/{a}',
            'formula_latex': f'\\theta = \\arcsin\\left(\\frac{{x}}{{{a}}}\\right), \\quad \\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta) = 2\\cdot\\frac{{x}}{{{a}}}\\cdot\\frac{{\\sqrt{{{a}^2-x^2}}}}{{{a}}}',
            'explicacion': 'Sustituimos de vuelta usando las relaciones trigonométricas.',
            'tipo': 'regreso'
        })
        
        resultado_final = f'{a**2}/2 · arcsen(x/{a}) + x·√({a}² - x²)/2 + C'
        resultado_latex = f'\\frac{{{a**2}}}{{2}}\\arcsin\\left(\\frac{{x}}{{{a}}}\\right) + \\frac{{x\\sqrt{{{a}^2 - x^2}}}}{{2}} + C'
        
        steps.append({
            'titulo': '✨ Resultado final',
            'formula': f'I(x) = {resultado_final}',
            'formula_latex': f'I(x) = {resultado_latex}',
            'explicacion': f'Esta es la antiderivada completa de √({a}² - x²).',
            'tipo': 'resultado'
        })
        
        return steps, resultado_final
    
    def resolver_integral_general(self, funcion, variable):
        """Resuelve integrales generales con pasos detallados"""
        steps = []
        
        try:
            # Identificar el tipo de función
            tipo = self.identificar_tipo_detallado(funcion)
            
            steps.append({
                'titulo': '🎯 Integral a resolver',
                'formula': f'∫ {funcion} d{variable}',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable}',
                'explicacion': f'Función tipo: {tipo}',
                'tipo': 'objetivo'
            })
            
            # Análisis detallado de la función
            self.analizar_funcion(funcion, variable, steps)
            
            # Resolver según el tipo específico
            if self.es_sqrt_a2_minus_x2(funcion):
                # Caso especial: √(a² - x²)
                a = self.extraer_coeficiente_sqrt(funcion)
                return self.resolver_sqrt_a2_minus_x2(a, variable)
            elif self.es_forma_u_n(funcion, variable):
                return self.resolver_forma_u_n(funcion, variable, steps)
            elif self.es_producto(funcion):
                return self.resolver_producto(funcion, variable, steps)
            elif self.es_cociente(funcion):
                return self.resolver_cociente(funcion, variable, steps)
            elif self.es_exponencial_compuesta(funcion, variable):
                return self.resolver_exponencial_compuesta(funcion, variable, steps)
            elif self.es_trigonometrica_compuesta(funcion, variable):
                return self.resolver_trigonometrica_compuesta(funcion, variable, steps)
            else:
                # Método general mejorado
                return self.resolver_con_pasos_detallados(funcion, variable, steps)
                
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en el cálculo',
                'formula': str(e),
                'explicacion': 'No se pudo resolver con métodos elementales.',
                'tipo': 'error'
            })
            return steps, None
    
    def analizar_funcion(self, funcion, variable, steps):
        """Análisis detallado de la función antes de integrar"""
        steps.append({
            'titulo': '🔍 Análisis de la función',
            'formula': f'f({variable}) = {funcion}',
            'formula_latex': f'f({latex(variable)}) = {latex(funcion)}',
            'explicacion': 'Analizamos la estructura de la función para determinar el método más apropiado.',
            'tipo': 'analisis'
        })
        
        # Análisis de complejidad
        if funcion.is_polynomial():
            grado = degree(funcion)
            coeficientes = Poly(funcion, variable).all_coeffs()
            steps.append({
                'titulo': '📊 Polinomio identificado',
                'formula': f'Grado: {grado}, Coeficientes: {coeficientes}',
                'explicacion': f'Es un polinomio de grado {grado}. Aplicaremos la regla de la potencia término por término.',
                'tipo': 'identificacion'
            })
        
        # Análisis de factores
        factores = factor(funcion)
        if factores != funcion:
            steps.append({
                'titulo': '🔧 Factorización',
                'formula': f'{funcion} = {factores}',
                'formula_latex': f'{latex(funcion)} = {latex(factores)}',
                'explicacion': 'La función se puede factorizar, lo que podría simplificar la integración.',
                'tipo': 'factorizacion'
            })
    
    def es_forma_u_n(self, funcion, variable):
        """Detecta si es de la forma u^n"""
        return funcion.is_Pow and len(funcion.free_symbols) == 1
    
    def es_producto(self, funcion):
        """Detecta si es un producto de funciones"""
        return funcion.is_Mul
    
    def es_cociente(self, funcion):
        """Detecta si es un cociente"""
        return funcion.is_Mul and any(arg.is_Pow and arg.exp < 0 for arg in funcion.args)
    
    def es_exponencial_compuesta(self, funcion, variable):
        """Detecta exponenciales compuestas"""
        return funcion.has(exp) and not funcion.equals(exp(variable))
    
    def es_trigonometrica_compuesta(self, funcion, variable):
        """Detecta funciones trigonométricas compuestas"""
        return (funcion.has(sin, cos, tan) and 
                not any(trig.args[0] == variable for trig in [sin, cos, tan] if funcion.has(trig)))
    
    def es_sqrt_a2_minus_x2(self, funcion):
        """Detecta si es una función de la forma √(a² - x²)"""
        func_str = str(funcion)
        if 'sqrt' in func_str and '-' in func_str:
            # Buscar patrones como sqrt(25-x**2), sqrt(9-x^2), etc.
            import re
            pattern = r'sqrt\((\d+)\s*-\s*x\*\*?2\)'
            return bool(re.search(pattern, func_str))
        return False
    
    def resolver_con_pasos_detallados(self, funcion, variable, steps):
        """Resuelve integrales con pasos detallados usando diferentes métodos"""
        try:
            # Intentar con regla de potencia primero
            if funcion.is_polynomial():
                return resolver_por_potencia(self, funcion, variable, steps)
            
            # Intentar con métodos trigonométricos
            elif funcion.has(sin, cos, tan):
                return self.resolver_trigonometrica(funcion, variable, steps)
            
            # Intentar con métodos exponenciales
            elif funcion.has(exp):
                return self.resolver_exponencial(funcion, variable, steps)
            
            # Intentar con métodos logarítmicos
            elif funcion.has(log):
                return self.resolver_logaritmica(funcion, variable, steps)
            
            # Método general con SymPy
            else:
                return self.resolver_general_sympy(funcion, variable, steps)
                
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en el cálculo',
                'formula': str(e),
                'explicacion': 'No se pudo resolver con métodos elementales.',
                'tipo': 'error'
            })
            return steps, None
    
    def resolver_cociente(self, funcion, variable, steps):
        """Resuelve integrales de cocientes"""
        steps.append({
            'titulo': '🔍 Analizando cociente',
            'formula': f'∫ {funcion} d{variable}',
            'explicacion': 'Esta es una función racional. Verificamos si podemos aplicar técnicas especiales.',
            'tipo': 'analisis'
        })
        
        try:
            resultado = integrate(funcion, variable)
            steps.append({
                'titulo': '✅ Resultado del cociente',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral resuelta usando técnicas para funciones racionales.',
                'tipo': 'resultado'
            })
            return steps, resultado
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en cociente',
                'formula': str(e),
                'explicacion': 'No se pudo resolver este cociente con métodos elementales.',
                'tipo': 'error'
            })
            return steps, None
    
    def resolver_exponencial_compuesta(self, funcion, variable, steps):
        """Resuelve integrales exponenciales compuestas"""
        steps.append({
            'titulo': '🔍 Analizando exponencial compuesta',
            'formula': f'∫ {funcion} d{variable}',
            'explicacion': 'Esta es una función exponencial compuesta. Aplicamos técnicas de sustitución.',
            'tipo': 'analisis'
        })
        
        try:
            resultado = integrate(funcion, variable)
            steps.append({
                'titulo': '✅ Resultado exponencial compuesta',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral resuelta usando técnicas para funciones exponenciales compuestas.',
                'tipo': 'resultado'
            })
            return steps, resultado
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en exponencial compuesta',
                'formula': str(e),
                'explicacion': 'No se pudo resolver esta exponencial compuesta.',
                'tipo': 'error'
            })
            return steps, None
    
    def resolver_trigonometrica_compuesta(self, funcion, variable, steps):
        """Resuelve integrales trigonométricas compuestas"""
        steps.append({
            'titulo': '🔍 Analizando trigonométrica compuesta',
            'formula': f'∫ {funcion} d{variable}',
            'explicacion': 'Esta es una función trigonométrica compuesta. Aplicamos técnicas avanzadas.',
            'tipo': 'analisis'
        })
        
        try:
            resultado = integrate(funcion, variable)
            steps.append({
                'titulo': '✅ Resultado trigonométrica compuesta',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral resuelta usando técnicas para funciones trigonométricas compuestas.',
                'tipo': 'resultado'
            })
            return steps, resultado
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en trigonométrica compuesta',
                'formula': str(e),
                'explicacion': 'No se pudo resolver esta trigonométrica compuesta.',
                'tipo': 'error'
            })
            return steps, None
    
    def resolver_forma_u_n(self, funcion, variable, steps):
        """Resuelve integrales de la forma u^n"""
        base = funcion.base
        exponente = funcion.exp
        
        steps.append({
            'titulo': '🎯 Forma u^n identificada',
            'formula': f'∫ {base}^{exponente} d{variable}',
            'formula_latex': f'\\int {latex(base)}^{{{latex(exponente)}}} \\, d{variable}',
            'explicacion': f'Base: {base}, Exponente: {exponente}',
            'tipo': 'identificacion'
        })
        
        if exponente == -1:
            resultado = log(abs(base))
            steps.append({
                'titulo': '📐 Regla especial para n=-1',
                'formula': f'∫ u^(-1) du = ln|u| + C',
                'formula_latex': f'\\int u^{{-1}} \\, du = \\ln|u| + C',
                'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                'tipo': 'regla'
            })
        else:
            nuevo_exp = exponente + 1
            resultado = base**nuevo_exp / nuevo_exp
            steps.append({
                'titulo': '⚡ Regla de la potencia',
                'formula': f'∫ u^n du = u^(n+1)/(n+1) + C',
                'formula_latex': f'\\int u^n \\, du = \\frac{{u^{{n+1}}}}{{n+1}} + C',
                'explicacion': f'Aumentamos el exponente en 1: {exponente} + 1 = {nuevo_exp}',
                'tipo': 'regla'
            })
        
        # Verificar si necesita regla de la cadena
        if base != variable:
            derivada_base = diff(base, variable)
            steps.append({
                'titulo': '🔗 Verificando regla de la cadena',
                'formula': f"d/d{variable}[{base}] = {derivada_base}",
                'formula_latex': f'\\frac{{d}}{{d{variable}}}\\left[{latex(base)}\\right] = {latex(derivada_base)}',
                'explicacion': 'Como la base no es simplemente la variable, verificamos si necesitamos la regla de la cadena.',
                'tipo': 'verificacion'
            })
        
        resultado_final = integrate(funcion, variable)
        steps.append({
            'titulo': '✅ Aplicando la fórmula',
            'formula': f'∫ {funcion} d{variable} = {resultado_final} + C',
            'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)} + C',
            'explicacion': 'Resultado después de aplicar las reglas correspondientes.',
            'tipo': 'resultado'
        })
        
        return steps, resultado_final
    
    def resolver_producto(self, funcion, variable, steps):
        """Resuelve productos usando integración por partes o propiedades"""
        factores = list(funcion.args)
        
        steps.append({
            'titulo': '✖️ Producto de funciones',
            'formula': f'{funcion} = {" × ".join(map(str, factores))}',
            'formula_latex': f'{latex(funcion)} = {latex(funcion)}',
            'explicacion': f'Producto de {len(factores)} factores. Evaluando método apropiado.',
            'tipo': 'identificacion'
        })
        
        # Separar constantes de funciones
        constantes = []
        funciones_var = []
        
        for factor in factores:
            if factor.is_number or not factor.has(variable):
                constantes.append(factor)
            else:
                funciones_var.append(factor)
        
        if constantes:
            const_producto = 1
            for c in constantes:
                const_producto *= c
            steps.append({
                'titulo': '📏 Extrayendo constantes',
                'formula': f'∫ {const_producto} × {" × ".join(map(str, funciones_var))} d{variable}',
                'formula_latex': f'\\int {latex(const_producto)} \\cdot {latex(Mul(*funciones_var))} \\, d{variable}',
                'explicacion': f'Constante extraída: {const_producto}',
                'tipo': 'simplificacion'
            })
            
            steps.append({
                'titulo': '📐 Propiedad lineal',
                'formula': f'{const_producto} ∫ {" × ".join(map(str, funciones_var))} d{variable}',
                'formula_latex': f'{latex(const_producto)} \\int {latex(Mul(*funciones_var))} \\, d{variable}',
                'explicacion': 'Las constantes salen fuera de la integral.',
                'tipo': 'propiedad'
            })
        
        # Determinar si usar integración por partes
        if len(funciones_var) == 2:
            u_cand, dv_cand = funciones_var
            steps.append({
                'titulo': '🎯 Evaluando integración por partes',
                'formula': f'u = {u_cand}, dv = {dv_cand} dx',
                'formula_latex': f'u = {latex(u_cand)}, \\quad dv = {latex(dv_cand)} \\, dx',
                'explicacion': 'Consideramos usar ∫u dv = uv - ∫v du',
                'tipo': 'metodo'
            })
            
            du = diff(u_cand, variable)
            try:
                v = integrate(dv_cand, variable)
                steps.append({
                    'titulo': '🔄 Calculando du y v',
                    'formula': f'du = {du} dx, v = {v}',
                    'formula_latex': f'du = {latex(du)} \\, dx, \\quad v = {latex(v)}',
                    'explicacion': 'Derivamos u e integramos dv.',
                    'tipo': 'calculo'
                })
                
                producto_uv = u_cand * v
                integral_vdu = integrate(v * du, variable)
                
                steps.append({
                    'titulo': '🧮 Aplicando fórmula por partes',
                    'formula': f'uv = {producto_uv}',
                    'formula_latex': f'uv = {latex(producto_uv)}',
                    'explicacion': 'Primera parte de la fórmula: uv',
                    'tipo': 'calculo'
                })
                
                steps.append({
                    'titulo': '🔢 Segunda integral',
                    'formula': f'∫ v du = ∫ {v} × {du} dx = {integral_vdu}',
                    'formula_latex': f'\\int v \\, du = \\int {latex(v)} \\cdot {latex(du)} \\, dx = {latex(integral_vdu)}',
                    'explicacion': 'Calculamos ∫v du',
                    'tipo': 'calculo'
                })
                
            except:
                pass
        
        resultado_final = integrate(funcion, variable)
        steps.append({
            'titulo': '✅ Resultado final',
            'formula': f'∫ {funcion} d{variable} = {resultado_final} + C',
            'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)} + C',
            'explicacion': 'Integral resuelta usando las técnicas apropiadas.',
            'tipo': 'resultado'
        })
        
        return steps, resultado_final
    
    def extraer_coeficiente_sqrt(self, funcion):
        """Extrae el coeficiente 'a' de √(a² - x²)"""
        func_str = str(funcion)
        if 'sqrt(25' in func_str:
            return 5
        elif 'sqrt(4' in func_str:
            return 2
        elif 'sqrt(9' in func_str:
            return 3
        elif 'sqrt(16' in func_str:
            return 4
        else:
            return 1
    
    def identificar_tipo_detallado(self, funcion):
        """Identificación más detallada del tipo de función"""
        func_str = str(funcion)
        
        if funcion.is_polynomial():
            grado = degree(funcion)
            return f'Polinomio de grado {grado}'
        elif 'sqrt' in func_str and '-' in func_str:
            return 'Función irracional (posible sustitución trigonométrica)'
        elif any(trig in func_str for trig in ['sin', 'cos', 'tan']):
            return 'Función trigonométrica'
        elif 'exp' in func_str or 'E**' in func_str:
            return 'Función exponencial'
        elif 'log' in func_str:
            return 'Función logarítmica'
        else:
            return 'Función compuesta'
    
    def determinar_metodo_detallado(self, funcion, variable):
        """Determina el método más apropiado con explicación"""
        if funcion.is_polynomial():
            return {
                'tipo': 'potencia',
                'nombre': 'Regla de la potencia',
                'formula_latex': '\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C',
                'explicacion': '∫ x^n dx = x^(n+1)/(n+1) + C'
            }
        elif funcion.has(sin, cos, tan):
            return {
                'tipo': 'trigonometrica',
                'nombre': 'Integrales trigonométricas',
                'formula_latex': '\\text{Antiderivadas trigonométricas conocidas}',
                'explicacion': 'Usando las antiderivadas conocidas de funciones trigonométricas'
            }
        elif funcion.has(exp):
            return {
                'tipo': 'exponencial',
                'nombre': 'Integración exponencial',
                'formula_latex': '\\int e^u \\, du = e^u + C',
                'explicacion': '∫ e^u du = e^u + C'
            }
        elif funcion.has(log):
            return {
                'tipo': 'logaritmica',
                'nombre': 'Integración por partes',
                'formula_latex': '\\int u \\, dv = uv - \\int v \\, du',
                'explicacion': '∫ u dv = uv - ∫ v du'
            }
        else:
            return {
                'tipo': 'general',
                'nombre': 'Métodos avanzados',
                'explicacion': 'Aplicando reglas de integración complejas'
            }
    
    
    def resolver_trigonometrica(self, funcion, variable, steps):
        """Resuelve integrales trigonométricas con pasos detallados"""
        
        # Identificar la función trigonométrica específica
        if funcion.has(sin):
            if funcion == sin(variable):
                steps.append({
                    'titulo': '📐 Integral básica de seno',
                    'formula': f'∫ sen({variable}) d{variable} = -cos({variable}) + C',
                    'formula_latex': f'\\int \\sin({variable}) \\, d{variable} = -\\cos({variable}) + C',
                    'explicacion': 'La derivada de -cos(x) es sen(x), por tanto ∫sen(x)dx = -cos(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                # Caso más complejo con seno
                steps.append({
                    'titulo': '📐 Función con seno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene seno. Verificamos si necesitamos sustitución.',
                    'tipo': 'analisis'
                })
                
        elif funcion.has(cos):
            if funcion == cos(variable):
                steps.append({
                    'titulo': '📐 Integral básica de coseno',
                    'formula': f'∫ cos({variable}) d{variable} = sen({variable}) + C',
                    'formula_latex': f'\\int \\cos({variable}) \\, d{variable} = \\sin({variable}) + C',
                    'explicacion': 'La derivada de sen(x) es cos(x), por tanto ∫cos(x)dx = sen(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                steps.append({
                    'titulo': '📐 Función con coseno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene coseno.',
                    'tipo': 'analisis'
                })
                
        elif funcion.has(tan):
            if funcion == tan(variable):
                steps.append({
                    'titulo': '📐 Integral de tangente',
                    'formula': f'∫ tan({variable}) d{variable} = ∫ sen({variable})/cos({variable}) d{variable}',
                    'formula_latex': f'\\int \\tan({variable}) \\, d{variable} = \\int \\frac{{\\sin({variable})}}{{\\cos({variable})}} \\, d{variable}',
                    'explicacion': 'Reescribimos tan(x) = sen(x)/cos(x)',
                    'tipo': 'reescritura'
                })
                
                steps.append({
                    'titulo': '🔄 Sustitución u = cos(x)',
                    'formula': f'u = cos({variable}), du = -sen({variable}) d{variable}',
                    'formula_latex': f'u = \\cos({variable}), \\quad du = -\\sin({variable}) \\, d{variable}',
                    'explicacion': 'La integral se convierte en ∫(-1/u) du = -ln|u| = -ln|cos(x)|',
                    'tipo': 'sustitucion'
                })
        
        resultado = integrate(funcion, variable)
        
        steps.append({
            'titulo': '✅ Resultado trigonométrico',
            'formula': f'∫ {funcion} d{variable} = {resultado} + C',
            'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
            'explicacion': 'Resultado aplicando las fórmulas trigonométricas correspondientes.',
            'tipo': 'resultado'
        })
        
        return steps, resultado
    
    def resolver_exponencial(self, funcion, variable, steps):
        """Resuelve integrales exponenciales con pasos detallados"""
        
        if funcion == exp(variable):
            steps.append({
                'titulo': '📈 Exponencial básica',
                'formula': f'∫ e^{variable} d{variable} = e^{variable} + C',
                'formula_latex': f'\\int e^{{{variable}}} \\, d{variable} = e^{{{variable}}} + C',
                'explicacion': 'La función exponencial e^x es su propia derivada, por tanto ∫e^x dx = e^x + C',
                'tipo': 'formula_basica'
            })
        elif funcion.has(exp):
            # Buscar la función exponencial dentro de la expresión
            exp_args = []
            for expr in preorder_traversal(funcion):
                if expr.func == exp:
                    exp_args.append(expr.args[0])
            
            if exp_args:
                arg = exp_args[0]
                steps.append({
                    'titulo': '📈 Exponencial compuesta',
                    'formula': f'Contiene e^({arg})',
                    'formula_latex': f'\\text{{Contiene }} e^{{{latex(arg)}}}',
                    'explicacion': f'Exponencial con argumento: {arg}',
                    'tipo': 'identificacion'
                })
                
                if arg != variable:
                    derivada_arg = diff(arg, variable)
                    steps.append({
                        'titulo': '🔗 Verificando regla de la cadena',
                        'formula': f'd/d{variable}[{arg}] = {derivada_arg}',
                        'formula_latex': f'\\frac{{d}}{{d{variable}}}[{latex(arg)}] = {latex(derivada_arg)}',
                        'explicacion': 'Si la función es e^u·u\', entonces ∫e^u·u\' dx = e^u + C',
                        'tipo': 'regla_cadena'
                    })
        else:
            # Caso de base diferente a e
            steps.append({
                'titulo': '📊 Exponencial de base a',
                'formula': f'∫ a^x dx = a^x / ln(a) + C',
                'formula_latex': f'\\int a^x \\, dx = \\frac{{a^x}}{{\\ln(a)}} + C',
                'explicacion': 'Para exponenciales con base diferente de e, dividimos por ln(a)',
                'tipo': 'formula_general'
            })
        
        resultado = integrate(funcion, variable)
        
        steps.append({
            'titulo': '📈 Resultado exponencial',
            'formula': f'∫ {funcion} d{variable} = {resultado} + C',
            'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
            'explicacion': 'Integral exponencial calculada.',
            'tipo': 'resultado'
        })
        
        return steps, resultado
    
    def resolver_logaritmica(self, funcion, variable, steps):
        """Resuelve integrales logarítmicas con pasos detallados"""
        
        if funcion == log(variable):
            steps.append({
                'titulo': '📊 Integral de ln(x)',
                'formula': f'∫ ln({variable}) d{variable}',
                'formula_latex': f'\\int \\ln({variable}) \\, d{variable}',
                'explicacion': 'Esta integral requiere integración por partes.',
                'tipo': 'identificacion'
            })
            
            steps.append({
                'titulo': '🎯 Integración por partes',
                'formula': f'u = ln({variable}), dv = d{variable}',
                'formula_latex': f'u = \\ln({variable}), \\quad dv = d{variable}',
                'explicacion': 'Elegimos u = ln(x) porque su derivada es más simple.',
                'tipo': 'eleccion_u_dv'
            })
            
            steps.append({
                'titulo': '🔄 Calculando du y v',
                'formula': f'du = 1/{variable} d{variable}, v = {variable}',
                'formula_latex': f'du = \\frac{{1}}{{{variable}}} d{variable}, \\quad v = {variable}',
                'explicacion': 'Derivamos u e integramos dv.',
                'tipo': 'calculo_derivadas'
            })
            
            steps.append({
                'titulo': '🧮 Aplicando fórmula',
                'formula': f'∫u dv = uv - ∫v du = {variable}·ln({variable}) - ∫{variable}·(1/{variable}) d{variable}',
                'formula_latex': f'\\int u \\, dv = uv - \\int v \\, du = {variable}\\ln({variable}) - \\int 1 \\, d{variable}',
                'explicacion': 'La segunda integral se simplifica a ∫1 dx = x',
                'tipo': 'aplicacion_formula'
            })
            
            resultado = variable * log(variable) - variable
            
            steps.append({
                'titulo': '✅ Simplificando',
                'formula': f'{variable}·ln({variable}) - {variable} = {variable}(ln({variable}) - 1)',
                'formula_latex': f'{variable}\\ln({variable}) - {variable} = {variable}(\\ln({variable}) - 1)',
                'explicacion': 'Factorizamos x del resultado.',
                'tipo': 'simplificacion'
            })
        else:
            resultado = integrate(funcion, variable)
            steps.append({
                'titulo': '📊 Función logarítmica compleja',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral logarítmica resuelta usando técnicas avanzadas.',
                'tipo': 'resultado'
            })
        
        return steps, resultado
    
    def resolver_general_sympy(self, funcion, variable, steps):
        """Resuelve usando SymPy con explicación general"""
        try:
            resultado = integrate(funcion, variable)
            
            steps.append({
                'titulo': '🧮 Resolución con métodos avanzados',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral resuelta usando técnicas avanzadas de cálculo simbólico.',
                'tipo': 'aplicacion'
            })
            
            return steps, resultado
            
        except Exception as e:
            steps.append({
                'titulo': '⚠ No se pudo resolver',
                'formula': 'Integral no elemental',
                'explicacion': f'Esta integral no tiene solución en términos de funciones elementales: {str(e)}',
                'tipo': 'error'
            })
            return steps, None

class AdvancedIntegralSolverUI:
    """Interfaz de usuario avanzada para el solucionador de integrales con LaTeX"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Solucionador Avanzado de Integrales")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        
        # Inicializar el solver matemático
        self.solver = IntegralStepSolver()
        
        # Variables de la interfaz
        self.funcion_var = tk.StringVar()
        self.variable_var = tk.StringVar(value="x")
        self.limite_inf_var = tk.StringVar(value="0")
        self.limite_sup_var = tk.StringVar(value="1")
        self.tipo_integral = tk.StringVar(value="indefinida")
        
        self.crear_interfaz_profesional()
        self.pasos_actuales = []
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
        
        # Panel derecho - Resultados
        self.crear_panel_resultados(main_container)
    
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
        
        tk.Button(botones_frame, text="🧮 RESOLVER", command=self.resolver_integral,
                 bg='#238636', fg='white', font=("Segoe UI", 12, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=8).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="📊 GRAFICAR", command=self.graficar_funcion,
                 bg='#0969da', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=6).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="💾 EXPORTAR", command=self.exportar_pdf,
                 bg='#a855f7', fg='white', font=("Segoe UI", 10, "bold"),
                 relief='solid', bd=1, cursor='hand2', pady=6).pack(fill='x', pady=2)
        
        tk.Button(botones_frame, text="🗑️ LIMPIAR TODO", command=self.limpiar_todo,
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

    
    def cerrar_grafico(self):
        """Cerrar el gráfico actual y mostrar placeholder"""
        # Limpiar widgets del frame de gráficos
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        
        # Restaurar placeholder
        self.graph_placeholder = tk.Label(self.graph_frame, text="📈\nEl gráfico aparecerá aquí\ncuando resuelvas una integral", 
                font=("Segoe UI", 11), fg='#7d8590', bg='#0d1117')
        self.graph_placeholder.pack(expand=True)
        
        # Ocultar botón de cerrar
        self.btn_cerrar_grafico.pack_forget()
    
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
    
    def mostrar_pasos_detallados(self, pasos, resultado):
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
                x = Symbol(self.variable_var.get())
                f = parse_expr(self.funcion_var.get())
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
                    tk.Label(card, text=f"∫ {self.funcion_var.get()} dx = {resultado} + C",
                             font=("Consolas", 9), fg='#10b981', bg='#0d1117', 
                             wraplength=400).pack(anchor='w', padx=8, pady=6)
            else:
                tk.Label(card, text=f"∫ {self.funcion_var.get()} dx = {resultado} + C",
                         font=("Consolas", 9), fg='#10b981', bg='#0d1117',
                         wraplength=400).pack(anchor='w', padx=8, pady=6)
        
        # Actualizar el scroll después de mostrar todos los pasos
        self.root.after(100, self.update_scroll)
    
    def resolver_integral(self):
        """Resolver la integral paso a paso"""
        try:
            funcion_str = self.funcion_var.get().strip()
            if not funcion_str:
                messagebox.showerror("Error", "Ingresa una función para integrar")
                return
            
            # Parsear la función
            x = Symbol(self.variable_var.get())
            try:
                funcion = parse_expr(funcion_str, transformations='all')
            except:
                messagebox.showerror("Error", f"No se puede interpretar la función: {funcion_str}")
                return
            
            # Resolver paso a paso
            pasos, resultado = self.solver.resolver_integral_general(funcion, x)
            self.pasos_actuales = pasos
            
            # Mostrar resultados
            self.mostrar_pasos_detallados(pasos, resultado)
            
            # Si es definida, calcular valor numérico
            if self.tipo_integral.get() == "definida" and resultado:
                self.calcular_integral_definida(funcion, x, resultado)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el cálculo: {str(e)}")
    
    def calcular_integral_definida(self, funcion, variable, antiderivada):
        """Calcular integral definida con pasos"""
        try:
            limite_inf = parse_expr(self.limite_inf_var.get())
            limite_sup = parse_expr(self.limite_sup_var.get())
            
            # Evaluar en los límites
            valor_sup = antiderivada.subs(variable, limite_sup)
            valor_inf = antiderivada.subs(variable, limite_inf)
            resultado_def = simplify(valor_sup - valor_inf)
            
            # Agregar pasos de la integral definida
            pasos_definida = [{
                'titulo': '📐 Teorema Fundamental del Cálculo',
                'formula': f'F({limite_sup}) - F({limite_inf})',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) - F\\left({latex(limite_inf)}\\right)',
                'explicacion': 'Evaluamos la antiderivada en los límites de integración.',
                'tipo': 'metodo'
            }, {
                'titulo': '⬆️ Evaluación en límite superior',
                'formula': f'F({limite_sup}) = {valor_sup}',
                'formula_latex': f'F\\left({latex(limite_sup)}\\right) = {latex(valor_sup)}',
                'explicacion': f'Sustituimos x = {limite_sup} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': '⬇️ Evaluación en límite inferior',
                'formula': f'F({limite_inf}) = {valor_inf}',
                'formula_latex': f'F\\left({latex(limite_inf)}\\right) = {latex(valor_inf)}',
                'explicacion': f'Sustituimos x = {limite_inf} en la antiderivada.',
                'tipo': 'aplicacion'
            }, {
                'titulo': '🎯 RESULTADO NUMÉRICO',
                'formula': f'{resultado_def}',
                'formula_latex': f'{latex(resultado_def)}',
                'explicacion': 'Resultado de la integral definida.',
                'tipo': 'resultado'
            }]
            
            # Agregar estos pasos a la visualización
            for paso in pasos_definida:
                self.pasos_actuales.append(paso)
            
            # Actualizar visualización
            self.mostrar_pasos_detallados(self.pasos_actuales, None)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en integral definida: {str(e)}")
    
    def graficar_funcion(self):
        """Crear gráfico de la función y su integral"""
        try:
            funcion_str = self.funcion_var.get().strip()
            if not funcion_str:
                messagebox.showwarning("Advertencia", "Ingresa una función para graficar")
                return
            
            # Limpiar frame anterior
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Crear figura con tamaño más compacto
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5))
            fig.patch.set_facecolor('#0d1117')
            fig.subplots_adjust(hspace=0.35, top=0.95, bottom=0.08, left=0.09, right=0.98)
            
            # Parsear función
            x = Symbol('x')
            funcion = parse_expr(funcion_str, transformations='all')
            
            # Crear función numérica
            func_lambdified = lambdify(x, funcion, 'numpy')
            
            # Rango de valores
            x_vals = np.linspace(-5, 5, 1000)
            
            try:
                with np.errstate(all='ignore'):
                    y_vals = func_lambdified(x_vals)
                    y_vals = np.where(np.isfinite(y_vals), y_vals, np.nan)
                
                # Gráfico de la función original
                ax1.plot(x_vals, y_vals, color='#58a6ff', linewidth=2, label=f'f(x) = {funcion}')
                ax1.axhline(0, color='#374151', linewidth=1)
                ax1.axvline(0, color='#374151', linewidth=1)
                ax1.grid(True, alpha=0.3, color='#30363d')
                ax1.set_facecolor('#0d1117')
                ax1.tick_params(colors='#f0f6fc', labelsize=8)
                ax1.set_title('Función Original', color='#f0f6fc', fontsize=10, fontweight='bold')
                ax1.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='#f0f6fc', fontsize=8)
                
                # Intentar graficar la integral (siempre que sea integrable)
                try:
                    integral_result = simplify(integrate(funcion, x))
                    integral_lambdified = lambdify(x, integral_result, 'numpy')
                    with np.errstate(all='ignore'):
                        y_integral = integral_lambdified(x_vals)
                        y_integral = np.where(np.isfinite(y_integral), y_integral, np.nan)
                    
                    ax2.plot(x_vals, y_integral, color='#22c55e', linewidth=2, 
                            label=f'∫f(x)dx = {integral_result}')
                    ax2.axhline(0, color='#374151', linewidth=1)
                    ax2.axvline(0, color='#374151', linewidth=1)
                    ax2.grid(True, alpha=0.3, color='#30363d')
                    ax2.set_facecolor('#0d1117')
                    ax2.tick_params(colors='#f0f6fc', labelsize=8)
                    ax2.set_title('Función Integral', color='#f0f6fc', fontsize=10, fontweight='bold')
                    ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='#f0f6fc', fontsize=8)
                except:
                    ax2.text(0.5, 0.5, 'Integral no graficable', transform=ax2.transAxes,
                            ha='center', va='center', color='#7d8590', fontsize=10)
                    ax2.set_facecolor('#0d1117')
                
            except Exception as e:
                ax1.text(0.5, 0.5, f'Error al graficar:\n{str(e)}', transform=ax1.transAxes,
                        ha='center', va='center', color='#ef4444', fontsize=9)
                ax1.set_facecolor('#0d1117')
            
            # Compactar un poco el layout para dejar espacio a la toolbar
            fig.tight_layout()
            
            # Contenedor para canvas + toolbar
            container = tk.Frame(self.graph_frame, bg='#0d1117')
            container.pack(fill='both', expand=True)

            # Canvas
            canvas = FigureCanvasTkAgg(fig, container)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

            # Toolbar siempre visible
            toolbar_frame = tk.Frame(container, bg='#0d1117')
            toolbar_frame.pack(side='bottom', fill='x')
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            # Mostrar botón de cerrar gráfico
            self.btn_cerrar_grafico.pack(side='right', padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")
    
    def exportar_pdf(self):
        """Exportar solución completa a PDF (pasos + gráficas)."""
        if not hasattr(self, 'pasos_actuales') or not self.pasos_actuales:
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

            with PdfPages(filename) as pdf:
                # Página 1: Gráficas (recrear figura para exportación)
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
                fig.patch.set_facecolor('white')
                fig.subplots_adjust(hspace=0.35, top=0.95, bottom=0.08, left=0.1, right=0.98)

                x = Symbol('x')
                funcion = parse_expr(self.funcion_var.get().strip(), transformations='all')
                func_lamb = lambdify(x, funcion, 'numpy')
                x_vals = np.linspace(-5, 5, 1000)
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

                # Páginas siguientes: Pasos con fórmulas
                def nueva_pagina():
                    fig_steps = plt.figure(figsize=(8.27, 11.69))  # A4
                    fig_steps.patch.set_facecolor('white')
                    ax = fig_steps.add_axes([0.06, 0.04, 0.88, 0.92])
                    ax.axis('off')
                    return fig_steps, ax

                fig_s, ax_s = nueva_pagina()
                y = 0.96
                header = f"Solución Paso a Paso — {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                ax_s.text(0.5, y, header, ha='center', va='top', fontsize=14, weight='bold')
                y -= 0.05
                ax_s.text(0.06, y, f"Función: {self.funcion_var.get()}  |  Tipo: {self.tipo_integral.get()}", fontsize=10)
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
                        txt = f"${formula_ltx}$"
                        ax_s.text(0.08, y, txt, fontsize=11)
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
        self.funcion_var.set("")
        self.variable_var.set("x")
        self.limite_inf_var.set("0")
        self.limite_sup_var.set("1")
        self.tipo_integral.set("indefinida")
        
        # Limpiar pasos
        for w in self.steps_inner.winfo_children():
            w.destroy()
        self._img_cache.clear()
        
        self.integral_preview.config(text="∫ f(x) dx")
        
        # Cerrar gráfico si existe
        self.cerrar_grafico()
        
        self.limites_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedIntegralSolverUI(root)
    root.mainloop()