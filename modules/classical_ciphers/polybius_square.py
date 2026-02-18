from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import string

class PolybiusSquareModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Полибианский квадрат"
        self.description = "Шифрование с использованием квадратной таблицы замены"
        self.category = "classical"
        self.icon = ""
        self.order = 3
    
    def render(self):
        st.title("Полибианский квадрат")
        st.subheader("Древнегреческий шифр замены с координатной системой")
        
        # Теоретическая справка
        with st.expander("Теоретическая справка", expanded=False):
            st.markdown("""
            ### Полибианский квадрат (2 век до н.э.)
            
            **Исторический контекст:**
            - Изобретен древнегреческим историком Полибием
            - Использовался для передачи сообщений с помощью факелов
            - Один из первых примеров кодирования информации
            
            **Принцип работы:**
            1. Буквы алфавита размещаются в квадратной таблице
            2. Каждая буква кодируется координатами (строка, столбец)
            3. Шифрование: буква → координаты
            4. Дешифрование: координаты → буква
            
            **Классический вариант (5×5 для латинского алфавита):**
            - 25 ячеек для 26 букв (I и J объединены)
            - Координаты от 1 до 5 или с использованием букв
            
            **Преимущества:**
            - Простота реализации
            - Удобство для ручного использования
            - Может адаптироваться для разных алфавитов
            """)
        
        # Выбор языка и типа квадрата
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.radio(
                "Выберите язык алфавита:",
                ["Английский", "Русский"],
                index=0,
                horizontal=True
            )
            
            square_type = st.radio(
                "Тип квадрата:",
                ["Классический 5×5", "Прямоугольный 6×5", "Произвольный ключ"],
                index=0
            )
        
        with col2:
            st.markdown("#### Настройки шифрования")
            
            if square_type == "Произвольный ключ":
                custom_key = st.text_input(
                    "Ключевое слово:",
                    "CRYPTO",
                    help="Слово для построения квадрата (буквы не будут повторяться)"
                )
            else:
                custom_key = ""
            
            # Выбор системы координат
            coordinate_system = st.radio(
                "Система координат:",
                ["Цифры (1-5)", "Буквы", "Символы"],
                index=0
            )
        
        # Создаем квадрат Полибия
        square, alphabet = self.create_polybius_square(language, square_type, custom_key)
        
        # Показываем квадрат
        self.display_polybius_square(square, coordinate_system)
        
        # Шифрование и дешифрование
        st.markdown("---")
        self.render_encryption_decryption(square, alphabet, coordinate_system, language)
        
        # Дополнительные возможности
        st.markdown("---")
        self.render_additional_features(square, alphabet, coordinate_system)
    
    def create_polybius_square(self, language, square_type, custom_key=""):
        """Создает квадрат Полибия для выбранных параметров"""
        if language == "Английский":
            # Английский алфавит (I и J в одной ячейке в классическом варианте)
            base_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if square_type == "Классический 5×5":
                # Объединяем I и J
                alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
                square_size = (5, 5)
            else:  # Прямоугольный 6×5
                alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[:30]
                square_size = (6, 5)
        else:  # Русский
            base_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
            if square_type == "Классический 5×5":
                # Берем 25 букв (исключаем редкие)
                alphabet = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭ"[:25]
                square_size = (5, 5)
            else:  # Прямоугольный 6×5
                alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789"[:30]
                square_size = (6, 5)
        
        # Если задан произвольный ключ
        if square_type == "Произвольный ключ" and custom_key:
            # Убираем повторяющиеся буквы из ключа
            key_chars = []
            for char in custom_key.upper():
                if char in base_alphabet and char not in key_chars:
                    key_chars.append(char)
            
            # Добавляем оставшиеся буквы алфавита
            for char in base_alphabet:
                if char not in key_chars:
                    key_chars.append(char)
            
            alphabet = ''.join(key_chars)
            # Обрезаем до нужного размера
            if len(alphabet) > 25 and square_type == "Классический 5×5":
                alphabet = alphabet[:25]
            elif len(alphabet) > 30:
                alphabet = alphabet[:30]
        
        # Создаем квадрат
        rows, cols = square_size
        square = []
        index = 0
        
        for i in range(rows):
            row = []
            for j in range(cols):
                if index < len(alphabet):
                    row.append(alphabet[index])
                    index += 1
                else:
                    row.append('')
            square.append(row)
        
        return square, alphabet
    
    def display_polybius_square(self, square, coordinate_system):
        """Отображает квадрат Полибия"""
        st.markdown("### Квадрат Полибия")
        
        rows = len(square)
        cols = len(square[0])
        
        # Создаем DataFrame для красивого отображения
        if coordinate_system == "Цифры (1-5)":
            columns = [str(i+1) for i in range(cols)]
            index = [str(i+1) for i in range(rows)]
        elif coordinate_system == "Буквы":
            columns = [chr(65 + i) for i in range(cols)]  # A, B, C, ...
            index = [chr(65 + i) for i in range(rows)]    # A, B, C, ...
        else:  # Символы
            symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
            columns = symbols[:cols]
            index = symbols[:rows]
        
        df = pd.DataFrame(square, columns=columns, index=index)
        
        # Стилизуем таблицу
        st.dataframe(df, use_container_width=True)
        
        # Легенда
        st.info(f"**Размер:** {rows}×{cols} | **Координаты:** {coordinate_system}")
    
    def render_encryption_decryption(self, square, alphabet, coordinate_system, language):
        """Отрисовывает интерфейс шифрования и дешифрования"""
        st.markdown("### Шифрование и дешифрование")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Шифрование")
            plaintext = st.text_area(
                "Текст для шифрования:",
                "HELLO" if language == "Английский" else "ПРИВЕТ",
                height=100,
                key="encrypt_text"
            )
            
            if st.button("Зашифровать", key="encrypt_btn"):
                if plaintext.strip():
                    encrypted = self.polybius_encrypt(plaintext, square, coordinate_system, language)
                    st.success(f"**Зашифрованный текст:**")
                    st.info(encrypted)
                    
                    # Показываем процесс шифрования
                    st.markdown("**Процесс шифрования:**")
                    self.show_encryption_process(plaintext, square, coordinate_system, language)
                else:
                    st.error("Введите текст для шифрования!")
        
        with col2:
            st.markdown("#### Дешифрование")
            ciphertext = st.text_area(
                "Текст для дешифрования:",
                "23 15 31 31 34" if language == "Английский" else "41 42 43 44 45 46",
                height=100,
                key="decrypt_text"
            )
            
            if st.button("Дешифровать", key="decrypt_btn"):
                if ciphertext.strip():
                    decrypted = self.polybius_decrypt(ciphertext, square, coordinate_system, language)
                    st.success(f"**Дешифрованный текст:**")
                    st.info(decrypted)
                else:
                    st.error("Введите текст для дешифрования!")
    
    def polybius_encrypt(self, text, square, coordinate_system, language):
        """Шифрует текст с помощью квадрата Полибия"""
        text_clean = self.prepare_text(text, language, for_encryption=True)
        encrypted_parts = []
        
        for char in text_clean:
            if char == ' ':  # Пробелы сохраняем
                encrypted_parts.append(' ')
                continue
            
            # Ищем символ в квадрате
            found = False
            for i, row in enumerate(square):
                for j, cell in enumerate(row):
                    if cell == char:
                        # Кодируем координаты
                        if coordinate_system == "Цифры (1-5)":
                            code = f"{i+1}{j+1}"
                        elif coordinate_system == "Буквы":
                            code = f"{chr(65+i)}{chr(65+j)}"
                        else:  # Символы
                            symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
                            code = f"{symbols[i]}{symbols[j]}"
                        
                        encrypted_parts.append(code)
                        found = True
                        break
                if found:
                    break
            
            if not found:
                encrypted_parts.append(char)  # Оставляем непонятные символы как есть
        
        return ' '.join(encrypted_parts)
    
    def polybius_decrypt(self, ciphertext, square, coordinate_system, language):
        """Дешифрует текст, зашифрованный квадратом Полибия"""
        decrypted_parts = []
        
        # Разбиваем на коды (учитываем разные разделители)
        if ' ' in ciphertext:
            codes = ciphertext.split()
        else:
            # Если нет пробелов, разбиваем по парам символов
            codes = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        
        for code in codes:
            if code == ' ':  # Пробелы
                decrypted_parts.append(' ')
                continue
            
            if len(code) != 2:  # Неправильный код
                decrypted_parts.append(code)
                continue
            
            try:
                # Декодируем координаты
                if coordinate_system == "Цифры (1-5)":
                    row = int(code[0]) - 1
                    col = int(code[1]) - 1
                elif coordinate_system == "Буквы":
                    row = ord(code[0].upper()) - 65
                    col = ord(code[1].upper()) - 65
                else:  # Символы
                    symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
                    row = symbols.index(code[0])
                    col = symbols.index(code[1])
                
                # Получаем символ из квадрата
                if 0 <= row < len(square) and 0 <= col < len(square[0]):
                    char = square[row][col]
                    if char:  # Если ячейка не пустая
                        decrypted_parts.append(char)
                    else:
                        decrypted_parts.append('?')  # Неизвестный символ
                else:
                    decrypted_parts.append('?')  # Неправильные координаты
                    
            except (ValueError, IndexError):
                decrypted_parts.append(code)  # Оставляем как есть при ошибке
        
        return ''.join(decrypted_parts)
    
    def prepare_text(self, text, language, for_encryption=True):
        """Подготавливает текст для шифрования/дешифрования"""
        text_upper = text.upper()
        
        if language == "Английский":
            # Оставляем только буквы, заменяем J на I при шифровании
            if for_encryption:
                result = ''.join([char if char != 'J' else 'I' for char in text_upper if char.isalpha() or char == ' '])
            else:
                result = ''.join([char for char in text_upper if char.isalpha() or char == ' '])
        else:  # Русский
            russian_letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
            result = ''.join([char for char in text_upper if char in russian_letters or char == ' '])
        
        return result
    
    def show_encryption_process(self, plaintext, square, coordinate_system, language):
        """Показывает подробный процесс шифрования"""
        text_clean = self.prepare_text(plaintext, language, for_encryption=True)
        
        process_data = []
        for char in text_clean:
            if char == ' ':
                process_data.append({
                    'Символ': '␣',
                    'Координаты': 'Пробел',
                    'Код': '␣'
                })
                continue
            
            # Ищем символ в квадрате
            found = False
            for i, row in enumerate(square):
                for j, cell in enumerate(row):
                    if cell == char:
                        # Кодируем координаты
                        if coordinate_system == "Цифры (1-5)":
                            row_code = i + 1
                            col_code = j + 1
                            code = f"{row_code}{col_code}"
                        elif coordinate_system == "Буквы":
                            row_code = chr(65 + i)
                            col_code = chr(65 + j)
                            code = f"{row_code}{col_code}"
                        else:  # Символы
                            symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
                            row_code = symbols[i]
                            col_code = symbols[j]
                            code = f"{row_code}{col_code}"
                        
                        process_data.append({
                            'Символ': char,
                            'Координаты': f"({row_code}, {col_code})",
                            'Код': code
                        })
                        found = True
                        break
                if found:
                    break
            
            if not found:
                process_data.append({
                    'Символ': char,
                    'Координаты': 'Не найден',
                    'Код': char
                })
        
        if process_data:
            st.dataframe(pd.DataFrame(process_data), use_container_width=True, hide_index=True)
    
    def render_additional_features(self, square, alphabet, coordinate_system):
        """Дополнительные возможности модуля"""
        st.markdown("### Дополнительные возможности")
        
        tab1, tab2, tab3 = st.tabs(["Анализ квадрата", "Интерактивная карта", "Исторический контекст"])
        
        with tab1:
            self.analyze_square(square, alphabet)
        
        with tab2:
            self.interactive_square_map(square, coordinate_system)
        
        with tab3:
            self.historical_context()
    
    def analyze_square(self, square, alphabet):
        """Анализирует свойства квадрата Полибия"""
        st.markdown("#### Анализ квадрата Полибия")
        
        rows = len(square)
        cols = len(square[0])
        total_cells = rows * cols
        used_cells = sum(1 for row in square for cell in row if cell != '')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Размер", f"{rows}×{cols}")
        with col2:
            st.metric("Всего ячеек", total_cells)
        with col3:
            st.metric("Использовано", used_cells)
        with col4:
            efficiency = (used_cells / total_cells) * 100
            st.metric("Эффективность", f"{efficiency:.1f}%")
        
        # Частотный анализ алфавита
        st.markdown("##### Частотный анализ")
        
        # Создаем "частотное распределение" по позициям в квадрате
        position_data = []
        for i, row in enumerate(square):
            for j, cell in enumerate(row):
                if cell:
                    position_data.append({
                        'Буква': cell,
                        'Строка': i + 1,
                        'Столбец': j + 1,
                        'Позиция': f"({i+1},{j+1})"
                    })
        
        st.dataframe(pd.DataFrame(position_data), use_container_width=True, hide_index=True)
        
        # Визуализация распределения
        fig, ax = plt.subplots(figsize=(10, 6))
        
        letters = [data['Буква'] for data in position_data]
        x_pos = [data['Столбец'] for data in position_data]
        y_pos = [data['Строка'] for data in position_data]
        
        scatter = ax.scatter(x_pos, y_pos, s=100, c=range(len(letters)), cmap='viridis', alpha=0.7)
        
        # Добавляем подписи
        for i, (letter, x, y) in enumerate(zip(letters, x_pos, y_pos)):
            ax.text(x, y, letter, ha='center', va='center', fontweight='bold', fontsize=12)
        
        ax.set_xlabel('Столбец')
        ax.set_ylabel('Строка')
        ax.set_title('Распределение букв в квадрате Полибия')
        ax.set_xticks(range(1, cols + 1))
        ax.set_yticks(range(1, rows + 1))
        ax.grid(True, alpha=0.3)
        ax.invert_yaxis()  # Чтобы первая строка была сверху
        
        st.pyplot(fig)
    
    def interactive_square_map(self, square, coordinate_system):
        """Интерактивная карта квадрата - упрощенная версия для Streamlit"""
        st.markdown("#### Интерактивная карта квадрата (работает некорректно)")
        
        st.info("Нажмите на ячейку, чтобы увидеть её координаты")
        
        rows = len(square)
        cols = len(square[0])
        
        # Создаем координаты для заголовков
        if coordinate_system == "Цифры (1-5)":
            col_headers = [str(i+1) for i in range(cols)]
            row_headers = [str(i+1) for i in range(rows)]
        elif coordinate_system == "Буквы":
            col_headers = [chr(65 + i) for i in range(cols)]
            row_headers = [chr(65 + i) for i in range(rows)]
        else:  # Символы
            symbols = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩']
            col_headers = symbols[:cols]
            row_headers = symbols[:rows]
        
        # Создаем интерактивную таблицу с помощью Streamlit
        st.markdown("##### Карта квадрата (нажмите на ячейку)")
        
        # Отображаем заголовки столбцов
        col_header_str = "| | " + " | ".join(col_headers) + " |"
        separator_str = "|-|" + "|".join(["---"] * cols) + "|"
        
        table_lines = [col_header_str, separator_str]
        
        # Создаем строки таблицы
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                cell_content = square[i][j] if square[i][j] else ' '
                # Создаем кнопку для каждой ячейки
                button_key = f"cell_{i}_{j}"
                if st.button(cell_content, key=button_key, 
                            help=f"Координаты: ({row_headers[i]}, {col_headers[j]})"):
                    # Сохраняем выбранную ячейку в session_state
                    st.session_state.selected_cell = {
                        'row': i,
                        'col': j,
                        'row_header': row_headers[i],
                        'col_header': col_headers[j],
                        'letter': cell_content
                    }
                row_cells.append(cell_content)
            
            row_str = f"| **{row_headers[i]}** | " + " | ".join(row_cells) + " |"
            table_lines.append(row_str)
        
        # Отображаем таблицу в markdown
        st.markdown("\n".join(table_lines))
        
        # Показываем информацию о выбранной ячейке
        if 'selected_cell' in st.session_state:
            cell = st.session_state.selected_cell
            st.success(
                f"**Выбрана ячейка:** "
                f"Координаты ({cell['row_header']}, {cell['col_header']}) → "
                f"Буква '{cell['letter']}'"
            )
        
        # Альтернативный способ: выбор через selectbox
        st.markdown("---")
        st.markdown("##### Поиск по координатам")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_row = st.selectbox(
                "Выберите строку:",
                options=list(range(rows)),
                format_func=lambda x: f"{row_headers[x]} (строка {x+1})",
                key="row_select"
            )
        
        with col2:
            selected_col = st.selectbox(
                "Выберите столбец:",
                options=list(range(cols)),
                format_func=lambda x: f"{col_headers[x]} (столбец {x+1})",
                key="col_select"
            )
        
        # Показываем результат выбора
        letter = square[selected_row][selected_col]
        if letter:
            st.info(
                f"**Результат:** Координаты ({row_headers[selected_row]}, "
                f"{col_headers[selected_col]}) → Буква **'{letter}'**"
            )
            
            # Показываем визуальное выделение
            st.markdown("##### Визуальное выделение выбранной ячейки")
            
            # Создаем визуализацию с выделением
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Рисуем сетку
            for i in range(rows + 1):
                ax.axhline(y=i, color='black', linewidth=1)
            for j in range(cols + 1):
                ax.axvline(x=j, color='black', linewidth=1)
            
            # Заполняем ячейки
            for i in range(rows):
                for j in range(cols):
                    # Выделяем выбранную ячейку
                    if i == selected_row and j == selected_col:
                        facecolor = 'lightgreen'
                        edgecolor = 'red'
                        linewidth = 3
                    else:
                        facecolor = 'lightblue'
                        edgecolor = 'black'
                        linewidth = 1
                    
                    rect = plt.Rectangle((j, rows-i-1), 1, 1, 
                                    facecolor=facecolor, edgecolor=edgecolor, 
                                    linewidth=linewidth)
                    ax.add_patch(rect)
                    
                    # Добавляем букву
                    if square[i][j]:
                        ax.text(j + 0.5, rows-i-0.5, square[i][j], 
                            ha='center', va='center', fontsize=16, fontweight='bold')
            
            # Добавляем подписи осей
            for i, header in enumerate(row_headers):
                ax.text(-0.3, rows-i-0.5, header, ha='center', va='center', 
                    fontsize=12, fontweight='bold')
            
            for j, header in enumerate(col_headers):
                ax.text(j + 0.5, rows + 0.3, header, ha='center', va='center', 
                    fontsize=12, fontweight='bold')
            
            ax.set_xlim(-0.5, cols + 0.5)
            ax.set_ylim(-0.5, rows + 0.5)
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Выбранная ячейка: ({row_headers[selected_row]}, {col_headers[selected_col]}) → "{letter}"')
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Выбранная ячейка пуста")
    
    def historical_context(self):
        """Исторический контекст Полибианского квадрата"""
        st.markdown("#### Исторический контекст")
        
        st.markdown("""
        **Древнегреческая криптография:**
        
        **Полибий (ок. 200-118 до н.э.)** - греческий историк, разработал систему передачи 
        сообщений на расстоянии с помощью факелов.
        
        **Система передачи:**
        ```
        Акрополь              Другой холм
           ↑                       ↑
        Факелы: ЛЕВЫЙ-ПРАВЫЙ   Наблюдатель
         1-2-3-4-5             Записывает цифры
        ```
        
        **Процесс передачи:**
        1. Сообщение кодировалось в цифры (11, 23, 45...)
        2. Левым факелом показывали номер строки
        3. Правым факелом - номер столбца
        4. Наблюдатель записывал координаты и декодировал сообщение
        
        **Значение в истории:**
        - Один из первых примеров телеграфной связи
        - Предшественник современных систем кодирования
        - Демонстрация принципов координатных систем
        
        **Современное применение:**
        - Образовательные цели в криптографии
        - Основы для более сложных шифров (ADFGVX)
        - Игры и головоломки
        """)
        
        # Визуализация древнегреческой системы
        st.markdown("##### Визуализация древнегреческой системы")
        
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Рисуем схему передачи
        ax.plot([1, 5], [1, 1], 'k-', linewidth=2, label='Линия связи')
        ax.scatter([1, 5], [1, 1], s=200, c=['red', 'blue'], alpha=0.7)
        
        # Подписи
        ax.text(1, 0.8, 'Отправитель\n(2 факела)', ha='center', va='top', fontsize=10)
        ax.text(5, 0.8, 'Получатель', ha='center', va='top', fontsize=10)
        ax.text(3, 1.2, 'Координатная\nпередача', ha='center', va='bottom', fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
        
        # Пример передачи
        ax.annotate('Левый факел: 2', xy=(1, 1), xytext=(0.5, 1.5),
                   arrowprops=dict(arrowstyle='->', color='red'), fontsize=9)
        ax.annotate('Правый факел: 3', xy=(1, 1), xytext=(1.5, 1.5),
                   arrowprops=dict(arrowstyle='->', color='blue'), fontsize=9)
        
        ax.set_xlim(0, 6)
        ax.set_ylim(0.5, 1.8)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Древнегреческая система передачи сообщений Полибия')
        
        plt.tight_layout()
        st.pyplot(fig)

# Необходимый импорт для визуализации
import matplotlib.pyplot as plt