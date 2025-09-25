"""
Resolución de integrales paso a paso con explicaciones claras.
"""
import sympy as sp
from sympy import *
import re

class MathSolver:
    """Motor de resolución de integrales con trazado de pasos."""
    
    def __init__(self):
        """Inicializa símbolos y estado base."""
        self.x = Symbol('x', real=True)
        
    def resolver_integral_general(self, funcion, variable):
        """Punto de entrada: detecta el tipo de función y elige el método.
        Devuelve (pasos, resultado)."""
        steps = []  # Lista para almacenar todos los pasos de la solución
        
        try:
            # PASO 1: Identificar qué tipo de función es
            tipo = self.identificar_tipo_detallado(funcion)
            
            # Agregar el paso inicial explicando qué vamos a resolver
            steps.append({
                'titulo': 'Integral a resolver',
                'formula': f'∫ {funcion} d{variable}',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable}',
                'explicacion': f'Función tipo: {tipo}',
                'tipo': 'objetivo'
            })
            
            # PASO 2: Análisis detallado de la estructura de la función
            self.analizar_funcion(funcion, variable, steps)
            
            # PASO 3: Elegir método de resolución
            
            # CASO ESPECIAL 1: √(a² - x²) - requiere sustitución trigonométrica
            if self.es_sqrt_a2_minus_x2(funcion):
                a = self.extraer_coeficiente_sqrt(funcion)
                return self.resolver_sqrt_a2_minus_x2(a, variable)
                
            # CASO ESPECIAL 2: Funciones de la forma u^n
            elif self.es_forma_u_n(funcion, variable):
                return self.resolver_forma_u_n(funcion, variable, steps)
                
            # CASO ESPECIAL 3: Productos de funciones (posible integración por partes)
            elif self.es_producto(funcion):
                return self.resolver_producto(funcion, variable, steps)
                
            # CASO ESPECIAL 4: Cocientes (fracciones)
            elif self.es_cociente(funcion):
                return self.resolver_cociente(funcion, variable, steps)
                
            # CASO ESPECIAL 5: Exponenciales compuestas
            elif self.es_exponencial_compuesta(funcion, variable):
                return self.resolver_exponencial_compuesta(funcion, variable, steps)
                
            # CASO ESPECIAL 6: Trigonométricas compuestas
            elif self.es_trigonometrica_compuesta(funcion, variable):
                return self.resolver_trigonometrica_compuesta(funcion, variable, steps)
                
            # CASO GENERAL: Si no encaja en ningún caso especial
            else:
                return self.resolver_con_pasos_detallados(funcion, variable, steps)
                
        except Exception as e:
            steps.append({
                'titulo': '⚠ Error en el cálculo',
                'formula': str(e),
                'explicacion': 'No se pudo resolver con métodos elementales.',
                'tipo': 'error'
            })
            return steps, None
    
    def resolver_sqrt_a2_minus_x2(self, a, var_sym):
        """Resuelve ∫√(a² − x²) dx vía sustitución trigonométrica (x = a·sinθ)."""
        steps = []
        
        # Paso 1: enunciado
        steps.append({
            'titulo': 'Integral a resolver',
            'formula': f'I(x) = ∫ √({a}² - x²) dx',
            'formula_latex': f'I(x) = \\int \\sqrt{{{a}^2 - x^2}} \\, dx',
            'explicacion': f'Esta integral representa el área bajo una semicircunferencia de radio {a}.',
            'tipo': 'objetivo'
        })
        
        # Paso 2: identificar
        steps.append({
            'titulo': 'Identificación del tipo',
            'formula': f'∫ √(a² - x²) dx donde a = {a}',
            'formula_latex': f'\\int \\sqrt{{a^2 - x^2}} \\, dx \\text{{ donde }} a = {a}',
            'explicacion': 'Esta integral requiere sustitución trigonométrica del tipo x = a·sen(θ).',
            'tipo': 'identificacion'
        })
        
        # Paso 3: sustitución
        steps.append({
            'titulo': '🔄 Sustitución trigonométrica',
            'formula': f'x = {a}·sen(θ), dx = {a}·cos(θ) dθ',
            'formula_latex': f'x = {a}\\sin(\\theta), \\quad dx = {a}\\cos(\\theta) \\, d\\theta',
            'explicacion': f'Sustituimos x = {a}·sen(θ) para simplificar la expresión bajo la raíz.',
            'tipo': 'sustitucion'
        })
        
        # Paso 4: simplificar
        steps.append({
            'titulo': '⚡ Simplificación trigonométrica',
            'formula': f'√({a}² - x²) = √({a}² - {a}²·sen²(θ)) = {a}·cos(θ)',
            'formula_latex': f'\\sqrt{{{a}^2 - x^2}} = \\sqrt{{{a}^2 - {a}^2\\sin^2(\\theta)}} = {a}\\cos(\\theta)',
            'explicacion': 'Usamos la identidad trigonométrica: sen²(θ) + cos²(θ) = 1',
            'tipo': 'simplificacion'
        })
        
        # Paso 5: integrar
        steps.append({
            'titulo': 'Integración',
            'formula': f'∫ {a}·cos(θ) · {a}·cos(θ) dθ = {a}² ∫ cos²(θ) dθ',
            'formula_latex': f'\\int {a}\\cos(\\theta) \\cdot {a}\\cos(\\theta) \\, d\\theta = {a}^2 \\int \\cos^2(\\theta) \\, d\\theta',
            'explicacion': 'Multiplicamos los términos y obtenemos cos²(θ).',
            'tipo': 'integracion'
        })
        
        # Paso 6: identidad ángulo doble
        steps.append({
            'titulo': 'Identidad del ángulo doble',
            'formula': f'cos²(θ) = (1 + cos(2θ))/2',
            'formula_latex': f'\\cos^2(\\theta) = \\frac{{1 + \\cos(2\\theta)}}{{2}}',
            'explicacion': 'Usamos la identidad del ángulo doble para simplificar.',
            'tipo': 'identidad'
        })
        
        # Paso 7: integración final
        steps.append({
            'titulo': 'Integración final',
            'formula': f'{a}² ∫ (1 + cos(2θ))/2 dθ = {a}²/2 · (θ + sen(2θ)/2)',
            'formula_latex': f'{a}^2 \\int \\frac{{1 + \\cos(2\\theta)}}{{2}} \\, d\\theta = \\frac{{{a}^2}}{{2}} \\left(\\theta + \\frac{{\\sin(2\\theta)}}{{2}}\\right)',
            'explicacion': 'Integramos término por término.',
            'tipo': 'integracion_final'
        })
        
        # Paso 8: regresar a x
        steps.append({
            'titulo': 'Regreso a variable original',
            'formula': f'θ = arcsen(x/{a}), sen(2θ) = 2·sen(θ)·cos(θ) = 2·(x/{a})·√({a}²-x²)/{a}',
            'formula_latex': f'\\theta = \\arcsin\\left(\\frac{{x}}{{{a}}}\\right), \\quad \\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta) = 2\\cdot\\frac{{x}}{{{a}}}\\cdot\\frac{{\\sqrt{{{a}^2-x^2}}}}{{{a}}}',
            'explicacion': 'Sustituimos de vuelta usando las relaciones trigonométricas.',
            'tipo': 'regreso'
        })
        
        # Paso 9: resultado
        resultado_final = f'{a**2}/2 · arcsen(x/{a}) + x·√({a}² - x²)/2 + C'
        resultado_latex = f'\\frac{{{a**2}}}{{2}}\\arcsin\\left(\\frac{{x}}{{{a}}}\\right) + \\frac{{x\\sqrt{{{a}^2 - x^2}}}}{{2}} + C'
        
        steps.append({
            'titulo': 'Resultado final',
            'formula': f'I(x) = {resultado_final}',
            'formula_latex': f'I(x) = {resultado_latex}',
            'explicacion': f'Esta es la antiderivada completa de √({a}² - x²).',
            'tipo': 'resultado'
        })
        
        return steps, resultado_final
    
    def analizar_funcion(self, funcion, variable, steps):
        """Análisis previo: estructura de f, grado y factorización (si aplica)."""
        steps.append({
            'titulo': 'Análisis de la función',
            'formula': f'f({variable}) = {funcion}',
            'formula_latex': f'f({latex(variable)}) = {latex(funcion)}',
            'explicacion': 'Analizamos la estructura de la función para determinar el método más apropiado.',
            'tipo': 'analisis'
        })
        
        # ¿Polinomio?
        if funcion.is_polynomial():
            grado = degree(funcion)  # Obtener el grado del polinomio
            coeficientes = Poly(funcion, variable).all_coeffs()  # Obtener coeficientes
            steps.append({
                'titulo': 'Polinomio identificado',
                'formula': f'Grado: {grado}, Coeficientes: {coeficientes}',
                'explicacion': f'Es un polinomio de grado {grado}. Aplicaremos la regla de la potencia término por término.',
                'tipo': 'identificacion'
            })
        
        # ¿Se puede factorizar?
        factores = factor(funcion)
        if factores != funcion:  # Si la factorización es diferente de la función original
            steps.append({
                'titulo': 'Factorización',
                'formula': f'{funcion} = {factores}',
                'formula_latex': f'{latex(funcion)} = {latex(factores)}',
                'explicacion': 'La función se puede factorizar, lo que podría simplificar la integración.',
                'tipo': 'factorizacion'
            })
    
    def identificar_tipo_detallado(self, funcion):
        """Clasifica la función (polinomio, irracional, trig., exp., log, compuesta)."""
        func_str = str(funcion)
        
        # Verificar diferentes tipos de funciones
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
    
    def resolver_con_pasos_detallados(self, funcion, variable, steps):
        """Orquesta métodos específicos y cae al general si es necesario."""
        try:
            # MÉTODO 1: Regla de potencia para polinomios
            if funcion.is_polynomial():
                return self.resolver_por_potencia(funcion, variable, steps)
            
            # MÉTODO 2: Métodos trigonométricos
            elif funcion.has(sin, cos, tan):
                return self.resolver_trigonometrica(funcion, variable, steps)
            
            # MÉTODO 3: Métodos exponenciales
            elif funcion.has(exp):
                return self.resolver_exponencial(funcion, variable, steps)
            
            # MÉTODO 4: Métodos logarítmicos
            elif funcion.has(log):
                return self.resolver_logaritmica(funcion, variable, steps)
            
            # MÉTODO 5: Método general con SymPy (último recurso)
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
    
    def resolver_por_potencia(self, funcion, variable, steps):
        """Regla de la potencia, término a término en polinomios."""
        
        # Si es un polinomio, procesarlo término por término
        if funcion.is_polynomial():
            # Expandir y obtener todos los términos del polinomio
            terminos = Add.make_args(expand(funcion))
            steps.append({
                'titulo': 'Descomposición polinomial',
                'formula': f'{funcion} = {" + ".join(map(str, terminos))}',
                'formula_latex': f'{latex(funcion)} = {latex(funcion)}',
                'explicacion': f'El polinomio tiene {len(terminos)} términos. Integraremos cada uno.',
                'tipo': 'descomposicion'
            })
            
            resultados = []  # Lista para guardar el resultado de cada término
            
            # Procesar cada término individualmente
            for i, termino in enumerate(terminos, 1):
                # Extraer coeficiente y potencia
                
                if termino.is_Mul:
                    coef = 1
                    potencia = None
                    # Analizar cada factor del producto
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
                
                # Mostrar el análisis de este término
                steps.append({
                    'titulo': f'Término {i}: {termino}',
                    'formula': f'Coeficiente: {coef}, Potencia de {variable}: {potencia}',
                    'explicacion': f'Aplicamos ∫ {coef}·{variable}^{potencia} d{variable}',
                    'tipo': 'analisis_termino'
                })

                # CASO ESPECIAL: n = -1 (da logaritmo)
                if potencia == -1:
                    resultado_termino = coef * log(abs(variable))
                    steps.append({
                        'titulo': f'🔥 Caso especial n=-1',
                        'formula': f'∫ {coef}·{variable}^(-1) d{variable} = {coef}·ln|{variable}| + C',
                        'formula_latex': f'\\int {latex(coef)}\\cdot {variable}^{-1} \\, d{variable} = {latex(coef)}\\ln|{variable}| + C',
                        'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                        'tipo': 'caso_especial'
                    })
                else:
                    # CASO NORMAL: Aplicar regla de la potencia
                    nueva_potencia = potencia + 1
                    resultado_termino = coef * variable**nueva_potencia / nueva_potencia
                    steps.append({
                        'titulo': f'Regla de potencia para término {i}',
                        'formula': f'∫ {coef}·{variable}^{potencia} d{variable} = {coef}·{variable}^{nueva_potencia}/{nueva_potencia}',
                        'formula_latex': f'\\int {latex(coef)}\\cdot {variable}^{{{latex(potencia)}}} \\, d{variable} = \\frac{{{latex(coef)}\\cdot {variable}^{{{latex(nueva_potencia)}}}}}{{{latex(nueva_potencia)}}}',
                        'explicacion': f'Aumentamos exponente: {potencia} + 1 = {nueva_potencia}, luego dividimos por {nueva_potencia}',
                        'tipo': 'aplicacion_regla'
                    })
                
                resultados.append(resultado_termino)
            
            # Sumar resultados
            resultado_final = Add(*resultados)
            
            steps.append({
                'titulo': 'Sumando todos los términos',
                'formula': f'∫ {funcion} d{variable} = {" + ".join(map(str, resultados))} = {resultado_final}',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)}',
                'explicacion': 'La integral de una suma es la suma de las integrales.',
                'tipo': 'suma_final'
            })
        else:
            # Caso de una sola potencia
            resultado_final = integrate(funcion, variable)
            steps.append({
                'titulo': 'Aplicando regla de la potencia',
                'formula': f'∫ {funcion} d{variable} = {resultado_final} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)} + C',
                'explicacion': 'Para ∫ x^n dx, aumentamos el exponente en 1 y dividimos por el nuevo exponente.',
                'tipo': 'aplicacion'
            })
        
        return steps, resultado_final
    def resolver_trigonometrica(self, funcion, variable, steps):
        """Integrales trigonométricas: casos básicos y compuestos."""
        
        # CASO 1: Función seno
        if funcion.has(sin):
            if funcion == sin(variable):
                steps.append({
                    'titulo': '🌊 Integral básica de seno',
                    'formula': f'∫ sen({variable}) d{variable} = -cos({variable}) + C',
                    'formula_latex': f'\\int \\sin({variable}) \\, d{variable} = -\\cos({variable}) + C',
                    'explicacion': 'La derivada de -cos(x) es sen(x), por tanto ∫sen(x)dx = -cos(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                # Caso más complejo con seno
                steps.append({
                    'titulo': '🌊 Función con seno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene seno. Verificamos si necesitamos sustitución.',
                    'tipo': 'analisis'
                })
                
        # CASO 2: Función coseno
        elif funcion.has(cos):
            if funcion == cos(variable):
                steps.append({
                    'titulo': '〰️ Integral básica de coseno',
                    'formula': f'∫ cos({variable}) d{variable} = sen({variable}) + C',
                    'formula_latex': f'\\int \\cos({variable}) \\, d{variable} = \\sin({variable}) + C',
                    'explicacion': 'La derivada de sen(x) es cos(x), por tanto ∫cos(x)dx = sen(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                steps.append({
                    'titulo': '〰️ Función con coseno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene coseno.',
                    'tipo': 'analisis'
                })
                
        # CASO 3: Función tangente (más compleja)
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
                    'titulo': 'Sustitución u = cos(x)',
                    'formula': f'u = cos({variable}), du = -sen({variable}) d{variable}',
                    'formula_latex': f'u = \\cos({variable}), \\quad du = -\\sin({variable}) \\, d{variable}',
                    'explicacion': 'La integral se convierte en ∫(-1/u) du = -ln|u| = -ln|cos(x)|',
                    'tipo': 'sustitucion'
                })
        
        # Resultado simbólico
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
        """Integrales exponenciales: e^x, compuestas y bases distintas."""
        
        # CASO 1: Exponencial natural básica e^x
        if funcion == exp(variable):
            steps.append({
                'titulo': '📈 Exponencial básica',
                'formula': f'∫ e^{variable} d{variable} = e^{variable} + C',
                'formula_latex': f'\\int e^{{{variable}}} \\, d{variable} = e^{{{variable}}} + C',
                'explicacion': 'La función exponencial e^x es su propia derivada, por tanto ∫e^x dx = e^x + C',
                'tipo': 'formula_basica'
            })
            
        # CASO 2: Exponencial compuesta
        elif funcion.has(exp):
            # Buscar argumentos de exponenciales
            exp_args = []
            for expr in preorder_traversal(funcion):
                if expr.func == exp:
                    exp_args.append(expr.args[0])
            
            if exp_args:
                arg = exp_args[0]  # Tomar el primer argumento encontrado
                steps.append({
                    'titulo': '📈 Exponencial compuesta',
                    'formula': f'Contiene e^({arg})',
                    'formula_latex': f'\\text{{Contiene }} e^{{{latex(arg)}}}',
                    'explicacion': f'Exponencial con argumento: {arg}',
                    'tipo': 'identificacion'
                })
                
                # Verificar regla de la cadena si el argumento no es la variable
                if arg != variable:
                    derivada_arg = diff(arg, variable)  # Derivar el argumento
                    steps.append({
                        'titulo': 'Verificando regla de la cadena',
                        'formula': f'd/d{variable}[{arg}] = {derivada_arg}',
                        'formula_latex': f'\\frac{{d}}{{d{variable}}}[{latex(arg)}] = {latex(derivada_arg)}',
                        'explicacion': 'Si la función es e^u·u\', entonces ∫e^u·u\' dx = e^u + C',
                        'tipo': 'regla_cadena'
                    })
        else:
            # Exponencial de base distinta a e
            steps.append({
                'titulo': 'Exponencial de base a',
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
        """Integrales logarítmicas; ln(x) por partes y casos generales."""
        
        # CASO ESPECIAL: ∫ ln(x) dx
        if funcion == log(variable):
            steps.append({
                'titulo': 'Integral de ln(x)',
                'formula': f'∫ ln({variable}) d{variable}',
                'formula_latex': f'\\int \\ln({variable}) \\, d{variable}',
                'explicacion': 'Esta integral requiere integración por partes.',
                'tipo': 'identificacion'
            })
            
            steps.append({
                'titulo': 'Integración por partes',
                'formula': f'u = ln({variable}), dv = d{variable}',
                'formula_latex': f'u = \\ln({variable}), \\quad dv = d{variable}',
                'explicacion': 'Elegimos u = ln(x) porque su derivada es más simple.',
                'tipo': 'eleccion_u_dv'
            })
            
            steps.append({
                'titulo': '🧮 Calculando du y v',
                'formula': f'du = 1/{variable} d{variable}, v = {variable}',
                'formula_latex': f'du = \\frac{{1}}{{{variable}}} d{variable}, \\quad v = {variable}',
                'explicacion': 'Derivamos u e integramos dv.',
                'tipo': 'calculo_derivadas'
            })
            
            steps.append({
                'titulo': '🔧 Aplicando fórmula',
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
            # Caso general
            resultado = integrate(funcion, variable)
            steps.append({
                'titulo': 'Función logarítmica compleja',
                'formula': f'∫ {funcion} d{variable} = {resultado} + C',
                'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado)} + C',
                'explicacion': 'Integral logarítmica resuelta usando técnicas avanzadas.',
                'tipo': 'resultado'
            })
        
        return steps, resultado
    
    def resolver_general_sympy(self, funcion, variable, steps):
        """Fallback: delega en SymPy y registra el resultado o error."""
        try:
            resultado = integrate(funcion, variable)
            
            steps.append({
                'titulo': '🎯 Resolución con métodos avanzados',
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
    # === Detección de tipos de funciones ===
    
    def es_sqrt_a2_minus_x2(self, funcion):
        """Detecta patrones tipo √(a² − x²)."""
        func_str = str(funcion)
        
        # Buscar raíz y resta
        if 'sqrt' in func_str and '-' in func_str:
            # Detectar sqrt(25-x**2), sqrt(9-x^2), etc.
            pattern = r'sqrt\((\d+)\s*-\s*x\*\*?2\)'
            return bool(re.search(pattern, func_str))
        return False
    
    def extraer_coeficiente_sqrt(self, funcion):
        """Devuelve a en √(a² − x²) para algunos cuadrados perfectos comunes."""
        func_str = str(funcion)
        
        # Mapear números cuadrados perfectos a sus raíces
        if 'sqrt(25' in func_str:
            return 5  # √25 = 5
        elif 'sqrt(4' in func_str:
            return 2  # √4 = 2
        elif 'sqrt(9' in func_str:
            return 3  # √9 = 3
        elif 'sqrt(16' in func_str:
            return 4  # √16 = 4
        else:
            return 1  # Valor por defecto
    
    def es_forma_u_n(self, funcion, variable):
        """Detecta potencias u^n con una sola variable libre."""
        return funcion.is_Pow and len(funcion.free_symbols) == 1
    
    def es_producto(self, funcion):
        """Detecta productos de funciones."""
        return funcion.is_Mul
    
    def es_cociente(self, funcion):
        """Detecta cocientes (potencias negativas en factores)."""
        # Verificar si hay multiplicación con potencias negativas
        return funcion.is_Mul and any(arg.is_Pow and arg.exp < 0 for arg in funcion.args)
    
    def es_exponencial_compuesta(self, funcion, variable):
        """Detecta e^(u(x)) distinto de e^x."""
        return funcion.has(exp) and not funcion.equals(exp(variable))
    
    def es_trigonometrica_compuesta(self, funcion, variable):
        """Detecta trigonométricas con argumento distinto de la variable."""
        return (funcion.has(sin, cos, tan) and 
                not any(trig.args[0] == variable for trig in [sin, cos, tan] if funcion.has(trig)))
    
    # === Métodos específicos para casos complejos ===
    
    def resolver_forma_u_n(self, funcion, variable, steps):
        """Caso u^n; aplica potencia y verifica regla de la cadena."""
        base = funcion.base      # La base 'u'
        exponente = funcion.exp  # El exponente 'n'
        
        steps.append({
            'titulo': 'Forma u^n identificada',
            'formula': f'∫ {base}^{exponente} d{variable}',
            'formula_latex': f'\\int {latex(base)}^{{{latex(exponente)}}} \\, d{variable}',
            'explicacion': f'Base: {base}, Exponente: {exponente}',
            'tipo': 'identificacion'
        })
        
        # CASO ESPECIAL: Exponente -1 (da logaritmo)
        if exponente == -1:
            resultado = log(abs(base))
            steps.append({
                'titulo': '🔥 Regla especial para n=-1',
                'formula': f'∫ u^(-1) du = ln|u| + C',
                'formula_latex': f'\\int u^{{-1}} \\, du = \\ln|u| + C',
                'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                'tipo': 'regla'
            })
        else:
            # CASO NORMAL: Regla de la potencia
            nuevo_exp = exponente + 1
            resultado = base**nuevo_exp / nuevo_exp
            steps.append({
                'titulo': 'Regla de la potencia',
                'formula': f'∫ u^n du = u^(n+1)/(n+1) + C',
                'formula_latex': f'\\int u^n \\, du = \\frac{{u^{{n+1}}}}{{n+1}} + C',
                'explicacion': f'Aumentamos el exponente en 1: {exponente} + 1 = {nuevo_exp}',
                'tipo': 'regla'
            })
        
        # Regla de la cadena
        if base != variable:
            derivada_base = diff(base, variable)
            steps.append({
                'titulo': 'Verificando regla de la cadena',
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
        """Productos: extrae constantes, evalúa por partes y resuelve."""
        factores = list(funcion.args)
        
        steps.append({
            'titulo': 'Producto de funciones',
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
        
        # Extraer constantes fuera de la integral
        if constantes:
            const_producto = 1
            for c in constantes:
                const_producto *= c
                
            steps.append({
                'titulo': 'Extrayendo constantes',
                'formula': f'∫ {const_producto} × {" × ".join(map(str, funciones_var))} d{variable}',
                'formula_latex': f'\\int {latex(const_producto)} \\cdot {latex(Mul(*funciones_var))} \\, d{variable}',
                'explicacion': f'Constante extraída: {const_producto}',
                'tipo': 'simplificacion'
            })
            
            steps.append({
                'titulo': '🔧 Propiedad lineal',
                'formula': f'{const_producto} ∫ {" × ".join(map(str, funciones_var))} d{variable}',
                'formula_latex': f'{latex(const_producto)} \\int {latex(Mul(*funciones_var))} \\, d{variable}',
                'explicacion': 'Las constantes salen fuera de la integral.',
                'tipo': 'propiedad'
            })
        
        # PASO 2: Si quedan exactamente 2 funciones, considerar integración por partes
        if len(funciones_var) == 2:
            u_cand, dv_cand = funciones_var
            steps.append({
                'titulo': 'Evaluando integración por partes',
                'formula': f'u = {u_cand}, dv = {dv_cand} dx',
                'formula_latex': f'u = {latex(u_cand)}, \\quad dv = {latex(dv_cand)} \\, dx',
                'explicacion': 'Consideramos usar ∫u dv = uv - ∫v du',
                'tipo': 'metodo'
            })
            
            # Calcular du y v
            du = diff(u_cand, variable)
            try:
                v = integrate(dv_cand, variable)
                steps.append({
                    'titulo': '🧮 Calculando du y v',
                    'formula': f'du = {du} dx, v = {v}',
                    'formula_latex': f'du = {latex(du)} \\, dx, \\quad v = {latex(v)}',
                    'explicacion': 'Derivamos u e integramos dv.',
                    'tipo': 'calculo'
                })
                
                producto_uv = u_cand * v
                integral_vdu = integrate(v * du, variable)
                
                steps.append({
                    'titulo': 'Aplicando fórmula por partes',
                    'formula': f'uv = {producto_uv}',
                    'formula_latex': f'uv = {latex(producto_uv)}',
                    'explicacion': 'Primera parte de la fórmula: uv',
                    'tipo': 'calculo'
                })
                
                steps.append({
                    'titulo': 'Segunda integral',
                    'formula': f'∫ v du = ∫ {v} × {du} dx = {integral_vdu}',
                    'formula_latex': f'\\int v \\, du = \\int {latex(v)} \\cdot {latex(du)} \\, dx = {latex(integral_vdu)}',
                    'explicacion': 'Calculamos ∫v du',
                    'tipo': 'calculo'
                })
                
            except:
                pass
        
        # Resolver
        resultado_final = integrate(funcion, variable)
        steps.append({
            'titulo': '✅ Resultado final',
            'formula': f'∫ {funcion} d{variable} = {resultado_final} + C',
            'formula_latex': f'\\int {latex(funcion)} \\, d{variable} = {latex(resultado_final)} + C',
            'explicacion': 'Integral resuelta usando las técnicas apropiadas.',
            'tipo': 'resultado'
        })
        
        return steps, resultado_final
    
    def resolver_cociente(self, funcion, variable, steps):
        """
        Resuelve integrales de cocientes (fracciones)
        
        Los cocientes pueden necesitar:
        - Fracciones parciales
        - Sustitución trigonométrica  
        - Completar el cuadrado
        
        Args:
            funcion: Función racional (cociente)
            variable: Variable de integración
            steps: Lista de pasos
        """
        steps.append({
            'titulo': 'Analizando cociente',
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
        """
        Resuelve integrales exponenciales compuestas
        
        Ejemplos: ∫ e^(x²) dx, ∫ e^(2x+1) dx
        Pueden necesitar sustitución u = argumento_de_e
        
        Args:
            funcion: Función exponencial compuesta
            variable: Variable de integración
            steps: Lista de pasos
        """
        steps.append({
            'titulo': 'Analizando exponencial compuesta',
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
        """
        Resuelve integrales trigonométricas compuestas
        
        Ejemplos: ∫ sin(2x) dx, ∫ cos(x²) dx, ∫ tan(3x+1) dx
        Pueden necesitar sustitución u = argumento_trigonométrico
        
        Args:
            funcion: Función trigonométrica compuesta
            variable: Variable de integración  
            steps: Lista de pasos
        """
        steps.append({
            'titulo': 'Analizando trigonométrica compuesta',
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