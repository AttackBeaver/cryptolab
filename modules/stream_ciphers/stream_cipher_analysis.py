from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from collections import Counter
import random
import math

class StreamCipherAnalysisModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Криптоанализ поточных шифров"
        self.description = "Методы атак и тестирование псевдослучайных последовательностей"
        self.category = "stream"
        self.icon = ""
        self.order = 3
    
    def render(self):
        st.title("🔍 Криптоанализ поточных шифров")
        st.subheader("Атаки на поточные шифры и тестирование ПСП")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Методы криптоанализа поточных шифров
            
            **Основные типы атак:**
            1. **Атака по известному открытому тексту** - знаем и открытый, и зашифрованный текст
            2. **Корреляционные атаки** - поиск статистических зависимостей
            3. **Атаки на слабые ключи** - поиск уязвимостей в процедуре инициализации
            4. **Атаки на основе временных характеристик** - анализ времени выполнения
            
            **Тесты случайности (NIST):**
            - **Frequency Test** - проверка равномерности распределения бит
            - **Runs Test** - проверка последовательностей одинаковых бит
            - **Autocorrelation Test** - проверка независимости бит
            - **Linear Complexity Test** - оценка линейной сложности
            
            **Уязвимости поточных шифров:**
            - Повторное использование ключевого потока
            - Слабые начальные значения (IV)
            - Предсказуемость ГПСЧ
            - Статистические аномалии
            """)
        
        # Выбор режима анализа
        analysis_mode = st.radio(
            "Режим анализа:",
            ["🎯 Атака на LFSR", "📊 Тесты случайности NIST", "🔓 Атака на RC4", "📈 Корреляционный анализ"],
            horizontal=True
        )
        
        if analysis_mode == "🎯 Атака на LFSR":
            self.render_lfsr_attack()
        elif analysis_mode == "📊 Тесты случайности NIST":
            self.render_nist_tests()
        elif analysis_mode == "🔓 Атака на RC4":
            self.render_rc4_attack()
        else:
            self.render_correlation_analysis()
    
    def render_lfsr_attack(self):
        """Атака Берлекэмпа-Масси на LFSR"""
        st.markdown("### 🎯 Атака Берлекэмпа-Масси на LFSR")
        
        st.info("""
        **Атака Берлекэмпа-Масси** позволяет восстановить полином обратной связи LFSR 
        по известному отрезку выходной последовательности.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод последовательности LFSR")
            
            sequence_input = st.text_area(
                "Битовая последовательность LFSR:",
                "1101011001111100010011101011001",
                height=100,
                help="Введите битовую последовательность (только 0 и 1)"
            )
            
            # Очищаем последовательность
            sequence = [int(bit) for bit in sequence_input if bit in '01']
            
            if sequence:
                st.success(f"Загружено {len(sequence)} бит")
                
                # Показываем статистику последовательности
                ones_count = sum(sequence)
                zeros_count = len(sequence) - ones_count
                st.write(f"Единицы: {ones_count}, Нули: {zeros_count}")
            
            max_degree = st.slider("Максимальная степень полинома:", 2, 20, 10)
        
        with col2:
            st.markdown("#### Анализ LFSR")
            
            if st.button("🎯 Начать атаку Берлекэмпа-Масси", type="primary"):
                if len(sequence) < 10:
                    st.error("Нужна последовательность длиной хотя бы 10 бит!")
                    return
                
                with st.spinner("Выполняю атаку Берлекэмпа-Масси..."):
                    polynomial, complexity = self.berlekamp_massey_attack(sequence, max_degree)
                    
                    if polynomial:
                        st.success("✅ Полином обратной связи найден!")
                        st.latex(f"C(x) = {self.format_polynomial(polynomial)}")
                        st.info(f"**Линейная сложность:** {complexity}")
                        
                        # Проверяем правильность
                        verification = self.verify_lfsr_polynomial(sequence, polynomial)
                        if verification:
                            st.success("✅ Полином корректно генерирует последовательность")
                        else:
                            st.warning("⚠️ Полином может быть не оптимальным")
                        
                        # Визуализация LFSR
                        self.visualize_lfsr_structure(polynomial)
                    else:
                        st.error("❌ Не удалось найти полином для данной последовательности")
            
            # Генератор тестовой LFSR последовательности
            st.markdown("---")
            st.markdown("#### Сгенерировать тестовую LFSR последовательность")
            
            test_poly = st.text_input("Полином (например, [1,0,1] для x² + 1):", "[1,0,0,1]")
            test_length = st.slider("Длина последовательности:", 10, 100, 30)
            
            if st.button("🎲 Сгенерировать тестовую последовательность"):
                try:
                    poly = eval(test_poly)
                    if isinstance(poly, list) and all(bit in [0,1] for bit in poly):
                        test_seq = self.generate_lfsr_sequence(poly, test_length)
                        sequence_str = ''.join(map(str, test_seq))
                        st.text_area("Сгенерированная последовательность:", sequence_str, height=100)
                    else:
                        st.error("Полином должен быть списком из 0 и 1")
                except:
                    st.error("Неверный формат полинома")
    
    def render_nist_tests(self):
        """Тесты случайности NIST"""
        st.markdown("### 📊 Тесты случайности NIST")
        
        st.info("""
        **NIST Statistical Test Suite** - набор тестов для проверки случайности 
        псевдослучайных последовательностей.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод последовательности для тестирования")
            
            sequence_type = st.radio(
                "Тип последовательности:",
                ["Битовая последовательность", "Числовая последовательность"],
                horizontal=True
            )
            
            if sequence_type == "Битовая последовательность":
                bit_sequence = st.text_area(
                    "Битовая последовательность:",
                    "11001010011010110100101001101011010010100110101101001010",
                    height=150,
                    help="Введите последовательность бит (0 и 1)"
                )
                sequence = [int(bit) for bit in bit_sequence if bit in '01']
            else:
                num_sequence = st.text_area(
                    "Числовая последовательность:",
                    " ".join(str(random.randint(0, 1)) for _ in range(100)),
                    height=150,
                    help="Введите числа через пробел"
                )
                sequence = [int(x) % 2 for x in num_sequence.split() if x.isdigit()]
            
            if sequence:
                st.success(f"Загружено {len(sequence)} бит")
            
            selected_tests = st.multiselect(
                "Выберите тесты для выполнения:",
                [
                    "Frequency Test", 
                    "Runs Test", 
                    "Autocorrelation Test",
                    "Linear Complexity Test",
                    "Entropy Test"
                ],
                default=["Frequency Test", "Runs Test"]
            )
        
        with col2:
            st.markdown("#### Результаты тестирования")
            
            if st.button("🧪 Выполнить тесты NIST", type="primary"):
                if len(sequence) < 100:
                    st.warning("⚠️ Для надежных результатов рекомендуется последовательность длиной >1000 бит")
                
                with st.spinner("Выполняю статистические тесты..."):
                    results = self.perform_nist_tests(sequence, selected_tests)
                    
                    # Показываем результаты
                    st.markdown("##### 📋 Результаты тестов")
                    
                    test_results = []
                    for test_name, (result, p_value, details) in results.items():
                        status = "✅ Прошел" if result else "❌ Не прошел"
                        test_results.append({
                            'Тест': test_name,
                            'Результат': status,
                            'P-value': f"{p_value:.6f}",
                            'Детали': details
                        })
                    
                    st.dataframe(pd.DataFrame(test_results), use_container_width=True)
                    
                    # Общая оценка
                    passed_tests = sum(1 for _, (result, _, _) in results.items() if result)
                    total_tests = len(results)
                    
                    st.metric("Процент пройденных тестов", f"{(passed_tests/total_tests)*100:.1f}%")
                    
                    if passed_tests / total_tests > 0.8:
                        st.success("🎉 Последовательность выглядит случайной!")
                    else:
                        st.warning("⚠️ Последовательность демонстрирует неслучайные свойства")
                    
                    # Визуализация тестов
                    self.visualize_nist_results(sequence, results)
    
    def render_rc4_attack(self):
        """Атаки на шифр RC4"""
        st.markdown("### 🔓 Атаки на шифр RC4")
        
        st.warning("""
        **RC4** широко использовался в WEP, SSL/TLS, но имеет несколько серьезных уязвимостей.
        """)
        
        attack_type = st.selectbox(
            "Выберите тип атаки:",
            [
                "Смещенные выходы (Biased Outputs)",
                "Атака FMS (Fluhrer-Mantin-Shamir)", 
                "Атака по повторному использованию ключа"
            ]
        )
        
        if attack_type == "Смещенные выходы (Biased Outputs)":
            self.render_rc4_biased_outputs()
        elif attack_type == "Атака FMS (Fluhrer-Mantin-Shamir)":
            self.render_rc4_fms_attack()
        else:
            self.render_rc4_key_reuse()
    
    def render_rc4_biased_outputs(self):
        """Демонстрация смещенных выходов RC4"""
        st.markdown("#### Смещенные выходы RC4")
        
        st.info("""
        Второй байт ключевого потока RC4 имеет смещение в сторону нуля с вероятностью 2/256 вместо 1/256.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_keys = st.slider("Количество тестовых ключей:", 100, 10000, 1000)
            key_length = st.slider("Длина ключа (байт):", 5, 32, 16)
            
            if st.button("🔍 Анализировать смещение RC4", type="primary"):
                with st.spinner("Генерирую ключевые потоки RC4..."):
                    # Анализ второго байта
                    second_bytes = []
                    zero_count = 0
                    
                    for _ in range(num_keys):
                        # Генерируем случайный ключ
                        key = [random.randint(0, 255) for _ in range(key_length)]
                        
                        # Генерируем ключевой поток RC4 (упрощенная версия)
                        key_stream = self.simplified_rc4(key, 10)  # Первые 10 байт
                        if len(key_stream) > 1:
                            second_bytes.append(key_stream[1])
                            if key_stream[1] == 0:
                                zero_count += 1
                    
                    # Статистика
                    expected_zero = num_keys / 256
                    actual_zero = zero_count
                    bias = (actual_zero - expected_zero) / num_keys
                    
                    st.metric("Ожидаемое количество нулей", f"{expected_zero:.1f}")
                    st.metric("Фактическое количество нулей", actual_zero)
                    st.metric("Смещение", f"{bias:.6f}")
                    
                    if bias > 0.001:
                        st.error("✅ Обнаружено значительное смещение!")
                    else:
                        st.success("❌ Смещение не обнаружено (возможно, недостаточно данных)")
                    
                    # Визуализация распределения
                    self.visualize_rc4_bias(second_bytes)
        
        with col2:
            st.markdown("#### Практическое значение")
            st.write("""
            **Последствия смещения:**
            - Снижение энтропии ключевого потока
            - Возможность статистических атак
            - Упрощение криптоанализа
            
            **Исторический контекст:**
            - В WEP это приводило к взлому за несколько минут
            - В TLS 1.0 позволяло восстанавливать cookies
            """)
    
    def render_rc4_fms_attack(self):
        """Демонстрация атаки FMS на RC4"""
        st.markdown("#### Атака FMS на RC4")
        
        st.info("""
        **Атака Fluhrer-Mantin-Shamir** использует слабые IV в WEP для восстановления ключа.
        """)
        
        st.write("""
        **Принцип атаки:**
        1. WEP использует конкатенацию IV и ключа
        2. Некоторые IV слабые и предсказуемы
        3. Анализируя множество пакетов, можно восстановить ключ по частям
        """)
        
        # Упрощенная демонстрация
        if st.button("🎭 Демонстрация атаки FMS", type="primary"):
            with st.spinner("Моделирую атаку FMS..."):
                # Генерируем "слабые" IV
                weak_ivs = self.generate_weak_ivs(50)
                
                # Моделируем атаку
                recovered_key = self.simulate_fms_attack(weak_ivs)
                
                st.success(f"**Восстановленный ключ (первые байты):** {recovered_key[:8]}...")
                
                # Визуализация процесса атаки
                self.visualize_fms_attack(weak_ivs, recovered_key)
    
    def render_rc4_key_reuse(self):
        """Атака на повторное использование ключа"""
        st.markdown("#### Атака на повторное использование ключа")
        
        st.error("""
        ⚠️ **Повторное использование ключевого потока** - самая опасная уязвимость поточных шифров!
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            plaintext1 = st.text_input("Первый открытый текст:", "Секретное сообщение 1")
            plaintext2 = st.text_input("Второй открытый текст:", "Секретное сообщение 2")
            
            if st.button("🔓 Продемонстрировать атаку", type="primary"):
                # Шифруем оба текста одним ключевым потоком
                key_stream = [random.randint(0, 255) for _ in range(max(len(plaintext1), len(plaintext2)))]
                
                cipher1 = self.xor_encrypt(plaintext1, key_stream)
                cipher2 = self.xor_encrypt(plaintext2, key_stream)
                
                # Атака: C1 ⊕ C2 = P1 ⊕ P2
                xor_ciphers = [c1 ^ c2 for c1, c2 in zip(cipher1, cipher2)]
                xor_plaintexts = [ord(p1) ^ ord(p2) for p1, p2 in zip(plaintext1, plaintext2)]
                
                st.success("**Результаты атаки:**")
                st.write(f"Зашифрованный текст 1: {[hex(c) for c in cipher1[:10]]}...")
                st.write(f"Зашифрованный текст 2: {[hex(c) for c in cipher2[:10]]}...")
                st.write(f"C1 ⊕ C2: {[hex(x) for x in xor_ciphers[:10]]}...")
                st.write(f"P1 ⊕ P2: {[hex(x) for x in xor_plaintexts[:10]]}...")
                
                if xor_ciphers[:min(len(plaintext1), len(plaintext2))] == xor_plaintexts[:min(len(plaintext1), len(plaintext2))]:
                    st.error("💀 Атака успешна! Можно восстановить оба текста!")
        
        with col2:
            st.markdown("#### Как работает атака:")
            st.latex(r"C_1 = P_1 \oplus K")
            st.latex(r"C_2 = P_2 \oplus K") 
            st.latex(r"C_1 \oplus C_2 = P_1 \oplus P_2")
            st.write("""
            **Зная P1 ⊕ P2, можно:**
            - Угадывать часто встречающиеся слова
            - Использовать частотный анализ
            - Восстанавливать оба текста
            """)
    
    def render_correlation_analysis(self):
        """Корреляционный анализ"""
        st.markdown("### 📈 Корреляционный анализ")
        
        st.info("""
        Корреляционные атаки ищут статистические зависимости между ключевым потоком 
        и внутренним состоянием генератора.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Генерация тестовых данных")
            
            generator_type = st.selectbox(
                "Тип генератора:",
                ["LFSR", "LKG", "Комбинированный генератор"]
            )
            
            sequence_length = st.slider("Длина последовательности:", 100, 10000, 1000)
            
            if st.button("📊 Выполнить корреляционный анализ", type="primary"):
                with st.spinner("Анализирую корреляции..."):
                    # Генерируем последовательность
                    if generator_type == "LFSR":
                        sequence = self.generate_lfsr_sequence([1,0,0,1,0,1], sequence_length)
                    elif generator_type == "LKG":
                        sequence = self.generate_lkg_sequence(1664525, 1013904223, 2**32, 123456789, sequence_length)
                        sequence = [x % 2 for x in sequence]  # Берем младшие биты
                    else:
                        sequence = [random.randint(0, 1) for _ in range(sequence_length)]
                    
                    # Анализ корреляций
                    autocorr = self.calculate_autocorrelation(sequence, 50)
                    cross_corr = self.calculate_cross_correlation(sequence, 20)
                    
                    # Визуализация
                    self.visualize_correlation_analysis(sequence, autocorr, cross_corr, generator_type)
        
        with col2:
            st.markdown("#### Методы корреляционного анализа")
            
            st.write("""
            **Автокорреляция:**
            - Проверяет зависимость между битами с разным лагом
            - Для случайной последовательности должна быть близка к 0
            
            **Кросс-корреляция:**
            - Сравнивает разные части последовательности
            - Обнаруживает периодичности
            
            **Линейная аппроксимация:**
            - Ищет линейные зависимости
            - Основа многих практических атак
            """)
    
    # Методы реализации атак и тестов
    
    def berlekamp_massey_attack(self, sequence, max_degree):
        """Упрощенная реализация атаки Берлекэмпа-Масси"""
        n = len(sequence)
        C = [1]  # Текущий полином
        B = [1]  # Лучший предыдущий полином
        L = 0    # Текущая длина LFSR
        
        for i in range(n):
            # Вычисляем невязку
            discrepancy = sequence[i]
            for j in range(1, len(C)):
                if j <= i:
                    discrepancy ^= (C[j] & sequence[i - j])
            
            if discrepancy != 0:
                T = C.copy()
                
                # Сдвигаем B и добавляем к C
                shift = i - L
                if shift > 0:
                    B_shifted = [0] * shift + B
                else:
                    B_shifted = B
                
                # Выравниваем длины
                max_len = max(len(C), len(B_shifted))
                C = C + [0] * (max_len - len(C))
                B_shifted = B_shifted + [0] * (max_len - len(B_shifted))
                
                # XOR
                C = [(C[j] ^ B_shifted[j]) for j in range(max_len)]
                
                if L <= i // 2:
                    L = i + 1 - L
                    B = T
        
        # Упрощаем полином (убираем ведущие нули)
        while len(C) > 1 and C[-1] == 0:
            C.pop()
        
        return C, L
    
    def format_polynomial(self, coeffs):
        """Форматирует полином для отображения"""
        terms = []
        for i, coeff in enumerate(coeffs):
            if coeff == 1:
                if i == 0:
                    terms.append("1")
                else:
                    terms.append(f"x^{i}")
        
        if not terms:
            return "0"
        
        return " + ".join(reversed(terms))
    
    def verify_lfsr_polynomial(self, sequence, polynomial):
        """Проверяет, что полином корректно генерирует последовательность"""
        if len(polynomial) < 2:
            return False
        
        # Генерируем последовательность с этим полиномом
        test_seq = self.generate_lfsr_sequence(polynomial, len(sequence))
        
        # Сравниваем с исходной
        return test_seq == sequence[:len(test_seq)]
    
    def generate_lfsr_sequence(self, polynomial, length):
        """Генерирует последовательность LFSR"""
        if len(polynomial) < 2:
            return []
        
        # Начальное состояние (все 1)
        state = [1] * (len(polynomial) - 1)
        sequence = []
        
        for _ in range(length):
            # Вычисляем новый бит
            new_bit = 0
            for i in range(1, len(polynomial)):
                if polynomial[i] == 1:
                    new_bit ^= state[len(polynomial) - 1 - i]
            
            sequence.append(state[-1])  # Выходной бит
            state = [new_bit] + state[:-1]  # Сдвиг
        
        return sequence
    
    def perform_nist_tests(self, sequence, selected_tests):
        """Выполняет выбранные тесты NIST"""
        results = {}
        
        if "Frequency Test" in selected_tests:
            results["Frequency Test"] = self.frequency_test(sequence)
        
        if "Runs Test" in selected_tests:
            results["Runs Test"] = self.runs_test(sequence)
        
        if "Autocorrelation Test" in selected_tests:
            results["Autocorrelation Test"] = self.autocorrelation_test(sequence)
        
        if "Linear Complexity Test" in selected_tests:
            results["Linear Complexity Test"] = self.linear_complexity_test(sequence)
        
        if "Entropy Test" in selected_tests:
            results["Entropy Test"] = self.entropy_test(sequence)
        
        return results
    
    def frequency_test(self, sequence):
        """Тест частоты (монобитный тест)"""
        n = len(sequence)
        ones_count = sum(sequence)
        zeros_count = n - ones_count
        
        # Статистика хи-квадрат
        expected = n / 2
        chi2 = (ones_count - expected)**2 / expected + (zeros_count - expected)**2 / expected
        
        # P-value
        p_value = math.exp(-chi2 / 2)
        
        # Порог 0.01
        passed = p_value > 0.01
        details = f"Единицы: {ones_count}/{n}, Хи-квадрат: {chi2:.4f}"
        
        return passed, p_value, details
    
    def runs_test(self, sequence):
        """Тест серий (runs test)"""
        n = len(sequence)
        
        # Считаем серии
        runs = 1
        current_bit = sequence[0]
        
        for bit in sequence[1:]:
            if bit != current_bit:
                runs += 1
                current_bit = bit
        
        # Ожидаемое количество серий
        expected_runs = (2 * n - 1) / 3
        
        # Статистика (упрощенная)
        deviation = abs(runs - expected_runs) / math.sqrt(16 * n / 15)
        p_value = math.exp(-deviation**2 / 2)
        
        passed = p_value > 0.01
        details = f"Серии: {runs}, Ожидалось: {expected_runs:.1f}"
        
        return passed, p_value, details
    
    def autocorrelation_test(self, sequence, lag=1):
        """Тест автокорреляции"""
        n = len(sequence)
        
        if lag >= n:
            return True, 1.0, "Недостаточно данных"
        
        # Считаем корреляцию
        correlated = 0
        for i in range(n - lag):
            if sequence[i] == sequence[i + lag]:
                correlated += 1
        
        correlation = correlated / (n - lag)
        expected = 0.5
        
        # Статистика
        deviation = abs(correlation - expected) / math.sqrt(1/(4*(n-lag)))
        p_value = math.exp(-deviation**2 / 2)
        
        passed = p_value > 0.01
        details = f"Корреляция при лаге {lag}: {correlation:.4f}"
        
        return passed, p_value, details
    
    def linear_complexity_test(self, sequence):
        """Тест линейной сложности"""
        # Используем Берлекэмп-Масси для оценки сложности
        poly, complexity = self.berlekamp_massey_attack(sequence, len(sequence)//2)
        
        # Для случайной последовательности сложность ~ n/2
        expected = len(sequence) / 2
        ratio = complexity / expected
        
        # Эвристическая проверка
        passed = 0.4 < ratio < 0.6
        p_value = 1.0 if passed else 0.0
        details = f"Сложность: {complexity}, Ожидалось: {expected:.1f}"
        
        return passed, p_value, details
    
    def entropy_test(self, sequence):
        """Тест энтропии"""
        n = len(sequence)
        ones = sum(sequence)
        p1 = ones / n
        p0 = 1 - p1
        
        # Энтропия Шеннона
        if p0 > 0 and p1 > 0:
            entropy = -p0 * math.log2(p0) - p1 * math.log2(p1)
        else:
            entropy = 0
        
        # Для случайной последовательности энтропия должна быть близка к 1
        passed = entropy > 0.95
        p_value = entropy  # Используем энтропию как p-value
        details = f"Энтропия: {entropy:.4f}"
        
        return passed, p_value, details
    
    def simplified_rc4(self, key, output_length):
        """Упрощенная реализация RC4 для демонстрации"""
        # Инициализация S-блока
        S = list(range(256))
        j = 0
        
        # Key Scheduling Algorithm (KSA)
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        # Pseudo-Random Generation Algorithm (PRGA)
        i = j = 0
        output = []
        
        for _ in range(output_length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            k = S[(S[i] + S[j]) % 256]
            output.append(k)
        
        return output
    
    def generate_weak_ivs(self, count):
        """Генерирует слабые IV для демонстрации атаки FMS"""
        weak_ivs = []
        for i in range(count):
            # Слабые IV имеют определенные паттерны
            iv = [3, 255, i]  # Пример слабого IV
            weak_ivs.append(iv)
        return weak_ivs
    
    def simulate_fms_attack(self, weak_ivs):
        """Упрощенная симуляция атаки FMS"""
        # В реальной атаке анализируются тысячи пакетов
        # Здесь просто демонстрируем принцип
        
        recovered_key = []
        for i in range(min(8, len(weak_ivs))):
            # Упрощенное "восстановление" байта ключа
            key_byte = (weak_ivs[i][2] + i) % 256
            recovered_key.append(key_byte)
        
        return recovered_key
    
    def xor_encrypt(self, plaintext, key_stream):
        """Шифрование XOR"""
        cipher = []
        for i, char in enumerate(plaintext):
            if i < len(key_stream):
                cipher.append(ord(char) ^ key_stream[i])
            else:
                break
        return cipher
    
    def calculate_cross_correlation(self, sequence, max_lag):
        """Вычисляет кросс-корреляцию"""
        n = len(sequence)
        cross_corr = []
        
        for lag in range(1, max_lag + 1):
            if 2 * lag >= n:
                break
            
            # Сравниваем первую и вторую половины
            first_half = sequence[:n//2]
            second_half = sequence[n//2:n//2 + len(first_half)]
            
            if lag < len(second_half):
                correlated = sum(1 for i in range(len(first_half) - lag) 
                               if first_half[i] == second_half[i + lag])
                correlation = correlated / (len(first_half) - lag)
                cross_corr.append(correlation)
        
        return cross_corr
    
    # Методы визуализации
    
    def visualize_lfsr_structure(self, polynomial):
        """Визуализирует структуру LFSR"""
        st.markdown("#### Структура LFSR")
        
        fig, ax = plt.subplots(figsize=(10, 3))
        
        # Рисуем регистр сдвига
        n = len(polynomial) - 1
        
        for i in range(n):
            # Ячейка регистра
            ax.add_patch(plt.Rectangle((i, 0), 0.8, 0.4, fill=True, color='lightblue'))
            ax.text(i + 0.4, 0.2, f"D{i}", ha='center', va='center', weight='bold')
        
        # Обратные связи
        for i in range(1, len(polynomial)):
            if polynomial[i] == 1:
                # Линия обратной связи
                ax.plot([i-1 + 0.4, n-1 + 0.8], [0.4, 0.6], 'r-', linewidth=2)
                ax.plot([n-1 + 0.8, n-1 + 0.8, 0.4], [0.6, 0.8, 0.8], 'r-', linewidth=2)
                ax.plot([0.4, -0.2], [0.8, 0.2], 'r-', linewidth=2)
        
        ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-0.5, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        st.pyplot(fig)
    
    def visualize_nist_results(self, sequence, results):
        """Визуализирует результаты тестов NIST"""
        st.markdown("#### Визуализация анализа")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # График 1: Распределение битов
        bit_counts = [sequence.count(0), sequence.count(1)]
        ax1.bar(['0', '1'], bit_counts, color=['blue', 'red'], alpha=0.7)
        ax1.set_title('Распределение битов')
        ax1.set_ylabel('Количество')
        for i, count in enumerate(bit_counts):
            ax1.text(i, count, str(count), ha='center', va='bottom')
        
        # График 2: Автокорреляция
        autocorr = self.calculate_autocorrelation(sequence, 20)
        ax2.plot(range(1, len(autocorr) + 1), autocorr, 'go-', alpha=0.7)
        ax2.axhline(y=0, color='red', linestyle='--')
        ax2.set_title('Автокорреляция')
        ax2.set_xlabel('Лаг')
        ax2.set_ylabel('Корреляция')
        ax2.grid(True, alpha=0.3)
        
        # График 3: Бегущая частота
        running_freq = []
        ones_so_far = 0
        for i, bit in enumerate(sequence):
            ones_so_far += bit
            running_freq.append(ones_so_far / (i + 1))
        
        ax3.plot(running_freq, 'b-', alpha=0.7)
        ax3.axhline(y=0.5, color='red', linestyle='--', label='Идеальная частота')
        ax3.set_title('Бегущая частота единиц')
        ax3.set_xlabel('Позиция')
        ax3.set_ylabel('Частота')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # График 4: Результаты тестов
        test_names = list(results.keys())
        test_scores = [results[name][1] for name in test_names]  # P-values
        
        bars = ax4.bar(test_names, test_scores, color=['green' if score > 0.01 else 'red' for score in test_scores])
        ax4.axhline(y=0.01, color='red', linestyle='--', label='Порог 0.01')
        ax4.set_title('P-values тестов NIST')
        ax4.set_ylabel('P-value')
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend()
        
        for bar, score in zip(bars, test_scores):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{score:.3f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_rc4_bias(self, second_bytes):
        """Визуализирует смещение в RC4"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # График 1: Распределение вторых байтов
        byte_counts = [0] * 256
        for byte in second_bytes:
            byte_counts[byte] += 1
        
        ax1.bar(range(256), byte_counts, alpha=0.7)
        ax1.set_title('Распределение вторых байтов RC4')
        ax1.set_xlabel('Значение байта')
        ax1.set_ylabel('Частота')
        
        # Подсвечиваем ноль
        ax1.bar([0], [byte_counts[0]], color='red', alpha=0.8, label='Ноль (смещен)')
        ax1.legend()
        
        # График 2: Сравнение с равномерным распределением
        expected = len(second_bytes) / 256
        actual_zero = byte_counts[0]
        
        ax2.bar(['Ожидаемо', 'Фактически'], [expected, actual_zero], 
                color=['blue', 'red'], alpha=0.7)
        ax2.set_title('Сравнение частоты нулевого байта')
        ax2.set_ylabel('Количество')
        
        for i, val in enumerate([expected, actual_zero]):
            ax2.text(i, val, f'{val:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_fms_attack(self, weak_ivs, recovered_key):
        """Визуализирует атаку FMS"""
        st.markdown("#### Процесс атаки FMS")
        
        # Показываем слабые IV
        st.write("**Использованные слабые IV:**")
        iv_df = pd.DataFrame(weak_ivs[:10], columns=['IV[0]', 'IV[1]', 'IV[2]'])
        st.dataframe(iv_df, use_container_width=True)
        
        # Показываем восстановление ключа
        st.write("**Восстановление ключа по байтам:**")
        key_progress = []
        for i in range(len(recovered_key)):
            key_progress.append({
                'Байт': i + 1,
                'Значение': recovered_key[i],
                'Уверенность': f"{(i+1)/len(recovered_key)*100:.1f}%"
            })
        
        st.dataframe(pd.DataFrame(key_progress), use_container_width=True)
    
    def visualize_correlation_analysis(self, sequence, autocorr, cross_corr, generator_type):
        """Визуализирует корреляционный анализ"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # График 1: Исходная последовательность (первые 200 бит)
        ax1.plot(sequence[:200], 'b-', alpha=0.7, linewidth=0.5)
        ax1.set_title(f'Последовательность ({generator_type}) - первые 200 бит')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Бит')
        ax1.set_yticks([0, 1])
        ax1.grid(True, alpha=0.3)
        
        # График 2: Автокорреляция
        ax2.plot(range(1, len(autocorr) + 1), autocorr, 'ro-', alpha=0.7)
        ax2.axhline(y=0, color='red', linestyle='--', label='Нулевая корреляция')
        ax2.set_title('Автокорреляция')
        ax1.set_xlabel('Лаг')
        ax1.set_ylabel('Корреляция')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # График 3: Кросс-корреляция
        if cross_corr:
            ax3.plot(range(1, len(cross_corr) + 1), cross_corr, 'go-', alpha=0.7)
            ax3.axhline(y=0.5, color='red', linestyle='--', label='Ожидаемая корреляция')
            ax3.set_title('Кросс-корреляция (первая vs вторая половина)')
            ax3.set_xlabel('Лаг')
            ax3.set_ylabel('Корреляция')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # График 4: 2D распределение (xₙ vs xₙ₊₁)
        if len(sequence) > 1000:
            pairs = list(zip(sequence[:1000], sequence[1:1001]))
            zero_zero = pairs.count((0, 0))
            zero_one = pairs.count((0, 1)) 
            one_zero = pairs.count((1, 0))
            one_one = pairs.count((1, 1))
            
            matrix = [[zero_zero, zero_one], [one_zero, one_one]]
            im = ax4.imshow(matrix, cmap='Blues', interpolation='nearest')
            
            ax4.set_xticks([0, 1])
            ax4.set_yticks([0, 1])
            ax4.set_xticklabels(['0', '1'])
            ax4.set_yticklabels(['0', '1'])
            ax4.set_xlabel('xₙ₊₁')
            ax4.set_ylabel('xₙ')
            ax4.set_title('Переходная матрица (xₙ → xₙ₊₁)')
            
            # Добавляем значения в ячейки
            for i in range(2):
                for j in range(2):
                    ax4.text(j, i, f'{matrix[i][j]}', 
                            ha='center', va='center', color='black', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)

    def generate_lkg_sequence(self, a, c, m, seed, count):
        """Генерирует последовательность LKG (из предыдущего модуля)"""
        sequence = []
        x = seed
        
        for _ in range(count):
            x = (a * x + c) % m
            sequence.append(x)
        
        return sequence

    def calculate_autocorrelation(self, sequence, max_lag=None):
        """Вычисляет автокорреляцию последовательности"""
        if max_lag is None:
            max_lag = min(20, len(sequence)//2)
        
        autocorr = []
        n = len(sequence)
        
        for lag in range(1, max_lag + 1):
            if lag >= n:
                break
            
            # Простая автокорреляция
            corr = np.corrcoef(sequence[:-lag], sequence[lag:])[0, 1]
            if np.isnan(corr):
                corr = 0
            autocorr.append(corr)
        
        return autocorr