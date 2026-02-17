from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from sympy import isprime, factorint, gcd, mod_inverse, symbols, solve
import sympy

class MathFoundationsModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Математические основы криптографии"
        self.description = "НОД, диофантовы уравнения, теория чисел и эллиптические кривые"
        self.category = "math"
        self.icon = ""
        self.order = 0  # Базовый модуль, должен быть первым
    
    def render(self):
        st.title("Математические основы криптографии")
        st.subheader("Теория чисел, алгебра и эллиптические кривые")
        
        # Теоретическая справка
        with st.expander("Теоретическая справка", expanded=False):
            st.markdown("""
            ### Математический фундамент криптографии
            
            **Основные разделы:**
            1. **Теория чисел** - простые числа, НОД, модульная арифметика
            2. **Алгебра** - группы, кольца, поля
            3. **Эллиптические кривые** - современная криптография
            
            **Ключевые понятия:**
            - **НОД** - основа алгоритма Евклида, используется в RSA
            - **Диофантовы уравнения** - решение уравнений в целых числах
            - **Простота чисел** - основа безопасности криптосистем
            - **Эллиптические кривые** - ECDSA, современные протоколы
            
            **Применение в криптографии:**
            - RSA: большие простые числа и модульная арифметика
            - Diffie-Hellman: дискретное логарифмирование
            - ECC: эллиптические кривые для эффективного шифрования
            """)
        
        # Выбор раздела
        section = st.radio(
            "Выберите раздел:",
            ["Алгоритм Евклида и НОД", 
             "Линейные диофантовы уравнения", 
             "Теория чисел и простые числа",
             "Эллиптические кривые",
             "Интегральные примеры"],
            horizontal=True
        )
        
        if section == "Алгоритм Евклида и НОД":
            self.render_euclidean_algorithm()
        elif section == "Линейные диофантовы уравнения":
            self.render_diophantine_equations()
        elif section == "Теория чисел и простые числа":
            self.render_number_theory()
        elif section == "Эллиптические кривые":
            self.render_elliptic_curves()
        else:
            self.render_integrated_examples()
    
    def render_euclidean_algorithm(self):
        """Алгоритм Евклида и расширенный алгоритм Евклида"""
        st.markdown("### Алгоритм Евклида и НОД")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод чисел")
            a = st.number_input("Первое число a:", min_value=1, max_value=10**6, value=56)
            b = st.number_input("Второе число b:", min_value=1, max_value=10**6, value=98)
            
            st.markdown("#### Выбор алгоритма")
            algorithm_type = st.radio(
                "Тип алгоритма:",
                ["Обычный алгоритм Евклида", "Расширенный алгоритм Евклида"],
                index=0
            )
        
        with col2:
            st.markdown("#### Результаты вычислений")
            
            if st.button("Вычислить НОД", type="primary"):
                with st.spinner("Вычисляю..."):
                    if algorithm_type == "Обычный алгоритм Евклида":
                        self.calculate_gcd(a, b)
                    else:
                        self.calculate_extended_gcd(a, b)
        
        # Теоретическое объяснение
        st.markdown("---")
        st.markdown("#### Теория алгоритма Евклида")
        
        st.latex(r"gcd(a, b) = gcd(b, a \mod b)")
        st.write("""
        **Алгоритм Евклида** основан на том, что НОД двух чисел не меняется, 
        если большее число заменить его остатком от деления на меньшее.
        
        **Расширенный алгоритм Евклида** также находит коэффициенты Безу:
        """)
        st.latex(r"a \cdot x + b \cdot y = gcd(a, b)")
        st.write("""
        **Применение в криптографии:**
        - Проверка взаимной простоты чисел в RSA
        - Нахождение обратных элементов в модульной арифметике
        - Решение линейных сравнений
        """)
    
    def calculate_gcd(self, a, b):
        """Вычисляет НОД с визуализацией шагов"""
        st.success(f"**Вычисляем НОД({a}, {b})**")
        
        steps = []
        x, y = a, b
        
        while y != 0:
            quotient = x // y
            remainder = x % y
            steps.append({
                'Шаг': len(steps) + 1,
                'a': x,
                'b': y, 
                'Частное': quotient,
                'Остаток': remainder,
                'Формула': f"{x} = {y} × {quotient} + {remainder}"
            })
            x, y = y, remainder
        
        result = x
        st.success(f"**НОД({a}, {b}) = {result}**")
        
        # Показываем шаги
        st.markdown("#### Шаги алгоритма")
        st.dataframe(pd.DataFrame(steps), use_container_width=True, hide_index=True)
        
        # Визуализация
        self.visualize_euclidean_algorithm(steps, a, b, result)
        
        # Дополнительная информация
        if result == 1:
            st.info(f"✅ Числа {a} и {b} взаимно просты")
        else:
            st.info(f"Числа {a} и {b} имеют общий делитель {result}")
    
    def calculate_extended_gcd(self, a, b):
        """Расширенный алгоритм Евклида"""
        st.success(f"**Расширенный алгоритм Евклида для ({a}, {b})**")
        
        # Инициализация
        r_prev, r_curr = a, b
        s_prev, s_curr = 1, 0
        t_prev, t_curr = 0, 1
        
        steps = [{
            'Шаг': 0,
            'r': r_prev,
            's': s_prev,
            't': t_prev,
            'q': '-',
            'Формула': f'Инициализация'
        }]
        
        step = 1
        while r_curr != 0:
            quotient = r_prev // r_curr
            
            # Обновляем значения
            r_next = r_prev - quotient * r_curr
            s_next = s_prev - quotient * s_curr
            t_next = t_prev - quotient * t_curr
            
            steps.append({
                'Шаг': step,
                'r': r_curr,
                's': s_curr,
                't': t_curr,
                'q': quotient,
                'Формула': f"{r_prev} = {r_curr} × {quotient} + {r_next}"
            })
            
            # Сдвигаем значения
            r_prev, r_curr = r_curr, r_next
            s_prev, s_curr = s_curr, s_next
            t_prev, t_curr = t_curr, t_next
            step += 1
        
        gcd_val = r_prev
        x, y = s_prev, t_prev
        
        st.success(f"**Результат:** {a} × ({x}) + {b} × ({y}) = {gcd_val}")
        
        # Проверка
        verification = a * x + b * y
        if verification == gcd_val:
            st.success("Проверка пройдена!")
        else:
            st.error("Ошибка в вычислениях!")
        
        # Показываем шаги
        st.markdown("#### Шаги расширенного алгоритма")
        st.dataframe(pd.DataFrame(steps), use_container_width=True, hide_index=True)
        
        # Применение в криптографии
        st.markdown("---")
        st.markdown("#### Применение в криптографии")
        
        if gcd_val == 1:
            st.info(f"**Обратный элемент:** {a}⁻¹ mod {b} = {x % b}")
            st.info(f"**Проверка:** {a} × {x % b} mod {b} = {(a * (x % b)) % b}")
        else:
            st.warning("Числа не взаимно просты, обратного элемента не существует")
    
    def render_diophantine_equations(self):
        """Решение линейных диофантовых уравнений"""
        st.markdown("### ➗ Линейные диофантовы уравнения")
        
        st.info("""
        **Линейное диофантово уравнение:** ax + by = c  
        **Условие разрешимости:** НОД(a, b) должен делить c
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод уравнения")
            a = st.number_input("Коэффициент a:", value=56, key="dioph_a")
            b = st.number_input("Коэффициент b:", value=98, key="dioph_b") 
            c = st.number_input("Правая часть c:", value=14, key="dioph_c")
            
            if st.button("Решить уравнение", type="primary"):
                with st.spinner("Решаю диофантово уравнение..."):
                    self.solve_diophantine_equation(a, b, c)
        
        with col2:
            st.markdown("#### Теория")
            st.write("""
            **Общий вид решения:**
            """)
            st.latex(r"x = x_0 + \frac{b}{d} \cdot t")
            st.latex(r"y = y_0 - \frac{a}{d} \cdot t")
            st.latex(r"d = gcd(a, b), \quad t \in \mathbb{Z}")
            st.write("""
            **Применение в криптографии:**
            - Решение линейных сравнений
            - Криптоанализ линейных систем
            - Построение линейных комбинаций
            """)
    
    def solve_diophantine_equation(self, a, b, c):
        """Решает линейное диофантово уравнение"""
        st.success(f"**Решаем уравнение:** {a}x + {b}y = {c}")
        
        # Проверяем условие разрешимости
        d = math.gcd(a, b)
        
        if c % d != 0:
            st.error(f"❌ Уравнение не имеет решений! НОД({a}, {b}) = {d} не делит {c}")
            return
        
        st.success(f"✅ Уравнение разрешимо! НОД({a}, {b}) = {d} делит {c}")
        
        # Находим частное решение с помощью расширенного алгоритма Евклида
        if d == 0:
            st.error("Деление на ноль!")
            return
            
        # Упрощаем уравнение
        a1, b1, c1 = a // d, b // d, c // d
        st.info(f"**Упрощенное уравнение:** {a1}x + {b1}y = {c1}")
        
        # Находим решение для упрощенного уравнения
        g, x0, y0 = self.extended_gcd(a1, b1)
        
        # Частное решение исходного уравнения
        x_part = x0 * c1
        y_part = y0 * c1
        
        st.success(f"**Частное решение:** x₀ = {x_part}, y₀ = {y_part}")
        st.info(f"**Проверка:** {a}×{x_part} + {b}×{y_part} = {a*x_part + b*y_part}")
        
        # Общее решение
        st.markdown("#### Общее решение")
        st.latex(f"x = {x_part} + {b1}t")
        st.latex(f"y = {y_part} - {a1}t")
        st.latex(r"t \in \mathbb{Z}")
        
        # Находим несколько конкретных решений
        st.markdown("#### Конкретные решения")
        solutions = []
        for t in range(-3, 4):
            x_sol = x_part + b1 * t
            y_sol = y_part - a1 * t
            solutions.append({
                't': t,
                'x': x_sol,
                'y': y_sol,
                'Проверка': f"{a}×{x_sol} + {b}×{y_sol} = {a*x_sol + b*y_sol}"
            })
        
        st.dataframe(pd.DataFrame(solutions), use_container_width=True, hide_index=True)
        
        # Визуализация решений
        self.visualize_diophantine_solutions(a, b, c, solutions)
    
    def extended_gcd(self, a, b):
        """Расширенный алгоритм Евклида (возвращает НОД и коэффициенты Безу)"""
        if b == 0:
            return a, 1, 0
        
        gcd_val, x1, y1 = self.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        
        return gcd_val, x, y
    
    def render_number_theory(self):
        """Теория чисел: простые числа, факторизация, тесты простоты"""
        st.markdown("### Теория чисел и простые числа")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Анализ числа")
            number = st.number_input("Введите число для анализа:", 
                                   min_value=2, max_value=10**6, value=123456)
            
            analysis_type = st.radio(
                "Тип анализа:",
                ["Проверка простоты", "Факторизация", "Функция Эйлера", "Тесты простоты"],
                horizontal=False
            )
            
            if st.button("Анализировать число", type="primary"):
                with st.spinner("Выполняю анализ..."):
                    if analysis_type == "Проверка простоты":
                        self.check_primality(number)
                    elif analysis_type == "Факторизация":
                        self.factorize_number(number)
                    elif analysis_type == "Функция Эйлера":
                        self.calculate_euler_totient(number)
                    else:
                        self.run_primality_tests(number)
        
        with col2:
            st.markdown("#### Теория простых чисел")
            st.write("""
            **Основные понятия:**
            - **Простое число** - имеет ровно два делителя
            - **Функция Эйлера** φ(n) - количество чисел, взаимно простых с n
            - **Малая теорема Ферма** - основа многих тестов простоты
            
            **Тесты простоты:**
            - **Тривиальное деление** - проверка делителей до √n
            - **Тест Ферма** - вероятностный тест
            - **Тест Миллера-Рабина** - более надежный вероятностный тест
            """)
    
    def check_primality(self, n):
        """Проверяет, является ли число простым"""
        st.success(f"**Анализ числа {n}**")
        
        if isprime(n):
            st.success(f"🎉 {n} - простое число!")
        else:
            st.error(f"❌ {n} - составное число")
        
        # Дополнительная информация
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Количество цифр", len(str(n)))
        
        with col2:
            # Проверка на четность
            if n % 2 == 0:
                parity = "Четное"
            else:
                parity = "Нечетное"
            st.metric("Четность", parity)
        
        with col3:
            # Ближайшие простые числа
            smaller_prime = self.find_previous_prime(n)
            larger_prime = self.find_next_prime(n)
            st.metric("Ближайшие простые", f"{smaller_prime} ← → {larger_prime}")
        
        # Визуализация простых чисел вокруг
        self.visualize_prime_numbers(n)
    
    def factorize_number(self, n):
        """Факторизует число на простые множители"""
        st.success(f"**Факторизация числа {n}**")
        
        factors = factorint(n)
        
        # Показываем факторизацию
        factorization_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
        st.latex(f"{n} = {factorization_str}")
        
        # Таца множителей
        factors_data = []
        for prime, exponent in factors.items():
            factors_data.append({
                'Простой множитель': prime,
                'Степень': exponent,
                'Вклад': prime ** exponent
            })
        
        st.dataframe(pd.DataFrame(factors_data), use_container_width=True, hide_index=True)
        
        # Проверка факторизации
        product = 1
        for prime, exponent in factors.items():
            product *= prime ** exponent
        
        if product == n:
            st.success("✅ Факторизация верна!")
        else:
            st.error("❌ Ошибка в факторизации!")
        
        # Визуализация факторизации
        self.visualize_factorization(n, factors)
    
    def calculate_euler_totient(self, n):
        """Вычисляет функцию Эйлера φ(n)"""
        st.success(f"**Функция Эйлера φ({n})**")
        
        if n == 1:
            phi = 1
        else:
            factors = factorint(n)
            phi = n
            for p in factors:
                phi *= (1 - 1/p)
            phi = int(phi)
        
        st.latex(f"\\phi({n}) = {phi}")
        
        # Объяснение вычисления
        st.markdown("#### Вычисление функции Эйлера")
        
        if n > 1:
            factors = factorint(n)
            formula_parts = []
            for p in factors:
                formula_parts.append(f"\\left(1 - \\frac{{1}}{{{p}}}\\right)")
            
            formula = f"{n} \\times " + " \\times ".join(formula_parts)
            st.latex(f"\\phi({n}) = {formula} = {phi}")
        
        # Числа, взаимно простые с n
        st.markdown("#### Числа, взаимно простые с n")
        coprime_numbers = [i for i in range(1, min(n, 101)) if math.gcd(i, n) == 1]
        
        if len(coprime_numbers) <= 20:
            st.write(f"**Числа от 1 до {min(n, 100)}, взаимно простые с {n}:**")
            st.write(", ".join(map(str, coprime_numbers)))
        else:
            st.write(f"**Первые 20 чисел, взаимно простых с {n}:**")
            st.write(", ".join(map(str, coprime_numbers[:20])))
        
        st.info(f"**Всего чисел, взаимно простых с {n}: {phi}**")
    
    def run_primality_tests(self, n):
        """Запускает различные тесты простоты"""
        st.success(f"**Тесты простоты для числа {n}**")
        
        test_results = []
        
        # 1. Тривиальное деление
        start_time = time.time()
        trivial_result = self.trivial_division_test(n)
        trivial_time = time.time() - start_time
        test_results.append(('Тривиальное деление', trivial_result, trivial_time))
        
        # 2. Тест Ферма
        start_time = time.time()
        fermat_result = self.fermat_test(n, k=5)
        fermat_time = time.time() - start_time
        test_results.append(('Тест Ферма', fermat_result, fermat_time))
        
        # 3. Тест Миллера-Рабина
        start_time = time.time()
        miller_rabin_result = self.miller_rabin_test(n, k=5)
        miller_rabin_time = time.time() - start_time
        test_results.append(('Тест Миллера-Рабина', miller_rabin_result, miller_rabin_time))
        
        # 4. Встроенный тест sympy
        start_time = time.time()
        sympy_result = isprime(n)
        sympy_time = time.time() - start_time
        test_results.append(('SymPy isprime', sympy_result, sympy_time))
        
        # Показываем результаты
        results_df = pd.DataFrame(test_results, 
                                columns=['Тест', 'Результат', 'Время (сек)'])
        results_df['Результат'] = results_df['Результат'].map({True: '✅ Простое', False: '❌ Составное'})
        
        st.dataframe(results_df, use_container_width=True, hide_index=True)
        
        # Анализ результатов
        prime_count = sum(1 for _, result, _ in test_results if result == '✅ Простое')
        total_tests = len(test_results)
        
        if prime_count == total_tests:
            st.success(f"🎉 Все тесты подтверждают, что {n} - простое число!")
        elif prime_count == 0:
            st.error(f"❌ Все тесты подтверждают, что {n} - составное число!")
        else:
            st.warning(f"⚠️ Результаты тестов противоречивы. Вероятностные тесты могут ошибаться.")
    
    def render_elliptic_curves(self):
        """Эллиптические кривые и их применение в криптографии"""
        st.markdown("### Эллиптические кривые")
        
        st.info("""
        **Уравнение эллиптической кривой:** y² = x³ + ax + b  
        **Дискриминант:** Δ = -16(4a³ + 27b²) ≠ 0
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Параметры кривой")
            a = st.number_input("Параметр a:", value=-1, key="ec_a")
            b = st.number_input("Параметр b:", value=1, key="ec_b")
            modulus = st.number_input("Модуль (0 для ℝ):", min_value=0, max_value=1000, value=0)
            
            st.markdown("#### Операции")
            operation = st.radio(
                "Операция:",
                ["Визуализация кривой", "Сложение точек", "Умножение точки на число"],
                horizontal=False
            )
            
            if st.button("Построить кривую", type="primary"):
                with st.spinner("Строю эллиптическую кривую..."):
                    if operation == "Визуализация кривой":
                        self.visualize_elliptic_curve(a, b, modulus)
                    elif operation == "Сложение точек":
                        self.demo_point_addition(a, b, modulus)
                    else:
                        self.demo_point_multiplication(a, b, modulus)
        
        with col2:
            st.markdown("#### Теория эллиптических кривых")
            st.write("""
            **Групповой закон:**
            - **Сложение точек** - геометрическая операция
            - **Нейтральный элемент** - точка на бесконечности
            - **Обратный элемент** - симметричная точка
            
            **Применение в криптографии (ECC):**
            - **ECDH** - обмен ключами
            - **ECDSA** - цифровые подписи
            - **Эффективность** - меньшие ключи при той же безопасности
            """)
            
            st.latex(r"P + Q = R")
            st.latex(r"k \times P = \underbrace{P + P + \cdots + P}_{k\ \text{раз}}")
    
    def visualize_elliptic_curve(self, a, b, modulus=0):
        """Визуализирует эллиптическую кривую"""
        st.success(f"**Эллиптическая кривая:** y² = x³ + {a}x + {b}")
        
        # Проверяем дискриминант
        discriminant = -16 * (4 * a**3 + 27 * b**2)
        if discriminant == 0:
            st.error("❌ Дискриминант равен 0! Это не эллиптическая кривая.")
            return
        else:
            st.info(f"**Дискриминант:** Δ = {discriminant}")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if modulus == 0:  # Действительные числа
            # Строим кривую над ℝ
            x = np.linspace(-3, 3, 1000)
            y_squared = x**3 + a*x + b
            
            # Только где y² >= 0
            valid_indices = y_squared >= 0
            x_valid = x[valid_indices]
            y_squared_valid = y_squared[valid_indices]
            
            y_positive = np.sqrt(y_squared_valid)
            y_negative = -y_positive
            
            ax.plot(x_valid, y_positive, 'b-', linewidth=2, label='y = +√(x³ + ax + b)')
            ax.plot(x_valid, y_negative, 'r-', linewidth=2, label='y = -√(x³ + ax + b)')
            ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f'Эллиптическая кривая: y² = x³ + {a}x + {b}')
            ax.legend()
            ax.set_aspect('equal')
            
        else:  # Конечное поле
            # Строим кривую над конечным полем
            points = []
            for x in range(modulus):
                y_squared = (x**3 + a*x + b) % modulus
                for y in range(modulus):
                    if (y*y) % modulus == y_squared:
                        points.append((x, y))
            
            if points:
                x_vals, y_vals = zip(*points)
                ax.scatter(x_vals, y_vals, color='blue', s=50)
                ax.set_xlim(-0.5, modulus-0.5)
                ax.set_ylim(-0.5, modulus-0.5)
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_title(f'Эллиптическая кривая над F_{modulus}: y² = x³ + {a}x + {b}')
                ax.set_aspect('equal')
                
                st.info(f"**Количество точек на кривой:** {len(points)}")
            else:
                st.warning("На кривой нет точек над выбранным полем")
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Дополнительная информация
        st.markdown("#### Криптографическое применение")
        st.write("""
        **Преимущества ECC:**
        - **Меньшие ключи**: 256-битный ECC ключ ≈ 3072-битный RSA ключ
        - **Высокая производительность**: Быстрые операции
        - **Меньшие накладные расходы**: Эффективно для мобильных устройств
        
        **Стандартные кривые:**
        - **secp256k1** - Bitcoin
        - **P-256** - NSA Suite B
        - **Curve25519** - современные протоколы
        """)
    
    def render_integrated_examples(self):
        """Интегральные примеры применения математики в криптографии"""
        st.markdown("### Интегральные примеры")
        
        example_type = st.selectbox(
            "Выберите пример:",
            [
                "RSA: Генерация ключей",
                "Diffie-Hellman: Математическая основа", 
                "ECDSA: Эллиптические кривые на практике",
                "Криптоанализ: Факторизация в атаках"
            ]
        )
        
        if example_type == "RSA: Генерация ключей":
            self.demo_rsa_math()
        elif example_type == "Diffie-Hellman: Математическая основа":
            self.demo_dh_math()
        elif example_type == "ECDSA: Эллиптические кривые на практике":
            self.demo_ecdsa_math()
        else:
            self.demo_factorization_attack()
    
    def demo_rsa_math(self):
        """Демонстрация математики RSA"""
        st.markdown("#### Математика RSA")
        
        st.info("""
        **Этапы RSA:**
        1. Выбираем простые p и q
        2. Вычисляем n = p × q
        3. Вычисляем φ(n) = (p-1)(q-1)  
        4. Выбираем e, взаимно простое с φ(n)
        5. Вычисляем d = e⁻¹ mod φ(n)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            p = st.number_input("Простое p:", min_value=2, max_value=1000, value=61)
            q = st.number_input("Простое q:", min_value=2, max_value=1000, value=53)
            e = st.number_input("Публичная экспонента e:", min_value=3, max_value=1000, value=17)
            
            if st.button("Показать математику RSA", type="primary"):
                # Проверяем простоту
                if not (isprime(p) and isprime(q)):
                    st.error("p и q должны быть простыми!")
                    return
                
                if p == q:
                    st.error("p и q должны быть разными!")
                    return
                
                # Вычисления
                n = p * q
                phi_n = (p - 1) * (q - 1)
                
                # Проверяем e
                if math.gcd(e, phi_n) != 1:
                    st.error(f"e и φ(n) должны быть взаимно простыми! НОД({e}, {phi_n}) = {math.gcd(e, phi_n)}")
                    return
                
                # Вычисляем d
                d = mod_inverse(e, phi_n)
                
                st.success("**Параметры RSA:**")
                st.latex(f"n = {p} \\times {q} = {n}")
                st.latex(f"\\phi(n) = ({p}-1)({q}-1) = {phi_n}")
                st.latex(f"e = {e}")
                st.latex(f"d = {e}^{{-1}} \\mod {phi_n} = {d}")
                
                # Проверка
                st.success("**Проверка:**")
                st.latex(f"e \\times d \\mod \\phi(n) = {e} \\times {d} \\mod {phi_n} = {(e * d) % phi_n}")
    
    # Вспомогательные методы
    
    def find_previous_prime(self, n):
        """Находит предыдущее простое число"""
        for i in range(n-1, 1, -1):
            if isprime(i):
                return i
        return 2
    
    def find_next_prime(self, n):
        """Находит следующее простое число"""
        i = n + 1
        while True:
            if isprime(i):
                return i
            i += 1
    
    def trivial_division_test(self, n):
        """Тест простоты тривиальным делением"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def fermat_test(self, n, k=5):
        """Тест простоты Ферма"""
        if n <= 1:
            return False
        if n <= 3:
            return True
        
        for _ in range(k):
            a = random.randint(2, n-2)
            if pow(a, n-1, n) != 1:
                return False
        return True
    
    def miller_rabin_test(self, n, k=5):
        """Тест простоты Миллера-Рабина"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Записываем n-1 как d×2^s
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        
        for _ in range(k):
            a = random.randint(2, n-2)
            x = pow(a, d, n)
            if x == 1 or x == n-1:
                continue
            
            for _ in range(s-1):
                x = pow(x, 2, n)
                if x == n-1:
                    break
            else:
                return False
        
        return True
    
    # Методы визуализации
    
    def visualize_euclidean_algorithm(self, steps, a, b, result):
        """Визуализирует алгоритм Евклида"""
        st.markdown("#### Визуализация алгоритма")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Подготавливаем данные для графика
        step_numbers = [step['Шаг'] for step in steps]
        a_values = [step['a'] for step in steps]
        b_values = [step['b'] for step in steps]
        
        ax.plot(step_numbers, a_values, 'bo-', label='a', linewidth=2, markersize=6)
        ax.plot(step_numbers, b_values, 'ro-', label='b', linewidth=2, markersize=6)
        ax.axhline(y=result, color='green', linestyle='--', label=f'НОД = {result}')
        
        ax.set_xlabel('Шаг алгоритма')
        ax.set_ylabel('Значение')
        ax.set_title('Визуализация алгоритма Евклида')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_diophantine_solutions(self, a, b, c, solutions):
        """Визуализирует решения диофантова уравнения"""
        if len(solutions) < 2:
            return
        
        st.markdown("#### Визуализация решений")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x_vals = [sol['x'] for sol in solutions]
        y_vals = [sol['y'] for sol in solutions]
        
        ax.plot(x_vals, y_vals, 'bo-', linewidth=2, markersize=6)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Решения уравнения {a}x + {b}y = {c}')
        ax.grid(True, alpha=0.3)
        
        # Добавляем уравнение прямой
        if b != 0:
            x_line = np.array([min(x_vals), max(x_vals)])
            y_line = (c - a * x_line) / b
            ax.plot(x_line, y_line, 'r--', alpha=0.5, label='Уравнение')
            ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_prime_numbers(self, n):
        """Визуализирует простые числа вокруг заданного числа"""
        st.markdown("#### Простые числа вокруг")
        
        # Находим простые числа в окрестности
        start = max(2, n - 20)
        end = n + 20
        
        primes = [i for i in range(start, end + 1) if isprime(i)]
        numbers = list(range(start, end + 1))
        
        fig, ax = plt.subplots(figsize=(12, 3))
        
        for num in numbers:
            if num == n:
                color = 'red'
                marker = 'o'
                size = 100
            elif isprime(num):
                color = 'green'
                marker = 's'
                size = 60
            else:
                color = 'lightgray'
                marker = 'o'
                size = 40
            
            ax.scatter(num, 0, c=color, marker=marker, s=size)
            ax.text(num, 0.1, str(num), ha='center', va='bottom', fontsize=8)
        
        ax.set_xlim(start - 0.5, end + 0.5)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_title('Простые числа (зеленые) и заданное число (красное)')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_factorization(self, n, factors):
        """Визуализирует факторизацию числа"""
        st.markdown("#### Визуализация факторизации")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        primes = list(factors.keys())
        exponents = list(factors.values())
        
        # Столбчатая диаграмма
        bars = ax.bar(range(len(primes)), exponents, color='skyblue', alpha=0.7)
        ax.set_xlabel('Простые множители')
        ax.set_ylabel('Степень')
        ax.set_title(f'Факторизация числа {n}')
        ax.set_xticks(range(len(primes)))
        ax.set_xticklabels(primes)
        
        for i, (prime, exp) in enumerate(factors.items()):
            ax.text(i, exp, f'{prime}^{exp}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)

# Необходимый импорт
import time

# Добавляем методы для демонстраций эллиптических кривых
def demo_point_addition(self, a, b, modulus):
    """Демонстрация сложения точек на эллиптической кривой"""
    st.info("Демонстрация сложения точек будет в следующей версии")

def demo_point_multiplication(self, a, b, modulus):
    """Демонстрация умножения точки на число"""
    st.info("Демонстрация умножения точек будет в следующей версии")

def demo_dh_math(self):
    """Демонстрация математики Diffie-Hellman"""
    st.info("Демонстрация Diffie-Hellman будет в следующей версии")

def demo_ecdsa_math(self):
    """Демонстрация математики ECDSA"""
    st.info("Демонстрация ECDSA будет в следующей версии")

def demo_factorization_attack(self):
    """Демонстрация атаки факторизацией"""
    st.info("Демонстрация атаки факторизацией будет в следующей версии")

# Добавляем недостающие методы к классу
MathFoundationsModule.demo_point_addition = demo_point_addition
MathFoundationsModule.demo_point_multiplication = demo_point_multiplication
MathFoundationsModule.demo_dh_math = demo_dh_math
MathFoundationsModule.demo_ecdsa_math = demo_ecdsa_math
MathFoundationsModule.demo_factorization_attack = demo_factorization_attack