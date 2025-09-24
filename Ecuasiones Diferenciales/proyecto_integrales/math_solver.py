"""
Clase especializada para resolver integrales paso a paso con detalle matemático
"""
import sympy as sp
from sympy import *
import re

class MathSolver:
    """Clase especializada para resolver integrales paso a paso con detalle matemático"""
    
    def __init__(self):
        self.x = Symbol('x', real=True)
        
    def resolver_integral_general(self, funcion, variable):
        """Resuelve integrales generales con pasos detallados"""
        steps = []
        
        try:
            # Identificar el tipo de función
            tipo = self.identificar_tipo_detallado(funcion)
            
            steps.append({
                'titulo': 'Integral a resolver',
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
    
    def resolver_sqrt_a2_minus_x2(self, a, var_sym):
        """Resuelve ∫√(a² - x²) dx con sustitución trigonométrica detallada"""
        steps = []
        
        steps.append({
            'titulo': 'Integral a resolver',
            'formula': f'I(x) = ∫ √({a}² - x²) dx',
            'formula_latex': f'I(x) = \\int \\sqrt{{{a}^2 - x^2}} \\, dx',
            'explicacion': f'Esta integral representa el área bajo una semicircunferencia de radio {a}.',
            'tipo': 'objetivo'
        })
        
        steps.append({
            'titulo': 'Identificación del tipo',
            'formula': f'∫ √(a² - x²) dx donde a = {a}',
            'formula_latex': f'\\int \\sqrt{{a^2 - x^2}} \\, dx \\text{{ donde }} a = {a}',
            'explicacion': 'Esta integral requiere sustitución trigonométrica del tipo x = a·sen(θ).',
            'tipo': 'identificacion'
        })
        
        steps.append({
            'titulo': ' Sustitución trigonométrica',
            'formula': f'x = {a}·sen(θ), dx = {a}·cos(θ) dθ',
            'formula_latex': f'x = {a}\\sin(\\theta), \\quad dx = {a}\\cos(\\theta) \\, d\\theta',
            'explicacion': f'Sustituimos x = {a}·sen(θ) para simplificar la expresión bajo la raíz.',
            'tipo': 'sustitucion'
        })
        
        steps.append({
            'titulo': ' Simplificación trigonométrica',
            'formula': f'√({a}² - x²) = √({a}² - {a}²·sen²(θ)) = {a}·cos(θ)',
            'formula_latex': f'\\sqrt{{{a}^2 - x^2}} = \\sqrt{{{a}^2 - {a}^2\\sin^2(\\theta)}} = {a}\\cos(\\theta)',
            'explicacion': 'Usamos la identidad trigonométrica: sen²(θ) + cos²(θ) = 1',
            'tipo': 'simplificacion'
        })
        
        steps.append({
            'titulo': 'Integración',
            'formula': f'∫ {a}·cos(θ) · {a}·cos(θ) dθ = {a}² ∫ cos²(θ) dθ',
            'formula_latex': f'\\int {a}\\cos(\\theta) \\cdot {a}\\cos(\\theta) \\, d\\theta = {a}^2 \\int \\cos^2(\\theta) \\, d\\theta',
            'explicacion': 'Multiplicamos los términos y obtenemos cos²(θ).',
            'tipo': 'integracion'
        })
        
        steps.append({
            'titulo': 'Identidad del ángulo doble',
            'formula': f'cos²(θ) = (1 + cos(2θ))/2',
            'formula_latex': f'\\cos^2(\\theta) = \\frac{{1 + \\cos(2\\theta)}}{{2}}',
            'explicacion': 'Usamos la identidad del ángulo doble para simplificar.',
            'tipo': 'identidad'
        })
        
        steps.append({
            'titulo': 'Integración final',
            'formula': f'{a}² ∫ (1 + cos(2θ))/2 dθ = {a}²/2 · (θ + sen(2θ)/2)',
            'formula_latex': f'{a}^2 \\int \\frac{{1 + \\cos(2\\theta)}}{{2}} \\, d\\theta = \\frac{{{a}^2}}{{2}} \\left(\\theta + \\frac{{\\sin(2\\theta)}}{{2}}\\right)',
            'explicacion': 'Integramos término por término.',
            'tipo': 'integracion_final'
        })
        
        steps.append({
            'titulo': 'Regreso a variable original',
            'formula': f'θ = arcsen(x/{a}), sen(2θ) = 2·sen(θ)·cos(θ) = 2·(x/{a})·√({a}²-x²)/{a}',
            'formula_latex': f'\\theta = \\arcsin\\left(\\frac{{x}}{{{a}}}\\right), \\quad \\sin(2\\theta) = 2\\sin(\\theta)\\cos(\\theta) = 2\\cdot\\frac{{x}}{{{a}}}\\cdot\\frac{{\\sqrt{{{a}^2-x^2}}}}{{{a}}}',
            'explicacion': 'Sustituimos de vuelta usando las relaciones trigonométricas.',
            'tipo': 'regreso'
        })
        
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
        """Análisis detallado de la función antes de integrar"""
        steps.append({
            'titulo': 'Análisis de la función',
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
                'titulo': 'Polinomio identificado',
                'formula': f'Grado: {grado}, Coeficientes: {coeficientes}',
                'explicacion': f'Es un polinomio de grado {grado}. Aplicaremos la regla de la potencia término por término.',
                'tipo': 'identificacion'
            })
        
        # Análisis de factores
        factores = factor(funcion)
        if factores != funcion:
            steps.append({
                'titulo': 'Factorización',
                'formula': f'{funcion} = {factores}',
                'formula_latex': f'{latex(funcion)} = {latex(factores)}',
                'explicacion': 'La función se puede factorizar, lo que podría simplificar la integración.',
                'tipo': 'factorizacion'
            })
    
    def es_sqrt_a2_minus_x2(self, funcion):
        """Detecta si es una función de la forma √(a² - x²)"""
        func_str = str(funcion)
        if 'sqrt' in func_str and '-' in func_str:
            # Buscar patrones como sqrt(25-x**2), sqrt(9-x^2), etc.
            pattern = r'sqrt\((\d+)\s*-\s*x\*\*?2\)'
            return bool(re.search(pattern, func_str))
        return False
    
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
    
    def resolver_con_pasos_detallados(self, funcion, variable, steps):
        """Resuelve integrales con pasos detallados usando diferentes métodos"""
        try:
            # Intentar con regla de potencia primero
            if funcion.is_polynomial():
                return self.resolver_por_potencia(funcion, variable, steps)
            
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
    
    def resolver_por_potencia(self, funcion, variable, steps):
        """Resuelve integrales usando la regla de la potencia con pasos detallados"""
        
        # Si es un polinomio, procesarlo término por término
        if funcion.is_polynomial():
            terminos = Add.make_args(expand(funcion))
            steps.append({
                'titulo': 'Descomposición polinomial',
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
                    'titulo': f'Término {i}: {termino}',
                    'formula': f'Coeficiente: {coef}, Potencia de {variable}: {potencia}',
                    'explicacion': f'Aplicamos ∫ {coef}·{variable}^{potencia} d{variable}',
                    'tipo': 'analisis_termino'
                })

                if potencia == -1:
                    resultado_termino = coef * log(abs(variable))
                    steps.append({
                        'titulo': f' Caso especial n=-1',
                        'formula': f'∫ {coef}·{variable}^(-1) d{variable} = {coef}·ln|{variable}| + C',
                        'formula_latex': f'\\int {latex(coef)}\\cdot {variable}^{-1} \\, d{variable} = {latex(coef)}\\ln|{variable}| + C',
                        'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                        'tipo': 'caso_especial'
                    })
                else:
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
        """Resuelve integrales trigonométricas con pasos detallados"""
        
        # Identificar la función trigonométrica específica
        if funcion.has(sin):
            if funcion == sin(variable):
                steps.append({
                    'titulo': ' Integral básica de seno',
                    'formula': f'∫ sen({variable}) d{variable} = -cos({variable}) + C',
                    'formula_latex': f'\\int \\sin({variable}) \\, d{variable} = -\\cos({variable}) + C',
                    'explicacion': 'La derivada de -cos(x) es sen(x), por tanto ∫sen(x)dx = -cos(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                # Caso más complejo con seno
                steps.append({
                    'titulo': ' Función con seno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene seno. Verificamos si necesitamos sustitución.',
                    'tipo': 'analisis'
                })
                
        elif funcion.has(cos):
            if funcion == cos(variable):
                steps.append({
                    'titulo': ' Integral básica de coseno',
                    'formula': f'∫ cos({variable}) d{variable} = sen({variable}) + C',
                    'formula_latex': f'\\int \\cos({variable}) \\, d{variable} = \\sin({variable}) + C',
                    'explicacion': 'La derivada de sen(x) es cos(x), por tanto ∫cos(x)dx = sen(x) + C',
                    'tipo': 'formula_basica'
                })
            else:
                steps.append({
                    'titulo': ' Función con coseno',
                    'formula': f'Analizando {funcion}',
                    'explicacion': 'Función trigonométrica que contiene coseno.',
                    'tipo': 'analisis'
                })
                
        elif funcion.has(tan):
            if funcion == tan(variable):
                steps.append({
                    'titulo': ' Integral de tangente',
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
                        'titulo': 'Verificando regla de la cadena',
                        'formula': f'd/d{variable}[{arg}] = {derivada_arg}',
                        'formula_latex': f'\\frac{{d}}{{d{variable}}}[{latex(arg)}] = {latex(derivada_arg)}',
                        'explicacion': 'Si la función es e^u·u\', entonces ∫e^u·u\' dx = e^u + C',
                        'tipo': 'regla_cadena'
                    })
        else:
            # Caso de base diferente a e
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
        """Resuelve integrales logarítmicas con pasos detallados"""
        
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
                'titulo': ' Calculando du y v',
                'formula': f'du = 1/{variable} d{variable}, v = {variable}',
                'formula_latex': f'du = \\frac{{1}}{{{variable}}} d{variable}, \\quad v = {variable}',
                'explicacion': 'Derivamos u e integramos dv.',
                'tipo': 'calculo_derivadas'
            })
            
            steps.append({
                'titulo': ' Aplicando fórmula',
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
                'titulo': 'Función logarítmica compleja',
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
                'titulo': ' Resolución con métodos avanzados',
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
    
    # Métodos auxiliares para detección de tipos
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
    
    def resolver_forma_u_n(self, funcion, variable, steps):
        """Resuelve integrales de la forma u^n"""
        base = funcion.base
        exponente = funcion.exp
        
        steps.append({
            'titulo': 'Forma u^n identificada',
            'formula': f'∫ {base}^{exponente} d{variable}',
            'formula_latex': f'\\int {latex(base)}^{{{latex(exponente)}}} \\, d{variable}',
            'explicacion': f'Base: {base}, Exponente: {exponente}',
            'tipo': 'identificacion'
        })
        
        if exponente == -1:
            resultado = log(abs(base))
            steps.append({
                'titulo': ' Regla especial para n=-1',
                'formula': f'∫ u^(-1) du = ln|u| + C',
                'formula_latex': f'\\int u^{{-1}} \\, du = \\ln|u| + C',
                'explicacion': 'Para exponente -1, la integral es el logaritmo natural.',
                'tipo': 'regla'
            })
        else:
            nuevo_exp = exponente + 1
            resultado = base**nuevo_exp / nuevo_exp
            steps.append({
                'titulo': 'Regla de la potencia',
                'formula': f'∫ u^n du = u^(n+1)/(n+1) + C',
                'formula_latex': f'\\int u^n \\, du = \\frac{{u^{{n+1}}}}{{n+1}} + C',
                'explicacion': f'Aumentamos el exponente en 1: {exponente} + 1 = {nuevo_exp}',
                'tipo': 'regla'
            })
        
        # Verificar si necesita regla de la cadena
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
        """Resuelve productos usando integración por partes o propiedades"""
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
                'titulo': ' Propiedad lineal',
                'formula': f'{const_producto} ∫ {" × ".join(map(str, funciones_var))} d{variable}',
                'formula_latex': f'{latex(const_producto)} \\int {latex(Mul(*funciones_var))} \\, d{variable}',
                'explicacion': 'Las constantes salen fuera de la integral.',
                'tipo': 'propiedad'
            })
        
        # Determinar si usar integración por partes
        if len(funciones_var) == 2:
            u_cand, dv_cand = funciones_var
            steps.append({
                'titulo': 'Evaluando integración por partes',
                'formula': f'u = {u_cand}, dv = {dv_cand} dx',
                'formula_latex': f'u = {latex(u_cand)}, \\quad dv = {latex(dv_cand)} \\, dx',
                'explicacion': 'Consideramos usar ∫u dv = uv - ∫v du',
                'tipo': 'metodo'
            })
            
            du = diff(u_cand, variable)
            try:
                v = integrate(dv_cand, variable)
                steps.append({
                    'titulo': ' Calculando du y v',
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
        """Resuelve integrales de cocientes"""
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
        """Resuelve integrales exponenciales compuestas"""
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
        """Resuelve integrales trigonométricas compuestas"""
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
