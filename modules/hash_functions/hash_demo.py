from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import time
import binascii
from collections import Counter
import random

class HashDemoModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Хеш-функции"
        self.description = "Целостность данных и лавинный эффект"
        self.category = "hash"
        self.icon = ""
        self.order = 1
        
        # Поддерживаемые хеш-функции
        self.hash_functions = {
            "MD5": hashlib.md5,
            "SHA-1": hashlib.sha1,
            "SHA-256": hashlib.sha256,
            "SHA-512": hashlib.sha512,
            "SHA-3-256": hashlib.sha3_256,
            "BLAKE2b": hashlib.blake2b
        }
    
    def render(self):
        st.title("📊 Хеш-функции")
        st.subheader("Целостность данных, лавинный эффект и коллизии")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Криптографические хеш-функции
            
            **Свойства идеальной хеш-функции:**
            1. **Детерминированность** - один вход всегда дает один выход
            2. **Быстрота вычисления** - быстрое вычисление для любого входа
            3. **Лавинный эффект** - малое изменение входа меняет хеш полностью
            4. **Необратимость** - невозможно восстановить вход по выходу
            5. **Устойчивость к коллизиям** - сложно найти два входа с одинаковым хешем
            
            **Применения:**
            - Проверка целостности файлов
            - Хранение паролей
            - Цифровые подписи
            - Блокчейн и криптовалюты
            
            **Известные уязвимости:**
            - MD5: коллизии находятся за секунды
            - SHA-1: практические атаки найдены
            - SHA-2/SHA-3: считаются безопасными
            """)
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔍 Сравнение хеш-функций", "🌊 Лавинный эффект", "🎯 Поиск коллизий", "🔐 Практические применения"],
            horizontal=True
        )
        
        if mode == "🔍 Сравнение хеш-функций":
            self.render_hash_comparison()
        elif mode == "🌊 Лавинный эффект":
            self.render_avalanche_effect()
        elif mode == "🎯 Поиск коллизий":
            self.render_collision_search()
        else:
            self.render_practical_uses()
    
    def render_hash_comparison(self):
        """Режим сравнения хеш-функций"""
        st.markdown("### 🔍 Сравнение хеш-функций")
        
        # Ввод данных
        input_text = st.text_area(
            "Введите текст для хеширования:",
            "Hello World!",
            height=100,
            help="Текст для демонстрации работы хеш-функций"
        )
        
        # Выбор алгоритмов для сравнения
        selected_hashes = st.multiselect(
            "Выберите хеш-функции для сравнения:",
            list(self.hash_functions.keys()),
            default=["MD5", "SHA-1", "SHA-256", "SHA-512"]
        )
        
        if st.button("🔍 Вычислить хеши", type="primary"):
            if not input_text.strip():
                st.error("Введите текст для хеширования!")
                return
            
            if not selected_hashes:
                st.error("Выберите хотя бы одну хеш-функцию!")
                return
            
            with st.spinner("Вычисляю хеши..."):
                self.show_hash_comparison(input_text, selected_hashes)
    
    def show_hash_comparison(self, input_text, selected_hashes):
        """Показывает сравнение хеш-функций"""
        st.markdown("---")
        st.markdown("## 📊 Результаты хеширования")
        
        # Таца результатов
        results = []
        performance_data = []
        
        for hash_name in selected_hashes:
            hash_func = self.hash_functions[hash_name]
            
            # Измеряем производительность
            start_time = time.time()
            hash_obj = hash_func(input_text.encode('utf-8'))
            end_time = time.time()
            
            hash_hex = hash_obj.hexdigest()
            hash_bin = bin(int(hash_hex, 16))[2:].zfill(len(hash_hex) * 4)
            hash_time = (end_time - start_time) * 1000  # в миллисекундах
            
            results.append({
                'Алгоритм': hash_name,
                'Размер выхода (бит)': len(hash_bin),
                'Хеш (HEX)': hash_hex,
                'Время (мс)': f"{hash_time:.6f}"
            })
            
            performance_data.append({
                'Алгоритм': hash_name,
                'Время (мс)': hash_time,
                'Размер (бит)': len(hash_bin)
            })
        
        # Показываем таблицу
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Визуализация производительности
        st.markdown("### ⚡ Производительность хеш-функций")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График времени выполнения
        algorithms = [r['Алгоритм'] for r in results]
        times = [float(r['Время (мс)']) for r in results]
        
        bars1 = ax1.bar(algorithms, times, color='skyblue', alpha=0.7)
        ax1.set_title('Время вычисления хеша')
        ax1.set_ylabel('Время (миллисекунды)')
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, time_val in zip(bars1, times):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{time_val:.4f} мс', ha='center', va='bottom')
        
        # График размера выхода
        sizes = [r['Размер выхода (бит)'] for r in results]
        
        bars2 = ax2.bar(algorithms, sizes, color='lightgreen', alpha=0.7)
        ax2.set_title('Размер выхода хеш-функции')
        ax2.set_ylabel('Размер (биты)')
        ax2.tick_params(axis='x', rotation=45)
        
        for bar, size in zip(bars2, sizes):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{size} бит', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Дополнительная информация
        st.markdown("#### 📈 Статистика распределения битов")
        self.show_bit_distribution(input_text, selected_hashes)
    
    def render_avalanche_effect(self):
        """Режим демонстрации лавинного эффекта"""
        st.markdown("### 🌊 Лавинный эффект")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_text = st.text_input(
                "Исходный текст:",
                "Hello World!",
                help="Исходный текст для хеширования"
            )
        
        with col2:
            modified_text = st.text_input(
                "Измененный текст:",
                "Hello World?",
                help="Текст с минимальным изменением"
            )
        
        selected_hash = st.selectbox(
            "Выберите хеш-функцию:",
            list(self.hash_functions.keys()),
            index=2  # SHA-256 по умолчанию
        )
        
        if st.button("🌊 Показать лавинный эффект", type="primary"):
            if not original_text or not modified_text:
                st.error("Введите оба текста!")
                return
            
            with st.spinner("Анализирую лавинный эффект..."):
                self.show_avalanche_effect(original_text, modified_text, selected_hash)
    
    def show_avalanche_effect(self, original_text, modified_text, hash_name):
        """Показывает лавинный эффект"""
        st.markdown("---")
        st.markdown("## 🌊 Анализ лавинного эффекта")
        
        hash_func = self.hash_functions[hash_name]
        
        # Вычисляем хеши
        hash_original = hash_func(original_text.encode('utf-8')).hexdigest()
        hash_modified = hash_func(modified_text.encode('utf-8')).hexdigest()
        
        # Преобразуем в бинарный вид
        bin_original = bin(int(hash_original, 16))[2:].zfill(len(hash_original) * 4)
        bin_modified = bin(int(hash_modified, 16))[2:].zfill(len(hash_modified) * 4)
        
        # Считаем различия
        differences = sum(1 for a, b in zip(bin_original, bin_modified) if a != b)
        total_bits = len(bin_original)
        difference_percent = (differences / total_bits) * 100
        
        # Показываем результаты
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Исходный хеш", hash_original[:16] + "...")
        with col2:
            st.metric("Измененный хеш", hash_modified[:16] + "...")
        with col3:
            st.metric("Изменено битов", f"{differences}/{total_bits} ({difference_percent:.1f}%)")
        
        # Визуализация различий
        st.markdown("### 🔍 Визуализация различий")
        
        # Показываем первые 128 бит для наглядности
        display_bits = 128
        bin_orig_display = bin_original[:display_bits]
        bin_mod_display = bin_modified[:display_bits]
        
        # Создаем визуализацию
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8))
        
        # График 1: Исходный хеш
        bits_orig = [int(bit) for bit in bin_orig_display]
        colors_orig = ['green' if bit == 1 else 'red' for bit in bits_orig]
        ax1.bar(range(len(bits_orig)), bits_orig, color=colors_orig, alpha=0.7)
        ax1.set_title(f'Исходный хеш ({hash_name}) - первые {display_bits} бит')
        ax1.set_ylabel('Бит (0/1)')
        ax1.set_ylim(0, 1)
        
        # График 2: Измененный хеш
        bits_mod = [int(bit) for bit in bin_mod_display]
        colors_mod = ['green' if bit == 1 else 'red' for bit in bits_mod]
        ax2.bar(range(len(bits_mod)), bits_mod, color=colors_mod, alpha=0.7)
        ax2.set_title(f'Измененный хеш ({hash_name}) - первые {display_bits} бит')
        ax2.set_ylabel('Бит (0/1)')
        ax2.set_ylim(0, 1)
        
        # График 3: Различия
        diff_bits = [1 if a != b else 0 for a, b in zip(bin_orig_display, bin_mod_display)]
        colors_diff = ['orange' if diff == 1 else 'gray' for diff in diff_bits]
        ax3.bar(range(len(diff_bits)), [1] * len(diff_bits), color=colors_diff, alpha=0.7)
        ax3.set_title(f'Различия между хешами ({sum(diff_bits)} из {display_bits} бит изменено)')
        ax3.set_ylabel('Изменен')
        ax3.set_ylim(0, 1)
        ax3.set_xlabel('Позиция бита')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Анализ изменений в тексте
        st.markdown("### 📝 Анализ изменений в тексте")
        
        text_diff = []
        for i, (char_orig, char_mod) in enumerate(zip(original_text, modified_text)):
            if char_orig != char_mod:
                text_diff.append(f"Позиция {i}: '{char_orig}' → '{char_mod}'")
        
        if text_diff:
            st.info("**Изменения в тексте:**")
            for diff in text_diff:
                st.write(f"- {diff}")
        else:
            st.warning("Тексты идентичны!")
    
    def render_collision_search(self):
        """Режим поиска коллизий"""
        st.markdown("### 🎯 Поиск коллизий")
        
        st.warning("""
        ⚠️ **Внимание:** Это учебная демонстрация. 
        Реальный поиск коллизий для современных хеш-функций требует огромных вычислительных ресурсов.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            hash_algorithm = st.selectbox(
                "Алгоритм для тестирования:",
                ["MD5", "SHA-1", "SHA-256"],
                index=0,
                key="collision_hash"
            )
        
        with col2:
            search_mode = st.selectbox(
                "Режим поиска:",
                ["Частичные коллизии (первые N бит)", "Полные коллизии (учебные)"],
                index=0
            )
        
        if search_mode == "Частичные коллизии (первые N бит)":
            collision_bits = st.slider("Количество бит для совпадения:", 8, 32, 16)
            max_attempts = st.slider("Максимальное количество попыток:", 1000, 100000, 10000)
        else:
            st.info("Будут показаны известные учебные примеры коллизий")
        
        if st.button("🎯 Начать поиск коллизий", type="primary"):
            with st.spinner("Ищу коллизии..."):
                if search_mode == "Частичные коллизии (первые N бит)":
                    self.find_partial_collisions(hash_algorithm, collision_bits, max_attempts)
                else:
                    self.show_educational_collisions(hash_algorithm)
    
    def find_partial_collisions(self, hash_algorithm, collision_bits, max_attempts):
        """Ищет частичные коллизии"""
        st.markdown("---")
        st.markdown(f"## 🎯 Поиск частичных коллизий для {hash_algorithm}")
        st.info(f"Ищем совпадение первых {collision_bits} бит")
        
        hash_func = self.hash_functions[hash_algorithm]
        found = False
        attempts = 0
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Генерируем случайные сообщения и ищем коллизии
        hashes_seen = {}
        
        for i in range(max_attempts):
            attempts = i + 1
            progress = attempts / max_attempts
            progress_bar.progress(progress)
            status_text.text(f"Попытка {attempts}/{max_attempts}")
            
            # Генерируем случайное сообщение
            message = f"message_{random.randint(0, 10**9)}"
            hash_hex = hash_func(message.encode('utf-8')).hexdigest()
            hash_bin = bin(int(hash_hex, 16))[2:].zfill(len(hash_hex) * 4)
            prefix = hash_bin[:collision_bits]
            
            if prefix in hashes_seen:
                # Нашли коллизию!
                found = True
                previous_message = hashes_seen[prefix]
                st.success(f"🎉 Найдена коллизия после {attempts} попыток!")
                
                st.markdown("#### 📊 Результаты коллизии:")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.error(f"**Сообщение 1:** {previous_message}")
                    st.error(f"**Хеш 1:** {hash_func(previous_message.encode('utf-8')).hexdigest()}")
                
                with col2:
                    st.error(f"**Сообщение 2:** {message}")
                    st.error(f"**Хеш 2:** {hash_hex}")
                
                st.info(f"**Совпадающие биты:** {collision_bits} бит")
                break
            else:
                hashes_seen[prefix] = message
        
        progress_bar.empty()
        status_text.empty()
        
        if not found:
            st.warning(f"Коллизии не найдены за {attempts} попыток")
            st.info("Попробуйте уменьшить количество бит или увеличить максимальное количество попыток")
    
    def show_educational_collisions(self, hash_algorithm):
        """Показывает учебные примеры коллизий"""
        st.markdown("---")
        st.markdown(f"## 📚 Известные коллизии для {hash_algorithm}")
        
        if hash_algorithm == "MD5":
            st.error("MD5 считается небезопасным из-за легкого нахождения коллизий")
            
            # Простые примеры для демонстрации
            examples = [
                {
                    "message1": "d131dd02c5e6eec4693d9a0698aff95c",
                    "message2": "d131dd02c5e6eec4693d9a0698aff95d", 
                    "description": "Изменение одного символа"
                }
            ]
            
            for example in examples:
                with st.expander(f"Пример коллизии: {example['description']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_area("Сообщение 1:", example["message1"], height=100)
                    with col2:
                        st.text_area("Сообщение 2:", example["message2"], height=100)
        
        elif hash_algorithm == "SHA-1":
            st.warning("SHA-1 имеет практические атаки на коллизии")
            st.info("Реальные примеры коллизий SHA-1 были продемонстрированы в 2017 году (атака SHAttered)")
        
        else:
            st.success("SHA-256 считается безопасным против атак на коллизии")
            st.info("На текущий момент не известно практических атак на полные коллизии SHA-256")
    
    def render_practical_uses(self):
        """Режим практических применений"""
        st.markdown("### 🔐 Практические применения хеш-функций")
        
        use_case = st.selectbox(
            "Выберите пример использования:",
            ["Проверка целостности файлов", "Хранение паролей", "Git коммиты", "Блокчейн (упрощенный)"]
        )
        
        if use_case == "Проверка целостности файлов":
            self.show_file_integrity()
        elif use_case == "Хранение паролей":
            self.show_password_storage()
        elif use_case == "Git коммиты":
            self.show_git_commits()
        else:
            self.show_blockchain_demo()
    
    def show_file_integrity(self):
        """Демонстрация проверки целостности файлов"""
        st.markdown("#### 📁 Проверка целостности файлов")
        
        # Инициализация состояния
        if 'file_original_content' not in st.session_state:
            st.session_state.file_original_content = "Важные данные: 12345\nКонфиденциальная информация"
        if 'file_original_hash' not in st.session_state:
            st.session_state.file_original_hash = ""
        
        file_content = st.text_area(
            "Содержимое файла:",
            st.session_state.file_original_content,
            height=150,
            key="file_content_input"
        )
        
        if st.button("🔍 Проверить целостность", key="check_integrity"):
            # Вычисляем хеш
            file_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
            st.session_state.file_original_content = file_content
            st.session_state.file_original_hash = file_hash
            st.rerun()
        
        # Показываем результаты если хеш вычислен
        if st.session_state.file_original_hash:
            st.success(f"**Хеш файла:** {st.session_state.file_original_hash}")
            st.info("Этот хеш можно использовать для проверки, что файл не был изменен")
            
            # Демонстрация изменения
            st.markdown("---")
            st.markdown("#### 🎭 Демонстрация изменения файла")
            
            modified_content = st.text_area(
                "Измените файл:",
                st.session_state.file_original_content,
                height=150,
                key="modified_file_content"
            )
            
            if modified_content != st.session_state.file_original_content:
                modified_hash = hashlib.sha256(modified_content.encode('utf-8')).hexdigest()
                st.error(f"**Новый хеш:** {modified_hash}")
                
                if modified_hash != st.session_state.file_original_hash:
                    st.error("❌ Целостность нарушена! Файл был изменен.")
                else:
                    st.success("✅ Целостность сохранена")
            else:
                st.info("Измените содержимое файла чтобы увидеть разницу в хеше")
    
    def show_password_storage(self):
        """Демонстрация хранения паролей"""
        st.markdown("#### 🔐 Хранение паролей")
        
        # Инициализация состояния
        if 'stored_password_hash' not in st.session_state:
            st.session_state.stored_password_hash = None
        if 'stored_salt' not in st.session_state:
            st.session_state.stored_salt = "random_salt_123"
        
        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input("Пароль:", type="password", value="mySecretPassword123", key="password_input")
        
        with col2:
            salt = st.text_input("Соль (salt):", value=st.session_state.stored_salt, key="salt_input")
            st.session_state.stored_salt = salt
        
        if st.button("🔒 Захешировать пароль", key="hash_password"):
            # Хешируем пароль с солью
            salted_password = password + salt
            password_hash = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
            st.session_state.stored_password_hash = password_hash
            st.rerun()
        
        # Показываем результаты если хеш сохранен
        if st.session_state.stored_password_hash:
            st.success(f"**Хеш пароля:** {st.session_state.stored_password_hash}")
            st.info("В базе данных хранится только этот хеш, а не оригинальный пароль")
            
            # Проверка пароля
            st.markdown("---")
            st.markdown("#### 🔍 Проверка пароля")
            
            check_password = st.text_input("Пароль для проверки:", type="password", key="check_password_input")
            
            if st.button("✅ Проверить пароль", key="verify_password"):
                if check_password:
                    check_hash = hashlib.sha256((check_password + st.session_state.stored_salt).encode('utf-8')).hexdigest()
                    
                    if check_hash == st.session_state.stored_password_hash:
                        st.success("✅ Пароль верный!")
                    else:
                        st.error("❌ Неверный пароль!")
    
    def show_bit_distribution(self, input_text, selected_hashes):
        """Показывает распределение битов в хешах"""
        st.markdown("#### 🔢 Распределение битов")
        
        bit_data = []
        
        for hash_name in selected_hashes:
            hash_func = self.hash_functions[hash_name]
            hash_hex = hash_func(input_text.encode('utf-8')).hexdigest()
            hash_bin = bin(int(hash_hex, 16))[2:].zfill(len(hash_hex) * 4)
            
            ones_count = hash_bin.count('1')
            zeros_count = hash_bin.count('0')
            total_bits = len(hash_bin)
            
            bit_data.append({
                'Алгоритм': hash_name,
                'Единицы': ones_count,
                'Нули': zeros_count,
                'Всего бит': total_bits,
                '% единиц': f"{(ones_count/total_bits)*100:.1f}%"
            })
        
        df_bits = pd.DataFrame(bit_data)
        st.dataframe(df_bits, use_container_width=True, hide_index=True)
        
        # Визуализация распределения
        fig, ax = plt.subplots(figsize=(10, 6))
        
        algorithms = [d['Алгоритм'] for d in bit_data]
        ones = [d['Единицы'] for d in bit_data]
        zeros = [d['Нули'] for d in bit_data]
        
        x = np.arange(len(algorithms))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, ones, width, label='Единицы (1)', color='blue', alpha=0.7)
        bars2 = ax.bar(x + width/2, zeros, width, label='Нули (0)', color='red', alpha=0.7)
        
        ax.set_title('Распределение битов в хешах')
        ax.set_ylabel('Количество бит')
        ax.set_xticks(x)
        ax.set_xticklabels(algorithms)
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)

    def show_git_commits(self):
        """Демонстрация Git коммитов"""
        st.markdown("#### 🗂️ Git коммиты и хеши")
        
        # Инициализация состояния
        if 'git_original_commit' not in st.session_state:
            st.session_state.git_original_commit = "Author: John Doe <john@example.com>\nDate: 2024-01-15\n\nMessage: Fix critical bug\n\nChanges: - Fixed null pointer exception"
        if 'git_original_hash' not in st.session_state:
            st.session_state.git_original_hash = ""
        
        commit_data = st.text_area(
            "Данные коммита (автор, дата, сообщение, изменения):",
            st.session_state.git_original_commit,
            height=200,
            key="git_commit_input"
        )
        
        if st.button("🔗 Создать Git-подобный хеш", key="create_git_hash"):
            # Упрощенная демонстрация Git хеширования
            git_like_content = f"commit {len(commit_data)}\0{commit_data}"
            commit_hash = hashlib.sha1(git_like_content.encode('utf-8')).hexdigest()
            
            st.session_state.git_original_commit = commit_data
            st.session_state.git_original_hash = commit_hash
            st.rerun()
        
        # Показываем результаты если хеш вычислен
        if st.session_state.git_original_hash:
            st.success(f"**Хеш коммита (SHA-1):** {st.session_state.git_original_hash}")
            st.info("Git использует SHA-1 для идентификации коммитов, хотя это вызывает споры о безопасности")
            
            # Показываем, как небольшое изменение меняет хеш
            st.markdown("---")
            st.markdown("#### 🔍 Чувствительность к изменениям")
            
            modified_commit = st.text_area(
                "Внесите небольшое изменение:",
                st.session_state.git_original_commit,
                height=200,
                key="modified_git_commit"
            )
            
            if modified_commit != st.session_state.git_original_commit:
                modified_git_content = f"commit {len(modified_commit)}\0{modified_commit}"
                modified_hash = hashlib.sha1(modified_git_content.encode('utf-8')).hexdigest()
                
                st.error(f"**Новый хеш:** {modified_hash}")
                st.warning("Даже минимальное изменение полностью меняет хеш коммита!")

    def show_blockchain_demo(self):
        """Упрощенная демонстрация блокчейна"""
        st.markdown("#### ⛓️ Блокчейн (упрощенная демонстрация)")
        
        st.info("""
        В блокчейне каждый блок содержит:
        - Данные транзакций
        - Хеш предыдущего блока
        - Собственный хеш
        """)
        
        # Инициализация состояния
        if 'blockchain_data' not in st.session_state:
            st.session_state.blockchain_data = {
                'block1': "Транзакция: Alice → Bob: 10 BTC",
                'block2': "Транзакция: Bob → Charlie: 5 BTC"
            }
        if 'blockchain_hashes' not in st.session_state:
            st.session_state.blockchain_hashes = {}
        
        # Создаем простую цепочку блоков
        block1_data = st.text_input("Данные блока 1:", 
                                st.session_state.blockchain_data.get('block1', "Транзакция: Alice → Bob: 10 BTC"),
                                key="block1_input")
        
        block2_data = st.text_input("Данные блока 2:", 
                                st.session_state.blockchain_data.get('block2', "Транзакция: Bob → Charlie: 5 BTC"),
                                key="block2_input")
        
        if st.button("🔗 Создать блокчейн", key="create_blockchain"):
            # Сохраняем данные
            st.session_state.blockchain_data = {
                'block1': block1_data,
                'block2': block2_data
            }
            
            # Блок 1
            block1_content = f"Блок 1: {block1_data}"
            block1_hash = hashlib.sha256(block1_content.encode('utf-8')).hexdigest()
            
            # Блок 2 (содержит хеш блока 1)
            block2_content = f"Блок 2: {block2_data} | Предыдущий хеш: {block1_hash}"
            block2_hash = hashlib.sha256(block2_content.encode('utf-8')).hexdigest()
            
            st.session_state.blockchain_hashes = {
                'block1_hash': block1_hash,
                'block2_hash': block2_hash,
                'block1_content': block1_content,
                'block2_content': block2_content
            }
            st.rerun()
        
        # Показываем результаты если блокчейн создан
        if st.session_state.blockchain_hashes:
            st.success("**Создана цепочка блоков:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Блок 1", st.session_state.blockchain_hashes['block1_hash'][:16] + "...")
                st.text_area("Содержимое:", 
                            st.session_state.blockchain_hashes['block1_content'], 
                            height=100, 
                            key="block1_display")
            
            with col2:
                st.metric("Блок 2", st.session_state.blockchain_hashes['block2_hash'][:16] + "...")
                st.text_area("Содержимое:", 
                            st.session_state.blockchain_hashes['block2_content'], 
                            height=100, 
                            key="block2_display")
            
            st.info("Если изменить данные в блоке 1, хеш блока 1 изменится, что сделает недействительным блок 2 и всю последующую цепочку!")
            
            # Кнопка для сброса блокчейна
            if st.button("🔄 Создать новый блокчейн", key="reset_blockchain"):
                st.session_state.blockchain_hashes = {}
                st.session_state.blockchain_data = {}
                st.rerun()