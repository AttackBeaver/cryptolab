from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from itertools import permutations

class MagicSquareModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Магический квадрат"
        self.description = "Шифрование с использованием магических квадратов"
        self.category = "classical"
        self.icon = ""
        self.order = 5
        
        # Инициализация session_state
        if 'magic_square' not in st.session_state:
            st.session_state.magic_square = None
        if 'square_size' not in st.session_state:
            st.session_state.square_size = 3
        if 'encrypted_message' not in st.session_state:
            st.session_state.encrypted_message = ""
        if 'decrypted_message' not in st.session_state:
            st.session_state.decrypted_message = ""
    
    def render(self):
        st.title("🔢 Магический квадрат")
        st.subheader("Криптография с использованием магических квадратов")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Магические квадраты в криптографии
            
            **Определение:**
            Магический квадрат - это квадратная таблица n×n, заполненная различными числами таким образом, 
            что сумма чисел в каждой строке, каждом столбце и на обеих диагоналях одинакова.
            
            **Магическая константа:** 
            ```
            M = n × (n² + 1) / 2
            ```
            
            **Принцип шифрования:**
            1. Создается магический квадрат (ключ)
            2. Буквы сообщения размещаются в ячейках в определенном порядке
            3. Чтение происходит в порядке возрастания чисел в квадрате
            4. Для дешифровки нужен тот же квадрат и знание порядка заполнения
            """)
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🎲 Создание квадратов", "🔐 Шифрование", "🔓 Дешифрование", "📊 Анализ"],
            horizontal=True
        )
        
        if mode == "🎲 Создание квадратов":
            self.render_square_creation()
        elif mode == "🔐 Шифрование":
            self.render_encryption()
        elif mode == "🔓 Дешифрование":
            self.render_decryption()
        else:
            self.render_analysis()
    
    def render_square_creation(self):
        """Создание магических квадратов"""
        st.markdown("### 🎲 Создание магических квадратов")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Параметры квадрата")
            square_size = st.selectbox(
                "Размер квадрата:",
                [3, 4, 5],
                index=0,
                help="Размер n×n магического квадрата"
            )
            
            generation_method = st.radio(
                "Метод генерации:",
                ["Сиамский метод (только нечетные)", "Ло Шу (3×3)", "Случайная перестановка"],
                index=0
            )
            
            if st.button("🎯 Создать магический квадрат", type="primary"):
                with st.spinner("Создаю магический квадрат..."):
                    try:
                        magic_square = self.generate_magic_square(square_size, generation_method)
                        if magic_square is not None:
                            st.session_state.magic_square = magic_square
                            st.session_state.square_size = square_size
                            st.success("✅ Квадрат успешно создан!")
                        else:
                            st.error("❌ Не удалось создать квадрат")
                    except Exception as e:
                        st.error(f"❌ Ошибка при создании квадрата: {e}")
        
        with col2:
            # Показываем созданный квадрат
            if st.session_state.magic_square is not None:
                magic_square = st.session_state.magic_square
                square_size = st.session_state.square_size
                
                st.success(f"### 🎉 Магический квадрат {square_size}×{square_size}")
                
                # Вычисляем магическую константу
                magic_constant = self.calculate_magic_constant(square_size)
                st.info(f"**Магическая константа:** {magic_constant}")
                
                # Отображаем квадрат
                self.display_magic_square(magic_square, square_size)
                
                # Проверяем магические свойства
                self.verify_magic_square(magic_square, square_size)
            else:
                st.info("Создайте магический квадрат для начала работы")
        
        # Примеры известных магических квадратов
        st.markdown("---")
        st.markdown("#### 📚 Известные магические квадраты")
        
        tab1, tab2 = st.tabs(["Ло Шу (3×3)", "Дюрер (4×4)"])
        
        with tab1:
            st.markdown("**Ло Шу - древнекитайский квадрат 3×3**")
            luoshu = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
            self.display_magic_square(luoshu, 3)
            st.info("Самый древний известный магический квадрат")
        
        with tab2:
            st.markdown("**Квадрат Дюрера из гравюры 'Меланхолия'**")
            durer = np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
            self.display_magic_square(durer, 4)
            st.info("Известен симметричными свойствами")
    
    def render_encryption(self):
        """Шифрование с использованием магического квадрата"""
        st.markdown("### 🔐 Шифрование магическим квадратом")
        
        # Проверяем наличие квадрата
        if st.session_state.magic_square is None:
            st.error("❌ Сначала создайте магический квадрат!")
            st.info("Перейдите в режим 'Создание квадратов'")
            return
        
        magic_square = st.session_state.magic_square
        square_size = st.session_state.square_size
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод сообщения")
            plaintext = st.text_area(
                "Текст для шифрования:",
                "HELLO WORLD",
                height=100,
                help=f"Максимум {square_size*square_size} символов"
            )
            
            if st.button("🔒 Зашифровать", type="primary"):
                if not plaintext.strip():
                    st.error("Введите текст для шифрования!")
                    return
                
                with st.spinner("Шифрую сообщение..."):
                    try:
                        encrypted = self.encrypt_with_magic_square(plaintext, magic_square, square_size)
                        st.session_state.encrypted_message = encrypted
                        st.session_state.last_plaintext = plaintext
                        st.success("✅ Сообщение успешно зашифровано!")
                    except Exception as e:
                        st.error(f"❌ Ошибка при шифровании: {e}")
        
        with col2:
            # Показываем результат шифрования
            if st.session_state.encrypted_message:
                encrypted = st.session_state.encrypted_message
                
                st.success("### 🎉 Зашифрованное сообщение")
                st.text_area("Результат:", encrypted, height=100, key="encrypted_output")
                
                # Показываем процесс заполнения
                if hasattr(st.session_state, 'last_plaintext'):
                    st.markdown("#### 📊 Процесс заполнения")
                    self.show_filling_process(st.session_state.last_plaintext, magic_square, square_size)
            else:
                st.info("Введите текст и нажмите 'Зашифровать'")
        
        # Показываем используемый квадрат
        st.markdown("---")
        st.markdown("#### 🎯 Используемый магический квадрат")
        self.display_magic_square(magic_square, square_size)
        
        # Инструкция по дешифровке
        st.markdown("#### 💡 Инструкция для дешифровки")
        st.info(f"""
        Для дешифровки получателю нужны:
        1. **Этот магический квадрат** {square_size}×{square_size}
        2. **Порядок чтения**: по возрастанию чисел в квадрате
        3. **Зашифрованное сообщение**: {st.session_state.encrypted_message if st.session_state.encrypted_message else 'будет здесь'}
        """)
    
    def render_decryption(self):
        """Дешифрование с использованием магического квадрата"""
        st.markdown("### 🔓 Дешифрование магическим квадратом")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод данных")
            ciphertext = st.text_area(
                "Зашифрованный текст:",
                st.session_state.encrypted_message if st.session_state.encrypted_message else "HORLLEW OLD",
                height=100
            )
            
            # Автоматическое определение размера квадрата
            if st.session_state.magic_square is not None:
                square_size = st.session_state.square_size
                use_saved_square = True
                st.info(f"Используется созданный квадрат {square_size}×{square_size}")
            else:
                square_size = st.selectbox("Размер квадрата:", [3, 4, 5], index=0)
                use_saved_square = False
                st.warning("Используется стандартный квадрат")
            
            if st.button("🔓 Дешифровать", type="primary"):
                if not ciphertext.strip():
                    st.error("Введите зашифрованный текст!")
                    return
                
                with st.spinner("Дешифрую сообщение..."):
                    try:
                        if use_saved_square and st.session_state.magic_square is not None:
                            magic_square = st.session_state.magic_square
                        else:
                            # Создаем стандартный квадрат для демонстрации
                            magic_square = self.generate_magic_square(square_size, "Ло Шу (3×3)" if square_size == 3 else "Сиамский метод (только нечетные)")
                        
                        decrypted = self.decrypt_with_magic_square(ciphertext, magic_square, square_size)
                        st.session_state.decrypted_message = decrypted
                        st.success("✅ Сообщение успешно дешифровано!")
                    except Exception as e:
                        st.error(f"❌ Ошибка при дешифровании: {e}")
        
        with col2:
            if st.session_state.decrypted_message:
                decrypted = st.session_state.decrypted_message
                
                st.success("### 🎉 Дешифрованное сообщение")
                st.text_area("Результат:", decrypted, height=100, key="decrypted_output")
                
                # Проверяем качество дешифровки
                if hasattr(st.session_state, 'last_plaintext') and st.session_state.last_plaintext:
                    original_clean = st.session_state.last_plaintext.upper().replace(' ', '')
                    decrypted_clean = decrypted.upper().replace(' ', '')
                    
                    if original_clean == decrypted_clean:
                        st.balloons()
                        st.success("🎉 Дешифровка полностью совпадает с оригиналом!")
                    else:
                        st.warning("⚠️ Дешифровка не полностью совпадает с оригиналом")
                
                # Показываем использованный квадрат
                st.markdown("#### 🎯 Использованный квадрат")
                if use_saved_square and st.session_state.magic_square is not None:
                    self.display_magic_square(st.session_state.magic_square, square_size)
                else:
                    magic_square = self.generate_magic_square(square_size, "Ло Шу (3×3)" if square_size == 3 else "Сиамский метод (только нечетные)")
                    self.display_magic_square(magic_square, square_size)
            else:
                st.info("Введите зашифрованный текст и нажмите 'Дешифровать'")
    
    def render_analysis(self):
        """Анализ магических квадратов"""
        st.markdown("### 📊 Анализ магических квадратов")
        
        st.info("""
        **Криптографические свойства магических квадратов:**
        
        **Преимущества:**
        - Простота реализации
        - Визуальная понятность
        - Историческая значимость
        
        **Недостатки:**
        - Ограниченная вместимость (n² символов)
        - Необходимость передачи квадрата
        - Уязвимость к частотному анализу
        - Предсказуемость при известном квадрате
        """)
        
        # Математические свойства
        st.markdown("#### 🧮 Математические свойства")
        
        sizes = [3, 4, 5]
        data = []
        for n in sizes:
            magic_constant = self.calculate_magic_constant(n)
            total_cells = n * n
            data.append({
                'Размер n': n,
                'Магическая константа': magic_constant,
                'Ячеек': total_cells,
                'Макс. символов': total_cells,
                'Сумма всех чисел': sum(range(1, total_cells + 1))
            })
        
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        
        # Генерация примеров
        if st.button("🔄 Сгенерировать примеры квадратов"):
            self.show_examples()
    
    def generate_magic_square(self, n, method):
        """Генерирует магический квадрат заданного размера и метода"""
        try:
            if method == "Сиамский метод (только нечетные)":
                if n % 2 == 0:
                    st.warning("Сиамский метод работает только для нечетных размеров. Использую Ло Шу для n=4.")
                    return self.generate_4x4_square()
                return self.siamese_method(n)
            elif method == "Ло Шу (3×3)":
                if n != 3:
                    st.warning("Ло Шу только для 3×3. Использую сиамский метод.")
                    return self.siamese_method(n)
                return np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
            elif method == "Случайная перестановка":
                return self.random_magic_square(n)
            else:
                return self.siamese_method(n)
        except Exception as e:
            st.error(f"Ошибка в generate_magic_square: {e}")
            return None
    
    def siamese_method(self, n):
        """Сиамский метод для нечетных n - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        if n % 2 == 0:
            return self.generate_4x4_square()  # Fallback for even n
        
        magic_square = np.zeros((n, n), dtype=int)
        
        # Начальная позиция - середина верхней строки
        i, j = 0, n // 2
        magic_square[i, j] = 1
        
        for num in range(2, n * n + 1):
            # Двигаемся вверх-вправо
            new_i, new_j = (i - 1) % n, (j + 1) % n
            
            # Если ячейка занята, двигаемся вниз от текущей позиции
            if magic_square[new_i, new_j] != 0:
                new_i, new_j = (i + 1) % n, j
            
            i, j = new_i, new_j
            magic_square[i, j] = num
        
        return magic_square
    
    def generate_4x4_square(self):
        """Генерирует магический квадрат 4×4"""
        # Один из стандартных магических квадратов 4×4
        return np.array([[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]])
    
    def random_magic_square(self, n):
        """Генерирует случайный магический квадрат (упрощенно)"""
        if n == 3:
            # Для n=3 используем перестановки Ло Шу
            base = np.array([[4, 9, 2], [3, 5, 7], [8, 1, 6]])
            # Применяем случайные симметрии
            import random
            transformations = [
                lambda x: x,
                lambda x: np.rot90(x),
                lambda x: np.rot90(x, 2),
                lambda x: np.rot90(x, 3),
                lambda x: np.fliplr(x),
                lambda x: np.flipud(x),
                lambda x: x.T
            ]
            return random.choice(transformations)(base)
        else:
            # Для больших n используем сиамский метод
            return self.siamese_method(n)
    
    def calculate_magic_constant(self, n):
        """Вычисляет магическую константу для квадрата n×n"""
        return n * (n * n + 1) // 2
    
    def display_magic_square(self, square, size):
        """Отображает магический квадрат"""
        if square is None:
            st.error("Квадрат не существует")
            return
            
        # Создаем красивый DataFrame
        df = pd.DataFrame(square)
        st.dataframe(df.style.format(None), use_container_width=True)
        
        # Дополнительная визуализация
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Рисуем сетку
        for i in range(size + 1):
            ax.axhline(y=i, color='black', linewidth=1)
            ax.axvline(x=i, color='black', linewidth=1)
        
        # Заполняем числами
        for i in range(size):
            for j in range(size):
                ax.text(j + 0.5, size - i - 0.5, str(square[i, j]), 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.set_title(f'Магический квадрат {size}×{size}')
        ax.axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def verify_magic_square(self, square, size):
        """Проверяет магические свойства квадрата"""
        if square is None:
            return
            
        magic_constant = self.calculate_magic_constant(size)
        
        st.markdown("#### ✅ Проверка магических свойств")
        
        # Проверяем строки
        row_sums = square.sum(axis=1)
        col_sums = square.sum(axis=0)
        diag1_sum = np.trace(square)
        diag2_sum = np.trace(np.fliplr(square))
        
        all_checks_passed = True
        
        for i, row_sum in enumerate(row_sums):
            status = "✓" if row_sum == magic_constant else "✗"
            color = "green" if row_sum == magic_constant else "red"
            st.markdown(f"<span style='color:{color}'>Строка {i+1}: {row_sum} {status}</span>", unsafe_allow_html=True)
            if row_sum != magic_constant:
                all_checks_passed = False
        
        for j, col_sum in enumerate(col_sums):
            status = "✓" if col_sum == magic_constant else "✗"
            color = "green" if col_sum == magic_constant else "red"
            st.markdown(f"<span style='color:{color}'>Столбец {j+1}: {col_sum} {status}</span>", unsafe_allow_html=True)
            if col_sum != magic_constant:
                all_checks_passed = False
        
        status = "✓" if diag1_sum == magic_constant else "✗"
        color = "green" if diag1_sum == magic_constant else "red"
        st.markdown(f"<span style='color:{color}'>Главная диагональ: {diag1_sum} {status}</span>", unsafe_allow_html=True)
        if diag1_sum != magic_constant:
            all_checks_passed = False
            
        status = "✓" if diag2_sum == magic_constant else "✗"
        color = "green" if diag2_sum == magic_constant else "red"
        st.markdown(f"<span style='color:{color}'>Побочная диагональ: {diag2_sum} {status}</span>", unsafe_allow_html=True)
        if diag2_sum != magic_constant:
            all_checks_passed = False
        
        if all_checks_passed:
            st.success("🎉 Все магические свойства выполнены!")
        else:
            st.error("❌ Квадрат не является полностью магическим")
    
    def encrypt_with_magic_square(self, text, square, size):
        """Шифрует текст с использованием магического квадрата - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        try:
            # Подготавливаем текст
            text_clean = text.upper().replace(' ', 'X')  # Заменяем пробелы на X
            max_chars = size * size
            
            if len(text_clean) > max_chars:
                text_clean = text_clean[:max_chars]
                st.warning(f"Текст обрезан до {max_chars} символов")
            elif len(text_clean) < max_chars:
                # Дополняем случайными буквами
                import string
                while len(text_clean) < max_chars:
                    text_clean += 'X'
            
            # Создаем матрицу для заполнения
            text_matrix = np.full((size, size), ' ', dtype='U1')
            
            # Получаем порядок заполнения (по возрастанию чисел в квадрате)
            flat_square = square.flatten()
            sorted_indices = np.argsort(flat_square)
            
            # Заполняем матрицу текстом в порядке возрастания чисел
            for idx, pos in enumerate(sorted_indices):
                if idx < len(text_clean):
                    i, j = pos // size, pos % size
                    text_matrix[i, j] = text_clean[idx]
            
            # Читаем построчно для получения шифротекста
            encrypted_chars = []
            for i in range(size):
                for j in range(size):
                    encrypted_chars.append(text_matrix[i, j])
            
            # Добавляем пробелы для читаемости
            result = ''.join(encrypted_chars)
            # Разбиваем на группы по 5 символов
            result_with_spaces = ' '.join([result[i:i+5] for i in range(0, len(result), 5)])
            
            return result_with_spaces
            
        except Exception as e:
            st.error(f"Ошибка в encrypt_with_magic_square: {e}")
            return f"Ошибка: {e}"
    
    def decrypt_with_magic_square(self, ciphertext, square, size):
        """Дешифрует текст, зашифрованный магическим квадратом - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        try:
            # Убираем пробелы из шифротекста
            ciphertext_clean = ciphertext.replace(' ', '').upper()
            
            if len(ciphertext_clean) != size * size:
                st.error(f"Длина текста должна быть {size*size} символов! Сейчас: {len(ciphertext_clean)}")
                return ciphertext
            
            # Создаем матрицу из шифротекста (построчное чтение)
            text_matrix = np.full((size, size), ' ', dtype='U1')
            idx = 0
            for i in range(size):
                for j in range(size):
                    if idx < len(ciphertext_clean):
                        text_matrix[i, j] = ciphertext_clean[idx]
                        idx += 1
            
            # Получаем порядок чтения (по возрастанию чисел в квадрате)
            flat_square = square.flatten()
            sorted_indices = np.argsort(flat_square)
            
            # Читаем в правильном порядке для дешифровки
            decrypted_chars = []
            for pos in sorted_indices:
                i, j = pos // size, pos % size
                decrypted_chars.append(text_matrix[i, j])
            
            result = ''.join(decrypted_chars)
            # Заменяем X обратно на пробелы
            result = result.replace('X', ' ')
            
            return result.strip()
            
        except Exception as e:
            st.error(f"Ошибка в decrypt_with_magic_square: {e}")
            return f"Ошибка: {e}"
    
    def show_filling_process(self, text, square, size):
        """Показывает процесс заполнения квадрата"""
        try:
            text_clean = text.upper().replace(' ', 'X').ljust(size*size, 'X')
            flat_square = square.flatten()
            sorted_indices = np.argsort(flat_square)
            
            # Создаем матрицу заполнения
            fill_matrix = np.full((size, size), ' ', dtype='U1')
            number_matrix = np.full((size, size), '', dtype='U10')
            
            for idx, pos in enumerate(sorted_indices):
                if idx < len(text_clean):
                    i, j = pos // size, pos % size
                    fill_matrix[i, j] = text_clean[idx]
                    number_matrix[i, j] = f"{square[i, j]}"
            
            # Отображаем процесс
            st.markdown("**Порядок заполнения (по числам):**")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Левый график: числа квадрата
            for i in range(size):
                for j in range(size):
                    ax1.text(j + 0.5, size - i - 0.5, str(square[i, j]), 
                           ha='center', va='center', fontsize=12, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
                    ax1.text(j + 0.5, size - i - 0.5, f"\n({i},{j})", 
                           ha='center', va='top', fontsize=8, color='gray')
            
            ax1.set_xlim(0, size)
            ax1.set_ylim(0, size)
            ax1.set_aspect('equal')
            ax1.set_title('Магический квадрат (числа)')
            ax1.axis('off')
            
            # Правый график: заполнение буквами
            for i in range(size):
                for j in range(size):
                    ax2.text(j + 0.5, size - i - 0.5, fill_matrix[i, j], 
                           ha='center', va='center', fontsize=14, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
                    ax2.text(j + 0.5, size - i - 0.5, f"\n{square[i, j]}", 
                           ha='center', va='top', fontsize=8, color='gray')
            
            ax2.set_xlim(0, size)
            ax2.set_ylim(0, size)
            ax2.set_aspect('equal')
            ax2.set_title('Заполнение текстом')
            ax2.axis('off')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Показываем порядок чтения
            order = [square.flatten()[i] for i in sorted_indices]
            st.info(f"**Порядок чтения чисел:** {', '.join(map(str, order))}")
            
        except Exception as e:
            st.error(f"Ошибка в show_filling_process: {e}")
    
    def show_examples(self):
        """Показывает примеры работы шифра"""
        st.markdown("#### 🧪 Примеры шифрования")
        
        examples = [
            {"text": "HELLO", "size": 3},
            {"text": "SECRET MESSAGE", "size": 4},
            {"text": "CRYPTOGRAPHY", "size": 4}
        ]
        
        for example in examples:
            with st.expander(f"Пример: '{example['text']}' с квадратом {example['size']}×{example['size']}"):
                try:
                    square = self.generate_magic_square(example['size'], "Ло Шу (3×3)" if example['size'] == 3 else "Сиамский метод (только нечетные)")
                    encrypted = self.encrypt_with_magic_square(example['text'], square, example['size'])
                    decrypted = self.decrypt_with_magic_square(encrypted.replace(' ', ''), square, example['size'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Оригинал", example['text'])
                    with col2:
                        st.metric("Зашифровано", encrypted[:20] + "..." if len(encrypted) > 20 else encrypted)
                    with col3:
                        st.metric("Дешифровано", decrypted)
                    
                    if example['text'].upper().replace(' ', 'X') == decrypted.upper().replace(' ', 'X'):
                        st.success("✅ Шифрование работает корректно!")
                    else:
                        st.error("❌ Ошибка в шифровании!")
                        
                except Exception as e:
                    st.error(f"Ошибка в примере: {e}")

# Необходимый импорт
import matplotlib.pyplot as plt