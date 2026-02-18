from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class MasonicCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Масонов"
        self.description = "Визуальный шифр с использованием решеток и символов"
        self.category = "classical"
        self.icon = ""
        self.order = 4
    
    def render(self):
        st.title("Шифр Масонов (Pigpen Cipher)")
        st.subheader("Визуальный шифр с решетками и точками")
        
        # Теоретическая справка
        with st.expander("Теоретическая справка", expanded=False):
            st.markdown("""
            ### Шифр Масонов (Pigpen Cipher)
            
            **Исторический контекст:**
            - Также известен как шифр "свинарник" (Pigpen)
            - Использовался масонами в 18 веке для секретной переписки
            - Простой визуальный шифр, основанный на замене символов
            
            **Принцип работы:**
            1. Алфавит размещается в двух решетках 3×3 (всего 26 букв + дополнительные символы)
            2. Каждая буква кодируется символом угла, в котором она находится
            3. Точка показывает, в какой из двух решеток находится буква
            
            **Структура решеток:**
            ```
            Решетка 1 (без точки)    Решетка 2 (с точкой)
              A B C                    J K L
              D E F                    M N O  
              G H I                    P Q R
                    
            Решетка 3 (без точки)    Решетка 4 (с точкой)
              S T U                    W X Y
              V W X                    Z ? !
              Y Z ?                    . , :
            ```
            
            **Преимущества:**
            - Простота запоминания и использования
            - Визуальная природа делает его интересным
            - Хорошо подходит для ручного шифрования
            
            **Недостатки:**
            - Легко взламывается частотным анализом
            - Ограниченный алфавит
            """)
        
        # Выбор языка и типа шифра
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.radio(
                "Выберите язык алфавита:",
                ["Английский", "Русский"],
                index=0,
                horizontal=True
            )
            
            cipher_variant = st.radio(
                "Вариант шифра:",
                ["Классический (4 решетки)", "Упрощенный (2 решетки)", "Символьный"],
                index=0
            )
        
        with col2:
            st.markdown("#### Настройки отображения")
            show_grids = st.checkbox("Показать решетки", value=True)
            interactive_mode = st.checkbox("Интерактивный режим", value=True)
        
        # Создаем решетки Масонов
        grids = self.create_masonic_grids(language, cipher_variant)
        
        # Показываем решетки
        if show_grids:
            self.display_masonic_grids(grids, cipher_variant, language)
        
        # Шифрование и дешифрование
        st.markdown("---")
        self.render_encryption_decryption(grids, language, cipher_variant)
        
        # Интерактивный режим
        if interactive_mode:
            st.markdown("---")
            self.render_interactive_mode(grids, language, cipher_variant)
        
        # Исторический контекст
        st.markdown("---")
        self.render_historical_context()
    
    def create_masonic_grids(self, language, variant):
        """Создает решетки Масонов для выбранных параметров"""
        grids = {}
        
        if language == "Английский":
            if variant == "Классический (4 решетки)":
                # 4 решетки 3×3 для 26 букв + символы
                grids['grid1'] = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
                grids['grid2'] = [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'Q', 'R']]
                grids['grid3'] = [['S', 'T', 'U'], ['V', 'W', 'X'], ['Y', 'Z', '?']]
                grids['grid4'] = [['!', '"', '#'], ['$', '%', '&'], ['(', ')', '*']]
            elif variant == "Упрощенный (2 решетки)":
                # 2 решетки 3×3 для основных букв
                grids['grid1'] = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
                grids['grid2'] = [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'Q', 'R']]
                grids['grid3'] = [['S', 'T', 'U'], ['V', 'W', 'X'], ['Y', 'Z', '.']]
            else:  # Символьный
                grids['grid1'] = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
                grids['grid2'] = [['⌖', '⚚', '☩'], ['♁', '☉', '☿'], ['♀', '♃', '♄']]
        else:  # Русский
            if variant == "Классический (4 решетки)":
                grids['grid1'] = [['А', 'Б', 'В'], ['Г', 'Д', 'Е'], ['Ё', 'Ж', 'З']]
                grids['grid2'] = [['И', 'Й', 'К'], ['Л', 'М', 'Н'], ['О', 'П', 'Р']]
                grids['grid3'] = [['С', 'Т', 'У'], ['Ф', 'Х', 'Ц'], ['Ч', 'Ш', 'Щ']]
                grids['grid4'] = [['Ъ', 'Ы', 'Ь'], ['Э', 'Ю', 'Я'], ['.', ',', '!']]
            elif variant == "Упрощенный (2 решетки)":
                grids['grid1'] = [['А', 'Б', 'В'], ['Г', 'Д', 'Е'], ['Ж', 'З', 'И']]
                grids['grid2'] = [['Й', 'К', 'Л'], ['М', 'Н', 'О'], ['П', 'Р', 'С']]
                grids['grid3'] = [['Т', 'У', 'Ф'], ['Х', 'Ц', 'Ч'], ['Ш', 'Щ', 'Ъ']]
            else:  # Символьный
                grids['grid1'] = [['А', 'Б', 'В'], ['Г', 'Д', 'Е'], ['Ё', 'Ж', 'З']]
                grids['grid2'] = [['⌖', '⚚', '☩'], ['♁', '☉', '☿'], ['♀', '♃', '♄']]
        
        return grids
    
    def display_masonic_grids(self, grids, variant, language):
        """Отображает решетки Масонов"""
        st.markdown("### Решетки Масонов")
        
        num_grids = len(grids)
        cols = 2  # Показываем по 2 решетки в строке
        
        # Создаем визуализацию решеток
        fig, axes = plt.subplots((num_grids + 1) // cols, cols, figsize=(12, 4 * ((num_grids + 1) // cols)))
        
        if num_grids == 1:
            axes = np.array([axes])
        
        axes = axes.flatten()
        
        for idx, (grid_name, grid) in enumerate(grids.items()):
            ax = axes[idx]
            self.draw_masonic_grid(ax, grid, grid_name, idx, variant)
        
        # Скрываем лишние subplots
        for idx in range(len(grids), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Легенда
        st.markdown("#### Легенда символов")
        
        if variant == "Символьный":
            st.info("""
            **Символы Масонов:**
            - ⌖ - Цель (Purpose)
            - ⚚ - Весы (Balance)  
            - ☩ - Иерусалимский крест (Jerusalem Cross)
            - ♁ - Земля (Earth)
            - ☉ - Солнце (Sun)
            - ☿ - Меркурий (Mercury)
            - ♀ - Венера (Venus)
            - ♃ - Юпитер (Jupiter)
            - ♄ - Сатурн (Saturn)
            """)
        else:
            st.info("""
            **Система кодирования:**
            - **Решетки 1 и 3**: Буквы без точек
            - **Решетки 2 и 4**: Буквы с точками в центре
            - **Позиция в решетке**: Определяет форму символа
            """)
    
    def draw_masonic_grid(self, ax, grid, grid_name, grid_index, variant):
        """Рисует одну решетку Масонов"""
        rows, cols = len(grid), len(grid[0])
        
        # Рисуем решетку
        for i in range(rows + 1):
            ax.axhline(y=i, color='black', linewidth=2)
        for j in range(cols + 1):
            ax.axvline(x=j, color='black', linewidth=2)
        
        # Заполняем ячейки
        for i in range(rows):
            for j in range(cols):
                # Рисуем символ Масонов
                self.draw_masonic_symbol(ax, j + 0.5, rows - i - 0.5, grid_index, i, j)
                
                # Добавляем букву
                if grid[i][j]:
                    ax.text(j + 0.5, rows - i - 0.5, grid[i][j], 
                           ha='center', va='center', fontsize=14, fontweight='bold',
                           bbox=dict(boxstyle="circle,pad=0.3", facecolor="white", alpha=0.8))
        
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect('equal')
        ax.set_title(f'Решетка {grid_index + 1}')
        ax.axis('off')
    
    def draw_masonic_symbol(self, ax, x, y, grid_index, row, col):
        """Рисует символ Масонов для данной позиции"""
        # Определяем тип символа на основе позиции в решетке
        symbol_type = (row, col)
        
        # Цвет в зависимости от решетки
        colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow']
        color = colors[grid_index % len(colors)]
        
        # Рисуем базовый квадрат
        size = 0.4
        ax.add_patch(plt.Rectangle((x - size/2, y - size/2), size, size, 
                                 facecolor=color, alpha=0.3, edgecolor='black'))
        
        # Рисуем углы в зависимости от позиции
        corner_size = 0.15
        
        if symbol_type == (0, 0):  # Верхний левый
            self.draw_corner(ax, x - size/2, y + size/2, 'top-left', corner_size)
        elif symbol_type == (0, 1):  # Верхний средний
            self.draw_line(ax, x - size/2, y + size/2, x + size/2, y + size/2, corner_size)
        elif symbol_type == (0, 2):  # Верхний правый
            self.draw_corner(ax, x + size/2, y + size/2, 'top-right', corner_size)
        elif symbol_type == (1, 0):  # Средний левый
            self.draw_line(ax, x - size/2, y + size/2, x - size/2, y - size/2, corner_size)
        elif symbol_type == (1, 1):  # Центр
            # Для центральной позиции рисуем точку если это решетка 2 или 4
            if grid_index % 2 == 1:  # Решетки 2 и 4 имеют точки
                ax.plot(x, y, 'ko', markersize=8)
            else:
                ax.plot(x, y, 'ko', markersize=3, alpha=0.5)
        elif symbol_type == (1, 2):  # Средний правый
            self.draw_line(ax, x + size/2, y + size/2, x + size/2, y - size/2, corner_size)
        elif symbol_type == (2, 0):  # Нижний левый
            self.draw_corner(ax, x - size/2, y - size/2, 'bottom-left', corner_size)
        elif symbol_type == (2, 1):  # Нижний средний
            self.draw_line(ax, x - size/2, y - size/2, x + size/2, y - size/2, corner_size)
        elif symbol_type == (2, 2):  # Нижний правый
            self.draw_corner(ax, x + size/2, y - size/2, 'bottom-right', corner_size)
    
    def draw_corner(self, ax, x, y, corner_type, size):
        """Рисует угол"""
        if corner_type == 'top-left':
            ax.plot([x, x + size], [y, y], 'k-', linewidth=2)
            ax.plot([x, x], [y, y - size], 'k-', linewidth=2)
        elif corner_type == 'top-right':
            ax.plot([x - size, x], [y, y], 'k-', linewidth=2)
            ax.plot([x, x], [y, y - size], 'k-', linewidth=2)
        elif corner_type == 'bottom-left':
            ax.plot([x, x + size], [y, y], 'k-', linewidth=2)
            ax.plot([x, x], [y, y + size], 'k-', linewidth=2)
        elif corner_type == 'bottom-right':
            ax.plot([x - size, x], [y, y], 'k-', linewidth=2)
            ax.plot([x, x], [y, y + size], 'k-', linewidth=2)
    
    def draw_line(self, ax, x1, y1, x2, y2, width):
        """Рисует линию"""
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=width*10)
    
    def render_encryption_decryption(self, grids, language, variant):
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
                    encrypted = self.masonic_encrypt(plaintext, grids, language, variant)
                    st.success("**Зашифрованный текст:**")
                    st.info(encrypted)
                    
                    # Показываем процесс шифрования
                    st.markdown("**Процесс шифрования:**")
                    self.show_encryption_process(plaintext, grids, language, variant)
                else:
                    st.error("Введите текст для шифрования!")
        
        with col2:
            st.markdown("#### Дешифрование")
            ciphertext = st.text_area(
                "Текст для дешифрования:",
                "◸ ◹ ◺ ◺ ◻" if language == "Английский" else "◸ ◹ ◺ ◺ ◻",
                height=100,
                key="decrypt_text"
            )
            
            if st.button("Дешифровать", key="decrypt_btn"):
                if ciphertext.strip():
                    decrypted = self.masonic_decrypt(ciphertext, grids, language, variant)
                    st.success("**Дешифрованный текст:**")
                    st.info(decrypted)
                else:
                    st.error("Введите текст для дешифрования!")
    
    def masonic_encrypt(self, text, grids, language, variant):
        """Шифрует текст шифром Масонов"""
        text_upper = text.upper()
        encrypted_parts = []
        
        # Создаем mapping из решеток
        mapping = self.create_mapping_from_grids(grids)
        
        for char in text_upper:
            if char == ' ':
                encrypted_parts.append(' ')
                continue
            
            if char in mapping:
                encrypted_parts.append(mapping[char])
            else:
                encrypted_parts.append(char)  # Оставляем непонятные символы как есть
        
        return ' '.join(encrypted_parts)
    
    def masonic_decrypt(self, ciphertext, grids, language, variant):
        """Дешифрует текст, зашифрованный шифром Масонов"""
        # Создаем обратное mapping
        mapping = self.create_mapping_from_grids(grids)
        reverse_mapping = {v: k for k, v in mapping.items()}
        
        # Разбиваем на символы
        symbols = ciphertext.split()
        decrypted_parts = []
        
        for symbol in symbols:
            if symbol == ' ':
                decrypted_parts.append(' ')
                continue
            
            if symbol in reverse_mapping:
                decrypted_parts.append(reverse_mapping[symbol])
            else:
                decrypted_parts.append('?')  # Неизвестный символ
        
        return ''.join(decrypted_parts)
    
    def create_mapping_from_grids(self, grids):
        """Создает mapping букв на символы Масонов из решеток"""
        mapping = {}
        mason_symbols = ['◸', '◹', '◺', '◻', '◼', '◽', '◾', '▢', '▣']
        
        symbol_idx = 0
        for grid_name, grid in grids.items():
            grid_index = int(grid_name[-1]) - 1  # grid1 -> 0, grid2 -> 1, etc.
            
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] and symbol_idx < len(mason_symbols):
                        mapping[grid[i][j]] = mason_symbols[symbol_idx]
                        symbol_idx += 1
        
        return mapping
    
    def show_encryption_process(self, plaintext, grids, language, variant):
        """Показывает подробный процесс шифрования"""
        text_upper = plaintext.upper()
        mapping = self.create_mapping_from_grids(grids)
        
        process_data = []
        for char in text_upper:
            if char == ' ':
                process_data.append({
                    'Символ': '␣',
                    'Символ Масонов': 'Пробел',
                    'Решетка': '-'
                })
                continue
            
            if char in mapping:
                # Находим в какой решетке символ
                grid_info = self.find_char_in_grids(char, grids)
                process_data.append({
                    'Символ': char,
                    'Символ Масонов': mapping[char],
                    'Решетка': grid_info
                })
            else:
                process_data.append({
                    'Символ': char,
                    'Символ Масонов': char,
                    'Решетка': 'Не найден'
                })
        
        if process_data:
            st.dataframe(pd.DataFrame(process_data), use_container_width=True, hide_index=True)
    
    def find_char_in_grids(self, char, grids):
        """Находит символ в решетках и возвращает информацию о его расположении"""
        for grid_name, grid in grids.items():
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == char:
                        grid_num = int(grid_name[-1])
                        position = f"Строка {i+1}, Столбец {j+1}"
                        return f"Решетка {grid_num} ({position})"
        return "Не найден"
    
    def render_interactive_mode(self, grids, language, variant):
        """Интерактивный режим изучения шифра"""
        st.markdown("### Интерактивный режим")
        
        st.info("Выберите букву чтобы увидеть её представление в шифре Масонов")
        
        # Создаем список всех букв из решеток
        all_letters = []
        for grid in grids.values():
            for row in grid:
                for cell in row:
                    if cell and cell not in all_letters:
                        all_letters.append(cell)
        
        if all_letters:
            selected_letter = st.selectbox("Выберите букву:", sorted(all_letters))
            
            # Показываем информацию о выбранной букве
            mapping = self.create_mapping_from_grids(grids)
            grid_info = self.find_char_in_grids(selected_letter, grids)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Буква", selected_letter)
            
            with col2:
                if selected_letter in mapping:
                    st.metric("Символ Масонов", mapping[selected_letter])
                else:
                    st.metric("Символ Масонов", "Не найден")
            
            with col3:
                st.metric("Расположение", grid_info.split('(')[0].strip())
            
            # Визуализация выбранной буквы
            st.markdown("#### Визуализация символа")
            self.visualize_single_symbol(selected_letter, grids, mapping)
    
    def visualize_single_symbol(self, letter, grids, mapping):
        """Визуализирует одиночный символ Масонов"""
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # Находим позицию буквы в решетках
        found = False
        for grid_name, grid in grids.items():
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == letter:
                        grid_index = int(grid_name[-1]) - 1
                        self.draw_masonic_symbol(ax, 0.5, 0.5, grid_index, i, j)
                        found = True
                        break
                if found:
                    break
            if found:
                break
        
        if letter in mapping:
            ax.text(0.5, 0.5, letter, ha='center', va='center', 
                   fontsize=20, fontweight='bold',
                   bbox=dict(boxstyle="circle,pad=0.3", facecolor="yellow", alpha=0.8))
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_title(f'Символ для буквы "{letter}"')
        ax.axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def render_historical_context(self):
        """Исторический контекст шифра Масонов"""
        st.markdown("### Исторический контекст")
        
        st.markdown("""
        **Масонство и криптография:**
        
        **Масонство** - это братская организация, возникшая в конце 16 - начале 17 веков.
        Масоны использовали различные символы и шифры для:
        
        - **Идентификации членов** - распознавание "своих"
        - **Секретной переписки** - защита внутренних дел
        - **Ритуалов и церемоний** - символические значения
        
        **Шифр Pigpen (Свинарник):**
        - Назван так из-за внешнего вида решеток, напоминающих свинарник
        - Также известен как шифр Масонов, шифр решетки, шифр Тайного общества
        - Использовался не только масонами, но и другими тайными обществами
        
        **Символика Масонов:**
        - **Циркуль и наугольник** - символ равновесия и меры
        - **Всевидящее око** - символ божественного провидения
        - **Буква G** - геометрия, Бог (God), великий архитектор вселенной
        
        **Современное значение:**
        - Образовательный инструмент для изучения криптографии
        - Пример простого визуального шифра
        - Исторический артефакт развития криптографии
        """)
        
        # Дополнительная визуализация масонских символов
        st.markdown("#### Масонские символы")
        
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        symbols_info = [
            ('◸', 'Верхний левый угол', 'Решетка 1'),
            ('◹', 'Верхний правый угол', 'Решетка 1'), 
            ('◺', 'Нижний левый угол', 'Решетка 1'),
            ('◻', 'Нижний правый угол', 'Решетка 1'),
            ('◼', 'Центр с точкой', 'Решетка 2'),
            ('⚚', 'Весы Масонов', 'Символика')
        ]
        
        for idx, (symbol, description, grid) in enumerate(symbols_info):
            ax = axes[idx // 3, idx % 3]
            ax.text(0.5, 0.5, symbol, ha='center', va='center', fontsize=30)
            ax.set_title(f'{description}\n{grid}', fontsize=10)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)

# Необходимый импорт
import matplotlib.pyplot as plt