from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import Counter
import random

class PRNGMethodsModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Генераторы ПСЧ"
        self.description = "ЛКГ, Фибоначчи, BBS и другие методы генерации ПСЧ"
        self.category = "stream"
        self.icon = ""
        self.order = 2
    
    def render(self):
        st.title("🎲 Генераторы псевдослучайных чисел")
        st.subheader("Линейный конгруэнтный генератор, метод Фибоначчи, BBS")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Криптографические генераторы ПСЧ
            
            **Требования к криптографическим ГПСЧ:**
            1. **Предсказуемость** - невозможно предсказать следующие числа
            2. **Равномерное распределение** - все числа равновероятны
            3. **Длинный период** - последовательность не должна повторяться
            4. **Эффективность** - быстрая генерация
            
            **Основные алгоритмы:**
            
            **Линейный конгруэнтный генератор (LKG):**
            - Формула: `Xₙ₊₁ = (a * Xₙ + c) mod m`
            - Быстрый, но предсказуемый
            - Используется в системах, где безопасность не критична
            
            **Метод Фибоначчи с запаздываниями:**
            - `Xₙ = (Xₙ₋ₐ + Xₙ₋բ) mod m`
            - Длинные периоды, лучшее распределение
            - Менее предсказуем чем LKG
            
            **Генератор Блюма-Блюма-Шуба (BBS):**
            - `Xₙ₊₁ = Xₙ² mod M`, где M = p*q
            - Криптографически стойкий
            - Медленный, но безопасный
            """)
        
        # Выбор алгоритма
        algorithm = st.radio(
            "Выберите алгоритм генерации:",
            ["📊 Линейный конгруэнтный генератор (LKG)", 
             "📈 Метод Фибоначчи с запаздываниями", 
             "🔐 Генератор Блюма-Блюма-Шуба (BBS)",
             "📊 Сравнительный анализ"],
            horizontal=True
        )
        
        if "Линейный конгруэнтный" in algorithm:
            self.render_lkg()
        elif "Фибоначчи" in algorithm:
            self.render_fibonacci()
        elif "Блюма-Блюма-Шуба" in algorithm:
            self.render_bbs()
        else:
            self.render_comparison()
    
    def render_lkg(self):
        """Линейный конгруэнтный генератор"""
        st.markdown("### 📊 Линейный конгруэнтный генератор (LKG)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Параметры генератора")
            a = st.slider("Множитель (a):", 1, 1000, 1664525, 
                         help="Множитель в формуле Xₙ₊₁ = (a * Xₙ + c) mod m")
            c = st.slider("Приращение (c):", 0, 1000, 1013904223,
                         help="Приращение в формуле")
            m = st.slider("Модуль (m):", 2, 10000, 2**32,
                         help="Модуль в формуле. Обычно степень двойки")
            seed = st.number_input("Начальное значение (seed):", 0, m-1, 123456789)
            count = st.slider("Количество чисел:", 10, 1000, 100)
        
        with col2:
            st.markdown("#### Генерация последовательности")
            
            if st.button("🎲 Сгенерировать последовательность", type="primary"):
                with st.spinner("Генерирую последовательность..."):
                    sequence = self.generate_lkg_sequence(a, c, m, seed, count)
                    
                    # Показываем последовательность
                    st.success(f"**Сгенерировано {count} чисел:**")
                    
                    # Отображаем первые 20 чисел
                    preview = sequence[:20]
                    st.text_area("Первые 20 чисел:", " ".join(map(str, preview)), height=100)
                    
                    # Анализ последовательности
                    self.analyze_sequence(sequence, m, "LKG")
                    
                    # Визуализация
                    self.visualize_lkg(sequence, a, c, m, seed)
    
    def generate_lkg_sequence(self, a, c, m, seed, count):
        """Генерирует последовательность LKG"""
        sequence = []
        x = seed
        
        for _ in range(count):
            x = (a * x + c) % m
            sequence.append(x)
        
        return sequence
    
    def render_fibonacci(self):
        """Метод Фибоначчи с запаздываниями"""
        st.markdown("### 📈 Метод Фибоначчи с запаздываниями")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Параметры генератора")
            lag1 = st.slider("Первое запаздывание (j):", 2, 100, 24,
                           help="Первое запаздывание в формуле Xₙ = (Xₙ₋ⱼ + Xₙ₋ₖ) mod m")
            lag2 = st.slider("Второе запаздывание (k):", 2, 100, 55,
                           help="Второе запаздывание, должно быть больше первого")
            m = st.slider("Модуль (m):", 2, 10000, 2**32)
            count = st.slider("Количество чисел:", 10, 1000, 100)
            
            # Инициализация начальных значений
            st.markdown("#### Начальные значения")
            init_count = max(lag1, lag2)
            st.info(f"Нужно ввести {init_count} начальных значений")
            
            initial_values = []
            for i in range(init_count):
                val = st.number_input(f"Начальное значение {i+1}:", 0, m-1, 
                                    random.randint(0, m-1), key=f"fib_init_{i}")
                initial_values.append(val)
        
        with col2:
            st.markdown("#### Генерация последовательности")
            
            if st.button("🎲 Сгенерировать последовательность Фибоначчи", type="primary"):
                if lag2 <= lag1:
                    st.error("Второе запаздывание должно быть больше первого!")
                    return
                
                with st.spinner("Генерирую последовательность..."):
                    sequence = self.generate_fibonacci_sequence(lag1, lag2, m, initial_values, count)
                    
                    # Показываем последовательность
                    st.success(f"**Сгенерировано {count} чисел:**")
                    
                    # Отображаем первые 20 чисел
                    preview = sequence[:20]
                    st.text_area("Первые 20 чисел:", " ".join(map(str, preview)), height=100)
                    
                    # Анализ последовательности
                    self.analyze_sequence(sequence, m, "Фибоначчи")
                    
                    # Визуализация
                    self.visualize_fibonacci(sequence, lag1, lag2, m)
    
    def generate_fibonacci_sequence(self, lag1, lag2, m, initial_values, count):
        """Генерирует последовательность методом Фибоначчи"""
        sequence = initial_values.copy()
        
        for i in range(len(initial_values), count):
            # Xₙ = (Xₙ₋ⱼ + Xₙ₋ₖ) mod m
            new_val = (sequence[i - lag1] + sequence[i - lag2]) % m
            sequence.append(new_val)
        
        return sequence
    
    def render_bbs(self):
        """Генератор Блюма-Блюма-Шуба"""
        st.markdown("### 🔐 Генератор Блюма-Блюма-Шуба (BBS)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Параметры генератора")
            
            # Предустановленные простые числа Блюма
            prime_pairs = {
                "Маленькие (для демонстрации)": {"p": 11, "q": 19},
                "Средние (учебные)": {"p": 227, "q": 283},
                "Большие (безопасные)": {"p": 10007, "q": 10039}
            }
            
            prime_choice = st.selectbox("Выберите простые числа:", list(prime_pairs.keys()))
            p = prime_pairs[prime_choice]["p"]
            q = prime_pairs[prime_choice]["q"]
            
            st.info(f"**Используются простые числа:** p = {p}, q = {q}")
            st.info(f"**Модуль:** M = p × q = {p * q}")
            
            seed = st.number_input("Начальное значение (seed):", 1, p*q-1, 
                                 random.randint(1, p*q-1),
                                 help="Должно быть взаимно просто с M")
            count = st.slider("Количество бит:", 10, 1000, 100)
        
        with col2:
            st.markdown("#### Генерация псевдослучайных бит")
            
            if st.button("🔐 Сгенерировать BBS последовательность", type="primary"):
                # Проверяем что seed взаимно прост с M
                M = p * q
                if math.gcd(seed, M) != 1:
                    st.error("Начальное значение должно быть взаимно простым с M!")
                    return
                
                with st.spinner("Генерирую криптографически стойкую последовательность..."):
                    bits, numbers = self.generate_bbs_sequence(p, q, seed, count)
                    
                    # Показываем битовую последовательность
                    st.success(f"**Сгенерировано {count} бит:**")
                    
                    # Отображаем первые 50 бит
                    bit_string = ''.join(map(str, bits[:50]))
                    st.text_area("Первые 50 бит:", bit_string, height=100)
                    
                    # Анализ битовой последовательности
                    self.analyze_bit_sequence(bits, "BBS")
                    
                    # Визуализация
                    self.visualize_bbs(bits, numbers, p, q, seed)
    
    def generate_bbs_sequence(self, p, q, seed, count):
        """Генерирует последовательность BBS"""
        M = p * q
        x = seed
        bits = []
        numbers = []
        
        for _ in range(count):
            x = (x * x) % M  # Xₙ₊₁ = Xₙ² mod M
            numbers.append(x)
            bit = x % 2  # Младший бит
            bits.append(bit)
        
        return bits, numbers
    
    def render_comparison(self):
        """Сравнительный анализ генераторов"""
        st.markdown("### 📊 Сравнительный анализ генераторов ПСЧ")
        
        st.markdown("""
        **Сравнение характеристик разных генераторов:**
        """)
        
        # Генерируем последовательности для сравнения
        sequences = {}
        
        # LKG последовательность
        lkg_seq = self.generate_lkg_sequence(1664525, 1013904223, 2**32, 123456789, 1000)
        sequences["LKG"] = lkg_seq
        
        # Фибоначчи последовательность
        fib_init = [random.randint(0, 2**32-1) for _ in range(55)]
        fib_seq = self.generate_fibonacci_sequence(24, 55, 2**32, fib_init, 1000)
        sequences["Фибоначчи"] = fib_seq
        
        # BBS последовательность (биты)
        bbs_bits, bbs_nums = self.generate_bbs_sequence(227, 283, 12345, 1000)
        sequences["BBS"] = bbs_nums
        
        # Сравнительная таблица
        comparison_data = []
        for name, seq in sequences.items():
            if name == "BBS":
                # Для BBS анализируем битовую последовательность
                bits = [x % 2 for x in seq]  # Берем младшие биты
                ones_ratio = sum(bits) / len(bits)
            else:
                ones_ratio = sum(1 for x in seq if x % 2 == 1) / len(seq)
            
            # Вычисляем период (упрощенная оценка)
            period_est = self.estimate_period(seq)
            
            # Стандартное отклонение (мера равномерности)
            std_dev = np.std(seq) if seq else 0
            
            comparison_data.append({
                'Алгоритм': name,
                'Равномерность (0-1)': f"{ones_ratio:.3f}",
                'Оценка периода': f"{period_est}",
                'Стандартное отклонение': f"{std_dev:.1f}",
                'Криптостойкость': self.get_security_level(name)
            })
        
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
        
        # Визуализация сравнения
        self.visualize_comparison(sequences)
        
        # Рекомендации
        st.markdown("---")
        st.markdown("#### 🎯 Рекомендации по применению")
        
        recommendations = [
            "**LKG**: Для некритичных приложений, игр, симуляций",
            "**Фибоначчи**: Для научных вычислений, статистики", 
            "**BBS**: Для криптографии, безопасности, шифрования"
        ]
        
        for rec in recommendations:
            st.write(f"- {rec}")
    
    def analyze_sequence(self, sequence, modulus, algorithm_name):
        """Анализирует статистические свойства последовательности"""
        st.markdown("---")
        st.markdown(f"#### 📈 Статистический анализ ({algorithm_name})")
        
        # Нормализуем последовательность к [0, 1]
        normalized = [x / modulus for x in sequence]
        
        # Основные статистики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Среднее значение", f"{np.mean(normalized):.3f}")
        with col2:
            st.metric("Стандартное отклонение", f"{np.std(normalized):.3f}")
        with col3:
            ones_ratio = sum(1 for x in sequence if x % 2 == 1) / len(sequence)
            st.metric("Соотношение 1/0", f"{ones_ratio:.3f}")
        with col4:
            period_est = self.estimate_period(sequence)
            st.metric("Оценка периода", period_est)
        
        # Тест на равномерность (хи-квадрат упрощенный)
        chi2_score = self.chi2_uniformity_test(sequence, modulus)
        st.info(f"**Тест на равномерность:** {'✅ Прошел' if chi2_score < 0.05 else '⚠️ Требует внимания'}")
    
    def analyze_bit_sequence(self, bits, algorithm_name):
        """Анализирует битовую последовательность"""
        st.markdown("---")
        st.markdown(f"#### 📈 Статистический анализ битов ({algorithm_name})")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            ones_count = sum(bits)
            st.metric("Количество единиц", ones_count)
        with col2:
            zeros_count = len(bits) - ones_count
            st.metric("Количество нулей", zeros_count)
        with col3:
            ones_ratio = ones_count / len(bits)
            st.metric("Соотношение 1/0", f"{ones_ratio:.3f}")
        with col4:
            # Тест на монотонность (последовательные одинаковые биты)
            runs = self.count_runs(bits)
            st.metric("Серии бит", runs)
        
        # Тесты случайности
        if abs(ones_ratio - 0.5) < 0.05:
            st.success("✅ Соотношение 1/0 близко к идеальному (0.5)")
        else:
            st.warning("⚠️ Соотношение 1/0 отклоняется от идеального")
    
    def visualize_lkg(self, sequence, a, c, m, seed):
        """Визуализация LKG последовательности"""
        st.markdown("---")
        st.markdown("#### 📊 Визуализация LKG последовательности")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # График 1: Последовательность чисел
        ax1.plot(sequence, 'b-', alpha=0.7)
        ax1.set_title('Последовательность чисел')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Значение')
        ax1.grid(True, alpha=0.3)
        
        # График 2: Гистограмма распределения
        ax2.hist(sequence, bins=20, alpha=0.7, color='green', edgecolor='black')
        ax2.set_title('Распределение значений')
        ax2.set_xlabel('Значение')
        ax2.set_ylabel('Частота')
        ax2.grid(True, alpha=0.3)
        
        # График 3: Автокорреляция (первые 50 значений)
        autocorr = self.calculate_autocorrelation(sequence[:50])
        ax3.plot(autocorr, 'r-', alpha=0.7)
        ax3.set_title('Автокорреляция (первые 50 значений)')
        ax3.set_xlabel('Лаг')
        ax3.set_ylabel('Корреляция')
        ax3.grid(True, alpha=0.3)
        
        # График 4: Парные точки (xₙ vs xₙ₊₁)
        if len(sequence) > 1:
            ax4.scatter(sequence[:-1], sequence[1:], alpha=0.5, s=1)
            ax4.set_title('Парная диаграмма (xₙ vs xₙ₊₁)')
            ax4.set_xlabel('xₙ')
            ax4.set_ylabel('xₙ₊₁')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_fibonacci(self, sequence, lag1, lag2, m):
        """Визуализация последовательности Фибоначчи"""
        st.markdown("---")
        st.markdown("#### 📊 Визуализация последовательности Фибоначчи")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # График 1: Последовательность
        ax1.plot(sequence, 'b-', alpha=0.7)
        ax1.set_title('Последовательность Фибоначчи')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Значение')
        ax1.grid(True, alpha=0.3)
        
        # График 2: Гистограмма
        ax2.hist(sequence, bins=20, alpha=0.7, color='orange', edgecolor='black')
        ax2.set_title('Распределение значений')
        ax2.set_xlabel('Значение')
        ax2.set_ylabel('Частота')
        ax2.grid(True, alpha=0.3)
        
        # График 3: 3D визуализация (xₙ vs xₙ₋ⱼ vs xₙ₋ₖ)
        if len(sequence) > max(lag1, lag2) + 10:
            x = sequence[lag2:-lag1]
            y = sequence[lag1:-lag2]
            z = sequence[:-lag1-lag2]
            
            # Для 2D используем scatter
            ax3.scatter(x[:100], y[:100], alpha=0.5)
            ax3.set_title(f'Диаграмма (xₙ₋{lag1} vs xₙ₋{lag2})')
            ax3.set_xlabel(f'xₙ₋{lag1}')
            ax3.set_ylabel(f'xₙ₋{lag2}')
            ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_bbs(self, bits, numbers, p, q, seed):
        """Визуализация BBS последовательности"""
        st.markdown("---")
        st.markdown("#### 📊 Визуализация BBS генератора")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # График 1: Битовый поток
        ax1.plot(bits[:100], 'ro-', alpha=0.7, markersize=3)
        ax1.set_title('Битовый поток (первые 100 бит)')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Бит (0/1)')
        ax1.set_yticks([0, 1])
        ax1.grid(True, alpha=0.3)
        
        # График 2: Распределение битов
        bit_counts = [bits.count(0), bits.count(1)]
        ax2.bar(['0', '1'], bit_counts, color=['blue', 'red'], alpha=0.7)
        ax2.set_title('Распределение битов')
        ax2.set_ylabel('Количество')
        for i, count in enumerate(bit_counts):
            ax2.text(i, count, str(count), ha='center', va='bottom')
        
        # График 3: Последовательность чисел
        ax3.plot(numbers, 'g-', alpha=0.7)
        ax3.set_title('Числовая последовательность BBS')
        ax3.set_xlabel('Позиция')
        ax3.set_ylabel('Значение')
        ax3.grid(True, alpha=0.3)
        
        # График 4: Автокорреляция битов
        bit_autocorr = self.calculate_autocorrelation(bits[:50])
        ax4.plot(bit_autocorr, 'purple', alpha=0.7)
        ax4.set_title('Автокорреляция битов')
        ax4.set_xlabel('Лаг')
        ax4.set_ylabel('Корреляция')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_comparison(self, sequences):
        """Визуализация сравнения генераторов"""
        st.markdown("---")
        st.markdown("#### 📈 Сравнительная визуализация")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Распределение (первые 100 значений нормализованные)
        for name, seq in sequences.items():
            if len(seq) > 100:
                normalized = [x / max(seq) for x in seq[:100]]
                ax1.plot(normalized, label=name, alpha=0.7)
        
        ax1.set_title('Сравнение последовательностей (первые 100 значений)')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Нормализованное значение')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # График 2: Соотношение единиц в битовом представлении
        algorithms = []
        one_ratios = []
        
        for name, seq in sequences.items():
            # Берем младшие биты для сравнения
            bits = [x % 2 for x in seq]
            one_ratio = sum(bits) / len(bits)
            algorithms.append(name)
            one_ratios.append(one_ratio)
        
        bars = ax2.bar(algorithms, one_ratios, color=['blue', 'orange', 'green'], alpha=0.7)
        ax2.axhline(y=0.5, color='red', linestyle='--', label='Идеальное соотношение (0.5)')
        ax2.set_title('Соотношение единиц в младших битах')
        ax2.set_ylabel('Доля единиц')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend()
        
        for bar, ratio in zip(bars, one_ratios):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{ratio:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    # Вспомогательные методы для анализа
    
    def estimate_period(self, sequence):
        """Упрощенная оценка периода последовательности"""
        if len(sequence) < 10:
            return "Недостаточно данных"
        
        # Ищем повторяющиеся паттерны
        for period in range(1, min(100, len(sequence)//2)):
            if sequence[:period] == sequence[period:2*period]:
                return period
        return f">{len(sequence)//2}"
    
    def chi2_uniformity_test(self, sequence, modulus):
        """Упрощенный тест хи-квадрат на равномерность"""
        if len(sequence) < 20:
            return 1.0
        
        # Делим на 10 интервалов
        expected = len(sequence) / 10
        observed = [0] * 10
        
        for num in sequence:
            bucket = int((num / modulus) * 10)
            if bucket == 10:
                bucket = 9
            observed[bucket] += 1
        
        # Упрощенный хи-квадрат
        chi2 = sum((obs - expected)**2 / expected for obs in observed)
        return chi2
    
    def count_runs(self, bits):
        """Считает количество серий (runs) в битовой последовательности"""
        if not bits:
            return 0
        
        runs = 1
        current_bit = bits[0]
        
        for bit in bits[1:]:
            if bit != current_bit:
                runs += 1
                current_bit = bit
        
        return runs
    
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
    
    def get_security_level(self, algorithm):
        """Возвращает уровень безопасности алгоритма"""
        security_levels = {
            "LKG": "❌ Низкая",
            "Фибоначчи": "⚠️ Средняя", 
            "BBS": "✅ Высокая"
        }
        return security_levels.get(algorithm, "Неизвестно")

# Необходимый импорт для математических операций
import math