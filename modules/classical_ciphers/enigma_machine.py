from modules.base_module import CryptoModule
import streamlit as st
import secrets
import string
from typing import List, Dict, Tuple
import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum
import plotly.graph_objects as go
import plotly.express as px

class RotorType(Enum):
    I = "I"
    II = "II" 
    III = "III"
    IV = "IV"
    V = "V"

@dataclass
class Rotor:
    wiring: str
    notch: str
    position: int
    ring_setting: int
    name: str

class ReflectorType(Enum):
    A = "A"
    B = "B"
    C = "C"

class EnigmaMachineModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Машина Энигма"
        self.description = "Легендарная шифровальная машина Второй мировой войны с полной визуализацией"
        self.category = "classical"
        self.icon = ""
        self.order = 10
        
        # Стандартные роторы Энигмы
        self.rotors_config = {
            RotorType.I: Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q", 0, 0, "I"),
            RotorType.II: Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E", 0, 0, "II"),
            RotorType.III: Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V", 0, 0, "III"),
            RotorType.IV: Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J", 0, 0, "IV"), 
            RotorType.V: Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", "Z", 0, 0, "V")
        }
        
        # Рефлекторы
        self.reflectors_config = {
            ReflectorType.A: "EJMZALYXVBWFCRQUONTSPIKHGD",
            ReflectorType.B: "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            ReflectorType.C: "FVPJIAOYEDRZXWGCTKUQSBNMHL"
        }
        
        # Алфавит
        self.alphabet = string.ascii_uppercase

    def render(self):
        st.title("⚙️ Машина Энигма")
        
        # Инициализация session_state
        if 'enigma_initialized' not in st.session_state:
            self.initialize_session_state()
        
        # Теоретическая справка
        with st.expander("📚 Историческая справка", expanded=False):
            st.markdown("""
            **Машина Энигма** - роторная шифровальная машина, использовавшаяся Германией во Второй мировой войне.
            
            **Принцип работы:**
            - **Роторы (3-5)**: Каждый ротор выполняет замену букв и поворачивается после каждого символа
            - **Рефлектор**: Отражает сигнал обратно через роторы, обеспечивая симметричность
            - **Коммутационная панель**: Дополнительные парные замены букв
            - **Кольцевые настройки**: Смещение wiring относительно положения ротора
            
            **Историческое значение:**
            - Считалась "невзламываемой" до работы Алана Тьюринга
            - Взлом Энигмы ускорил окончание войны на 2-4 года
            - Заложила основы современной криптографии и computer science
            
            **Стойкость:** ~158 миллионов миллионов миллионов возможных настроек
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4 = st.tabs(["🎛️ Управление машиной", "🔐 Шифрование", "🎯 Визуализация", "📚 Обучение"])
        
        with tab1:
            self.render_control_panel()
        
        with tab2:
            self.render_encryption_section()
            
        with tab3:
            self.render_visualization()
            
        with tab4:
            self.render_education_section()

    def initialize_session_state(self):
        """Инициализирует все необходимые переменные в session_state"""
        st.session_state.enigma_initialized = True
        st.session_state.enigma_rotors = [RotorType.I, RotorType.II, RotorType.III]
        st.session_state.enigma_positions = [0, 0, 0]
        st.session_state.enigma_rings = [0, 0, 0]
        st.session_state.enigma_reflector = ReflectorType.B
        st.session_state.enigma_plugboard = "AB CD EF"
        st.session_state.enigma_output = ""
        st.session_state.last_processed = ""
        st.session_state.last_signal_path = []

    def get_rotor_index(self, rotor_type: RotorType) -> int:
        """Получает индекс ротора в списке для selectbox"""
        rotor_values = [rt.value for rt in RotorType]
        return rotor_values.index(rotor_type.value)

    def get_reflector_index(self, reflector_type: ReflectorType) -> int:
        """Получает индекс рефлектора в списке для selectbox"""
        reflector_values = [rf.value for rf in ReflectorType]
        return reflector_values.index(reflector_type.value)

    def render_control_panel(self):
        """Панель управления настройками Энигмы"""
        st.header("🎛️ Панель управления Энигмой")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Выбор роторов и их позиций
            st.subheader("🔧 Настройка роторов")
            
            rotor_cols = st.columns(5)
            
            for i in range(3):
                with rotor_cols[i]:
                    # Сохраняем текущее значение перед созданием виджета
                    current_rotor = st.session_state.enigma_rotors[i]
                    
                    rotor_type = st.selectbox(
                        f"Ротор {i+1}:",
                        [rt.value for rt in RotorType],
                        index=self.get_rotor_index(current_rotor),
                        key=f"rotor_select_{i}"
                    )
                    # Обновляем состояние после взаимодействия с виджетом
                    selected_rotor = None
                    for rt in RotorType:
                        if rt.value == rotor_type:
                            selected_rotor = rt
                            break
                    
                    if selected_rotor and selected_rotor != st.session_state.enigma_rotors[i]:
                        st.session_state.enigma_rotors[i] = selected_rotor
                    
                    position = st.number_input(
                        "Позиция:",
                        min_value=0,
                        max_value=25,
                        value=st.session_state.enigma_positions[i],
                        key=f"pos_input_{i}"
                    )
                    if position != st.session_state.enigma_positions[i]:
                        st.session_state.enigma_positions[i] = position
                    
                    ring_setting = st.number_input(
                        "Кольцо:",
                        min_value=0,
                        max_value=25,
                        value=st.session_state.enigma_rings[i],
                        key=f"ring_input_{i}"
                    )
                    if ring_setting != st.session_state.enigma_rings[i]:
                        st.session_state.enigma_rings[i] = ring_setting
            
            # Рефлектор
            st.subheader("🪞 Рефлектор")
            current_reflector = st.session_state.enigma_reflector
            reflector = st.selectbox(
                "Тип рефлектора:",
                [rf.value for rf in ReflectorType],
                index=self.get_reflector_index(current_reflector),
                key="reflector_select"
            )
            
            selected_reflector = None
            for rf in ReflectorType:
                if rf.value == reflector:
                    selected_reflector = rf
                    break
            
            if selected_reflector and selected_reflector != st.session_state.enigma_reflector:
                st.session_state.enigma_reflector = selected_reflector
            
        with col2:
            # Коммутационная панель
            st.subheader("🔌 Коммутационная панель")
            st.markdown("Соедините буквы парами:")
            
            # Используем уникальный ключ для текстового поля
            plugboard_key = "plugboard_input_" + str(hash(st.session_state.enigma_plugboard))
            
            plug_pairs = st.text_area(
                "Пары (например: AB CD EF):",
                st.session_state.enigma_plugboard,
                height=100,
                key=plugboard_key
            )
            
            if plug_pairs != st.session_state.enigma_plugboard:
                st.session_state.enigma_plugboard = plug_pairs
            
            # Статус машины
            st.subheader("📊 Статус машины")
            self.display_machine_status()
            
            # Кнопки быстрой настройки
            st.subheader("⚡ Быстрые настройки")
            if st.button("🎲 Случайные настройки", use_container_width=True, key="random_btn"):
                self.random_settings()
                st.rerun()
                
            if st.button("🔄 Сброс", use_container_width=True, key="reset_btn"):
                self.reset_settings()
                st.rerun()

    def render_encryption_section(self):
        """Секция шифрования/дешифрования"""
        st.header("🔐 Шифрование текста")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ввод текста")
            input_text = st.text_area(
                "Текст для шифрования:",
                "HELLOENIGMA",
                height=150,
                key="enigma_input_text"
            ).upper()
            
            # Фильтруем только буквы
            filtered_text = ''.join(filter(str.isalpha, input_text))
            if filtered_text != input_text:
                st.warning(f"Удалены не-буквенные символы. Будет обработано: {filtered_text}")
            
            if st.button("🔒 Зашифровать", use_container_width=True, key="encrypt_btn"):
                if filtered_text:
                    encrypted = self.encrypt_text(filtered_text)
                    st.session_state.enigma_output = encrypted
                    st.session_state.last_processed = filtered_text
                    st.rerun()
        
        with col2:
            st.subheader("Результат")
            output_text = st.text_area(
                "Результат:",
                st.session_state.enigma_output,
                height=150,
                key="enigma_output_display"
            )
            
            if st.session_state.last_processed:
                st.info(f"Обработано: {st.session_state.last_processed}")
            
            if st.button("📋 Копировать результат", use_container_width=True, key="copy_btn"):
                st.code(output_text)

        # Детализация процесса для последнего символа
        if st.session_state.get('last_processed'):
            st.subheader("🔍 Детализация процесса")
            self.show_encryption_details(st.session_state.last_processed)

    def render_visualization(self):
        """Визуализация работы машины"""
        st.header("🎯 Визуализация работы Энигмы")
        
        # 3D визуализация роторов
        st.subheader("🔄 Визуализация роторов")
        self.visualize_rotors()
        
        # Диаграмма пути сигнала
        st.subheader("📡 Путь сигнала через машину")
        if st.session_state.last_signal_path:
            self.visualize_signal_path(st.session_state.last_signal_path)
        
        # Анимация работы
        st.subheader("🎬 Анимация процесса")
        demo_char = st.selectbox("Выберите букву для демонстрации:", list(self.alphabet), index=7, key="demo_char_select")
        
        if st.button("▶️ Запустить анимацию", key="animate_btn"):
            # Создаем правильные роторы для демонстрации
            rotors = self.create_demo_rotors()
            plugboard = self.set_plugboard(st.session_state.enigma_plugboard)
            reflector = self.reflectors_config[st.session_state.enigma_reflector]
            
            signal_path = self.animate_encryption_process(demo_char, rotors, reflector, plugboard)
            st.session_state.last_signal_path = signal_path
            st.rerun()

    def render_education_section(self):
        """Образовательный раздел"""
        st.header("📚 Обучение работе с Энигмой")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧩 Компоненты Энигмы")
            
            components = {
                "Роторы": "Выполняют замену. Поворачиваются после каждого символа",
                "Рефлектор": "Отражает сигнал, обеспечивая симметричность шифрования", 
                "Коммутационная панель": "Дополнительные парные замены букв",
                "Кольцевые настройки": "Смещение проводки относительно положения ротора"
            }
            
            for comp, desc in components.items():
                with st.expander(f"🔧 {comp}"):
                    st.write(desc)
        
        with col2:
            st.subheader("🎯 Принцип работы")
            
            st.markdown("""
            1. **Ввод символа** → Коммутационная панель
            2. **Проход через роторы** справа налево
            3. **Отражение** от рефлектора  
            4. **Обратный проход** через роторы
            5. **Вывод** через коммутационную панель
            6. **Поворот роторов** после каждого символа
            """)
            
            st.subheader("🔐 Криптоанализ")
            st.markdown("""
            - **Повторяемость**: 26³ = 17,576 начальных позиций
            - **Уязвимости**: Невозможность шифрования буквы самой в себя
            - **Методы взлома**: Бомба Тьюринга, crib-based атаки
            """)

    def create_demo_rotors(self):
        """Создает роторы для демонстрации с текущими настройками"""
        rotors = []
        for i in range(3):
            rotor_config = self.rotors_config[st.session_state.enigma_rotors[i]]
            rotor = Rotor(
                wiring=rotor_config.wiring,
                notch=rotor_config.notch,
                position=st.session_state.enigma_positions[i],
                ring_setting=st.session_state.enigma_rings[i],
                name=rotor_config.name
            )
            rotors.append(rotor)
        return rotors

    def set_plugboard(self, plug_pairs: str):
        """Устанавливает соединения на коммутационной панели"""
        plugboard = {}
        pairs = plug_pairs.upper().split()
        
        for pair in pairs:
            if len(pair) == 2 and pair[0] != pair[1]:
                plugboard[pair[0]] = pair[1]
                plugboard[pair[1]] = pair[0]
        
        return plugboard

    def display_machine_status(self):
        """Отображает текущий статус машины"""
        status_data = []
        
        for i in range(3):
            rotor = st.session_state.enigma_rotors[i]
            status_data.append({
                'Ротор': f"{i+1}",
                'Тип': rotor.value,
                'Позиция': chr(65 + st.session_state.enigma_positions[i]),
                'Кольцо': chr(65 + st.session_state.enigma_rings[i])
            })
        
        df = pd.DataFrame(status_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Коммутационная панель
        plugboard = self.set_plugboard(st.session_state.enigma_plugboard)
        if plugboard:
            plugs = [f"{k}{v}" for k, v in plugboard.items() if k < v]
            st.write(f"🔌 Соединения: {', '.join(plugs)}")
        else:
            st.write("🔌 Соединения: нет")
            
        st.write(f"🪞 Рефлектор: {st.session_state.enigma_reflector.value}")

    def random_settings(self):
        """Устанавливает случайные настройки"""
        # Случайные роторы
        all_rotors = list(RotorType)
        st.session_state.enigma_rotors = secrets.SystemRandom().sample(all_rotors, 3)
        
        # Случайные позиции и кольца
        st.session_state.enigma_positions = [secrets.randbelow(26) for _ in range(3)]
        st.session_state.enigma_rings = [secrets.randbelow(26) for _ in range(3)]
        
        # Случайный рефлектор
        st.session_state.enigma_reflector = secrets.choice(list(ReflectorType))
        
        # Случайные соединения
        letters = list(self.alphabet)
        secrets.SystemRandom().shuffle(letters)
        plug_pairs = []
        for i in range(0, min(10, len(letters)), 2):
            plug_pairs.append(f"{letters[i]}{letters[i+1]}")
        
        st.session_state.enigma_plugboard = " ".join(plug_pairs)

    def reset_settings(self):
        """Сбрасывает настройки к значениям по умолчанию"""
        st.session_state.enigma_rotors = [RotorType.I, RotorType.II, RotorType.III]
        st.session_state.enigma_positions = [0, 0, 0]
        st.session_state.enigma_rings = [0, 0, 0]
        st.session_state.enigma_reflector = ReflectorType.B
        st.session_state.enigma_plugboard = "AB CD EF"

    def encrypt_text(self, text: str) -> str:
        """Шифрует текст с текущими настройками Энигмы"""
        result = []
        
        # Инициализируем роторы
        rotors = self.create_demo_rotors()
        reflector = self.reflectors_config[st.session_state.enigma_reflector]
        plugboard = self.set_plugboard(st.session_state.enigma_plugboard)
        
        for char in text:
            if char in self.alphabet:
                # Поворачиваем роторы
                self.rotate_rotors(rotors)
                
                # Шифруем символ
                encrypted_char = self.process_char(char, rotors, reflector, plugboard)
                result.append(encrypted_char)
        
        return ''.join(result)

    def rotate_rotors(self, rotors: List[Rotor]):
        """Поворачивает роторы согласно механизму Энигмы"""
        # Правый ротор всегда поворачивается
        rotate_next = True
        
        for i in range(2, -1, -1):  # Справа налево: 2,1,0
            if rotate_next:
                rotors[i].position = (rotors[i].position + 1) % 26
                
                # Проверяем, достигли ли мы notch позиции
                current_pos = chr((rotors[i].position) % 26 + 65)
                if current_pos == rotors[i].notch:
                    rotate_next = True
                else:
                    rotate_next = False
            else:
                break

    def process_char(self, char: str, rotors: List[Rotor], reflector: str, plugboard: Dict) -> str:
        """Обрабатывает один символ через машину Энигма"""
        # Коммутационная панель (вход)
        if char in plugboard:
            char = plugboard[char]
        
        # Проход через роторы справа налево
        signal = char
        signal_path = [f"Вход: {signal}"]
        
        for i in range(2, -1, -1):
            signal = self.pass_through_rotor(signal, rotors[i], forward=True)
            signal_path.append(f"Ротор {i+1} → {signal}")
        
        # Рефлектор
        reflector_pos = self.alphabet.index(signal)
        signal = reflector[reflector_pos]
        signal_path.append(f"Рефлектор → {signal}")
        
        # Обратный проход через роторы слева направо
        for i in range(3):
            signal = self.pass_through_rotor(signal, rotors[i], forward=False)
            signal_path.append(f"Ротор {i+1} ← {signal}")
        
        # Коммутационная панель (выход)
        if signal in plugboard:
            signal = plugboard[signal]
        signal_path.append(f"Выход: {signal}")
        
        st.session_state.last_signal_path = signal_path
        return signal

    def pass_through_rotor(self, char: str, rotor: Rotor, forward: bool) -> str:
        """Пропускает символ через ротор в указанном направлении"""
        pos = self.alphabet.index(char)
        
        if forward:
            # Учитываем положение ротора и кольцевую настройку
            effective_pos = (pos + rotor.position - rotor.ring_setting) % 26
            encrypted_pos = self.alphabet.index(rotor.wiring[effective_pos])
            result_pos = (encrypted_pos - rotor.position + rotor.ring_setting) % 26
        else:
            # Обратное направление
            effective_pos = (pos + rotor.position - rotor.ring_setting) % 26
            encrypted_pos = rotor.wiring.index(self.alphabet[effective_pos])
            result_pos = (encrypted_pos - rotor.position + rotor.ring_setting) % 26
        
        return self.alphabet[result_pos]

    def show_encryption_details(self, text: str):
        """Показывает детали шифрования"""
        if len(text) > 0:
            # Показываем таблицу преобразований для первых 10 символов
            display_text = text[:10]
            
            data = []
            for i, char in enumerate(display_text):
                data.append({
                    'Позиция': i + 1,
                    'Вход': char,
                    'Выход': st.session_state.enigma_output[i] if i < len(st.session_state.enigma_output) else ''
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Показываем текущие позиции роторов
            st.subheader("📊 Текущие позиции роторов")
            positions = [chr(65 + (st.session_state.enigma_positions[i] + len(text)) % 26) for i in range(3)]
            
            col1, col2, col3 = st.columns(3)
            for i, pos in enumerate(positions):
                with [col1, col2, col3][i]:
                    st.metric(f"Ротор {i+1}", pos)

    def visualize_rotors(self):
        """Визуализирует текущее состояние роторов"""
        # Создаем круговые диаграммы для каждого ротора
        fig = go.Figure()
        
        for i in range(3):
            rotor = st.session_state.enigma_rotors[i]
            # Позиции на круге
            angles = np.linspace(0, 2*np.pi, 26, endpoint=False)
            radius = 3 - i * 0.7  # Разные радиусы для роторов
            
            # Текущая позиция
            current_angle = angles[st.session_state.enigma_positions[i]]
            
            # Добавляем круг с буквами
            x = radius * np.cos(angles)
            y = radius * np.sin(angles)
            
            fig.add_trace(go.Scatter(
                x=x, y=y,
                mode='text',
                text=list(self.alphabet),
                textfont=dict(size=14, color='blue'),
                name=f'Ротор {i+1} ({rotor.value})'
            ))
            
            # Маркер текущей позиции
            fig.add_trace(go.Scatter(
                x=[radius * np.cos(current_angle)],
                y=[radius * np.sin(current_angle)],
                mode='markers',
                marker=dict(size=20, color='red', symbol='triangle-up'),
                name=f'Позиция {i+1}'
            ))
        
        # Настройки графика
        fig.update_layout(
            title="Визуализация роторов Энигмы",
            showlegend=True,
            width=600,
            height=500,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def visualize_signal_path(self, signal_path: List[str]):
        """Визуализирует путь сигнала через машину"""
        steps = [step.split(' → ')[0] for step in signal_path]
        signals = [step.split(' → ')[1] if ' → ' in step else step for step in signal_path]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(len(signal_path))),
            y=[1] * len(signal_path),
            mode='lines+markers+text',
            line=dict(color='red', width=3),
            marker=dict(size=15, color='red'),
            text=signals,
            textposition="top center",
            name='Путь сигнала'
        ))
        
        fig.update_layout(
            title="Путь сигнала через машину Энигма",
            xaxis=dict(
                title='Этап обработки',
                tickvals=list(range(len(steps))),
                ticktext=steps
            ),
            yaxis=dict(visible=False),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def animate_encryption_process(self, char: str, rotors: List[Rotor], reflector: str, plugboard: Dict):
        """Анимирует процесс шифрования одного символа"""
        # Создаем пошаговую анимацию с реальными преобразованиями
        steps = []
        signals = []
        
        # Начальный этап
        current_signal = char
        steps.append("Вход")
        signals.append(current_signal)
        
        # Коммутационная панель (вход)
        if current_signal in plugboard:
            current_signal = plugboard[current_signal]
        steps.append("Plugboard вход")
        signals.append(current_signal)
        
        # Проход через роторы справа налево
        for i in range(2, -1, -1):
            current_signal = self.pass_through_rotor(current_signal, rotors[i], forward=True)
            steps.append(f"Ротор {i+1} →")
            signals.append(current_signal)
        
        # Рефлектор
        reflector_pos = self.alphabet.index(current_signal)
        current_signal = reflector[reflector_pos]
        steps.append("Рефлектор")
        signals.append(current_signal)
        
        # Обратный проход через роторы слева направо
        for i in range(3):
            current_signal = self.pass_through_rotor(current_signal, rotors[i], forward=False)
            steps.append(f"Ротор {i+1} ←")
            signals.append(current_signal)
        
        # Коммутационная панель (выход)
        if current_signal in plugboard:
            current_signal = plugboard[current_signal]
        steps.append("Plugboard выход")
        signals.append(current_signal)
        
        steps.append("Выход")
        signals.append(current_signal)
        
        # Создаем анимированный график
        fig = go.Figure()
        
        for i, (step, signal) in enumerate(zip(steps, signals)):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[1],
                mode='markers+text',
                marker=dict(size=25, color='blue', symbol='circle'),
                text=[signal],
                textposition="middle center",
                textfont=dict(size=16, color='white', weight='bold'),
                name=step
            ))
        
        # Добавляем линии соединения
        fig.add_trace(go.Scatter(
            x=list(range(len(steps))),
            y=[1] * len(steps),
            mode='lines',
            line=dict(color='red', width=3, dash='dot'),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"🔐 Анимация шифрования буквы '{char}' → '{signals[-1]}'",
            xaxis=dict(
                title='Этапы шифрования',
                tickvals=list(range(len(steps))),
                ticktext=steps,
                tickangle=45
            ),
            yaxis=dict(visible=False),
            showlegend=False,
            height=500,
            width=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Возвращаем путь сигнала для отображения в другой визуализации
        signal_path = [f"{step} → {sig}" for step, sig in zip(steps, signals)]
        return signal_path

# Для обратной совместимости
class EnigmaMachine(EnigmaMachineModule):
    pass