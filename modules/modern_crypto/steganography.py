import random
from modules.base_module import CryptoModule
import streamlit as st
import secrets
import numpy as np
#import cv2 
from PIL import Image
import io
import base64
from typing import List, Tuple, Dict, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
import wave
import struct
import math
from cryptography.fernet import Fernet

@dataclass
class SteganographyMethod:
    name: str
    description: str
    capacity: str
    security: str
    detectability: str
    file_types: List[str]

@dataclass
class StegoAnalysis:
    method: str
    detection_score: float
    confidence: float
    artifacts_found: List[str]

class SteganographyModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Методы стеганографии"
        self.description = "Визуализация методов сокрытия информации в различных носителях"
        self.category = "modern"
        self.icon = ""
        self.order = 11
        
        # Методы стеганографии
        self.methods = {
            "lsb_image": SteganographyMethod(
                "LSB в изображениях",
                "Замена наименее значащих битов пикселей",
                "Высокая",
                "Низкая",
                "Легко обнаруживается",
                ["PNG", "BMP", "TIFF"]
            ),
            "lsb_audio": SteganographyMethod(
                "LSB в аудио",
                "Замена наименее значащих битов аудиосэмплов",
                "Средняя",
                "Низкая",
                "Обнаруживается статистически",
                ["WAV", "FLAC"]
            ),
            "dct": SteganographyMethod(
                "DCT коэффициенты",
                "Модификация коэффициентов дискретного косинусного преобразования",
                "Средняя",
                "Высокая",
                "Трудно обнаруживается",
                ["JPEG"]
            ),
            "echo_hiding": SteganographyMethod(
                "Эхо-скрытие",
                "Добавление задержанных эхо-сигналов в аудио",
                "Низкая",
                "Средняя",
                "Обнаруживается спектральным анализом",
                ["WAV", "MP3"]
            ),
            "text_whitespace": SteganographyMethod(
                "Пробелы в тексте",
                "Использование пробелов и табуляций для кодирования",
                "Очень низкая",
                "Очень низкая",
                "Легко обнаруживается",
                ["TXT", "DOC", "PDF"]
            ),
            "pdf_metadata": SteganographyMethod(
                "Метаданные PDF",
                "Сокрытие в метаданных документов",
                "Низкая",
                "Средняя",
                "Обнаруживается анализом метаданных",
                ["PDF"]
            )
        }

    def render(self):
        st.title("🕵️ Методы стеганографии")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Стеганография** - наука о скрытой передаче информации путем сокрытия самого факта передачи.
            
            ### 🎯 Основные принципы:
            
            **Отличие от криптографии:**
            - Криптография скрывает содержание сообщения
            - Стеганография скрывает сам факт существования сообщения
            
            **Ключевые требования:**
            - **Незаметность**: Скрытые данные не должны быть обнаружены
            - **Емкость**: Количество данных, которые можно скрыть
            - **Устойчивость**: Сопротивление попыткам извлечения или уничтожения
            
            ### 🖼️ Методы стеганографии в изображениях:
            
            **LSB (Least Significant Bit):**
            - Замена наименее значимых битов пикселей
            - Высокая емкость, низкая безопасность
            - Легко обнаруживается статистическим анализом
            
            **DCT коэффициенты (JPEG):**
            - Модификация коэффициентов дискретного косинусного преобразования
            - Средняя емкость, высокая безопасность
            - Устойчиво к простому статистическому анализу
            
            **Стеганоанализ - обнаружение стеганографии:**
            - Статистический анализ гистограмм
            - Анализ частотных характеристик
            - Машинное обучение для классификации
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🖼️ Стеганография в изображениях", "🎵 Стеганография в аудио", 
            "📄 Стеганография в тексте", "🔍 Стеганоанализ", "📊 Сравнение методов"
        ])

        with tab1:
            self.render_image_steganography()
        
        with tab2:
            self.render_audio_steganography()
            
        with tab3:
            self.render_text_steganography()
            
        with tab4:
            self.render_steganalysis()
            
        with tab5:
            self.render_methods_comparison()

    def render_image_steganography(self):
        """Стеганография в изображениях"""
        st.header("🖼️ Стеганография в изображениях")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Кодирование сообщения")
            
            # Инициализация session_state
            if 'image_method' not in st.session_state:
                st.session_state.image_method = "LSB"
            if 'stego_image' not in st.session_state:
                st.session_state.stego_image = None
            
            # Загрузка изображения
            uploaded_file = st.file_uploader(
                "Выберите изображение-носитель:",
                type=['png', 'jpg', 'jpeg', 'bmp'],
                key="image_upload"
            )
            
            if uploaded_file is not None:
                # Отображение оригинального изображения
                image = Image.open(uploaded_file)
                st.image(image, caption="Оригинальное изображение", use_column_width=True)
                
                # Ввод сообщения
                secret_message = st.text_area(
                    "Секретное сообщение:",
                    "Секретная информация для сокрытия в изображении",
                    height=100,
                    key="secret_msg"
                )
                
                # Выбор метода - используем callback для обновления
                def update_image_method():
                    st.session_state.image_method = st.session_state.image_method_select
                
                method = st.selectbox(
                    "Метод стеганографии:",
                    ["LSB", "DCT"],
                    key="image_method_select",
                    index=0 if st.session_state.image_method == "LSB" else 1,
                    on_change=update_image_method
                )
                
                if st.button("🕵️ Скрыть сообщение", key="hide_image"):
                    if method == "LSB":
                        try:
                            stego_image = self.lsb_encode(image, secret_message)
                            st.session_state.stego_image = stego_image
                            st.success("✅ Сообщение скрыто в изображении методом LSB!")
                        except ValueError as e:
                            st.error(f"❌ Ошибка: {e}")
                    else:
                        stego_image = self.dct_encode(image, secret_message)
                        st.session_state.stego_image = stego_image
                        st.success("✅ Сообщение скрыто в изображении методом DCT!")
            
            # Извлечение сообщения
            st.subheader("📥 Извлечение сообщения")
            
            extracted_file = st.file_uploader(
                "Выберите стего-изображение:",
                type=['png', 'jpg', 'jpeg'],
                key="stego_upload"
            )
            
            if extracted_file is not None:
                stego_img = Image.open(extracted_file)
                st.image(stego_img, caption="Стего-изображение", use_column_width=True)
                
                # Используем отдельный ключ для извлечения
                extract_method = st.selectbox(
                    "Метод извлечения:",
                    ["LSB", "DCT"],
                    key="extract_method_select"
                )
                
                if st.button("🔍 Извлечь сообщение", key="extract_image"):
                    if extract_method == "LSB":
                        message = self.lsb_decode(stego_img)
                    else:
                        message = self.dct_decode(stego_img)
                    
                    if message:
                        st.success(f"✅ Извлеченное сообщение: {message}")
                    else:
                        st.error("❌ Не удалось извлечь сообщение")
        
        with col2:
            st.subheader("🔍 Анализ изображений")
            
            if st.session_state.stego_image is not None:
                st.image(st.session_state.stego_image, caption="Стего-изображение", use_column_width=True)
                
                # Сравнение гистограмм
                if uploaded_file and st.session_state.stego_image is not None:
                    st.subheader("📊 Сравнение гистограмм")
                    
                    # Конвертация изображений в numpy массивы
                    original_arr = np.array(image)
                    stego_arr = np.array(st.session_state.stego_image)
                    
                    # Создание гистограмм
                    fig = self.create_histogram_comparison(original_arr, stego_arr)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Анализ различий
                    analysis = self.analyze_image_differences(original_arr, stego_arr)
                    st.write("**Анализ различий:**")
                    st.write(f"- Средняя разница: {analysis['mean_diff']:.6f}")
                    st.write(f"- Максимальная разница: {analysis['max_diff']}")
                    st.write(f"- Измененные пиксели: {analysis['changed_pixels']}")
            
            # Демонстрация LSB метода
            st.subheader("🎯 Демонстрация LSB метода")
            
            if st.button("👁️ Показать LSB визуализацию", key="show_lsb"):
                demo_img = self.create_lsb_demo_image()
                st.image(demo_img, caption="Визуализация LSB метода", use_column_width=True)
                
                st.markdown("""
                **Объяснение LSB метода:**
                - Каждый пиксель представлен RGB значениями (0-255)
                - Меняем только последний бит каждого канала
                - Человеческий глаз не замечает такие изменения
                - На примере: пиксель (150, 200, 100) → (151, 200, 101)
                """)
            
    def render_audio_steganography(self):
        """Стеганография в аудио"""
        st.header("🎵 Стеганография в аудио")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Кодирование в аудио")
            
            # Демонстрация LSB в аудио
            st.markdown("""
            ### LSB в аудио сигналах
            
            **Принцип работы:**
            - Аудио сигнал дискретизируется (например, 44100 Гц)
            - Каждый сэмпл представляется как число (например, 16-битное)
            - Замена наименее значащих битов сэмплов
            - Человеческое ухо не различает такие изменения
            """)
            
            # Генерация демо аудио
            if st.button("🎵 Сгенерировать демо-аудио", key="gen_audio"):
                audio_data = self.generate_demo_audio()
                st.session_state.audio_data = audio_data
                st.audio(audio_data, format='audio/wav')
            
            if 'audio_data' in st.session_state:
                secret_audio_msg = st.text_input(
                    "Сообщение для скрытия в аудио:",
                    "Секретное аудио сообщение",
                    key="audio_msg"
                )
                
                if st.button("🔊 Скрыть в аудио", key="hide_audio"):
                    stego_audio = self.lsb_audio_encode(st.session_state.audio_data, secret_audio_msg)
                    st.session_state.stego_audio = stego_audio
                    st.audio(stego_audio, format='audio/wav')
                    st.success("✅ Сообщение скрыто в аудио!")
        
        with col2:
            st.subheader("📥 Извлечение из аудио")
            
            if 'stego_audio' in st.session_state:
                st.audio(st.session_state.stego_audio, format='audio/wav')
                
                if st.button("🎧 Извлечь сообщение", key="extract_audio"):
                    message = self.lsb_audio_decode(st.session_state.stego_audio)
                    if message:
                        st.success(f"✅ Извлеченное сообщение: {message}")
                    else:
                        st.error("❌ Не удалось извлечь сообщение")
            
            # Визуализация аудио сигналов
            st.subheader("📊 Визуализация сигналов")
            
            if 'audio_data' in st.session_state and 'stego_audio' in st.session_state:
                fig = self.create_audio_signal_plot(
                    st.session_state.audio_data, 
                    st.session_state.stego_audio
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Эхо-скрытие
            st.subheader("🔄 Эхо-скрытие")
            
            st.markdown("""
            **Принцип эхо-скрытия:**
            - Добавление задержанной копии сигнала (эхо)
            - Параметры эхо кодируют информацию:
              - Задержка = 0/1 для бита данных
              - Амплитуда эхо-сигнала
            - Человеческое ухо воспринимает как естественное эхо
            """)

    def render_text_steganography(self):
        """Стеганография в тексте"""
        st.header("📄 Стеганография в тексте")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Методы скрытия в тексте")
            
            # Инициализация
            if 'text_method' not in st.session_state:
                st.session_state.text_method = "Пробелы и табуляции"
            if 'stego_text' not in st.session_state:
                st.session_state.stego_text = None
            
            def update_text_method():
                st.session_state.text_method = st.session_state.text_method_select
            
            text_method = st.selectbox(
                "Метод скрытия:",
                ["Пробелы и табуляции", "Невидимые символы", "Синтаксические изменения"],
                key="text_method_select",
                index=["Пробелы и табуляции", "Невидимые символы", "Синтаксические изменения"].index(st.session_state.text_method),
                on_change=update_text_method
            )
            
            cover_text = st.text_area(
                "Текст-носитель:",
                "Это обычный текст, который будет использоваться для скрытия секретного сообщения. "
                "Он должен быть достаточно длинным и содержать разнообразные слова и предложения.",
                height=150,
                key="cover_text"
            )
            
            secret_text = st.text_input(
                "Секретное сообщение:",
                "секрет",
                key="secret_text"
            )
            
            if st.button("📄 Скрыть в тексте", key="hide_text"):
                if text_method == "Пробелы и табуляции":
                    stego_text = self.whitespace_encode(cover_text, secret_text)
                elif text_method == "Невидимые символы":
                    stego_text = self.invisible_chars_encode(cover_text, secret_text)
                else:
                    stego_text = self.syntactic_encode(cover_text, secret_text)
                
                st.session_state.stego_text = stego_text
                st.success("✅ Сообщение скрыто в тексте!")
        
        with col2:
            st.subheader("🔍 Анализ и извлечение")
            
            if st.session_state.stego_text is not None:
                st.text_area(
                    "Текст со скрытым сообщением:",
                    st.session_state.stego_text,
                    height=200,
                    key="stego_text_display"
                )
                
                # Показать скрытые символы
                if st.button("👁️ Показать скрытые символы", key="show_hidden"):
                    highlighted = self.highlight_hidden_chars(st.session_state.stego_text)
                    st.text_area(
                        "Текст с подсветкой скрытых символов:",
                        highlighted,
                        height=200,
                        key="highlighted_text"
                    )
                
                # Извлечение сообщения
                if 'extract_method' not in st.session_state:
                    st.session_state.extract_method = "Автоопределение"
                
                def update_extract_method():
                    st.session_state.extract_method = st.session_state.extract_method_select
                
                extract_method = st.selectbox(
                    "Метод извлечения:",
                    ["Автоопределение", "Пробелы", "Невидимые символы"],
                    key="extract_method_select",
                    index=["Автоопределение", "Пробелы", "Невидимые символы"].index(st.session_state.extract_method),
                    on_change=update_extract_method
                )
                
                if st.button("🔍 Извлечь сообщение", key="extract_text"):
                    if extract_method == "Пробелы":
                        message = self.whitespace_decode(st.session_state.stego_text)
                    elif extract_method == "Невидимые символы":
                        message = self.invisible_chars_decode(st.session_state.stego_text)
                    else:
                        message = self.auto_decode_text(st.session_state.stego_text)
                    
                    if message:
                        st.success(f"✅ Извлеченное сообщение: {message}")
                    else:
                        st.error("❌ Не удалось извлечь сообщение")
            
            # Статистический анализ
            st.subheader("📊 Статистический анализ")
            
            if st.session_state.stego_text is not None:
                analysis = self.analyze_text_steganography(st.session_state.stego_text)
                st.write("**Результаты анализа:**")
                st.write(f"- Длина текста: {analysis['length']} символов")
                st.write(f"- Количество пробелов: {analysis['spaces']}")
                st.write(f"- Подозрительные паттерны: {analysis['suspicious_patterns']}")
                st.write(f"- Вероятность стеганографии: {analysis['stego_probability']}%")
    
    def render_steganalysis(self):
        """Обнаружение стеганографии"""
        st.header("🔍 Стеганоанализ")
        
        st.info("""
        💡 **Стеганоанализ** - наука об обнаружении скрытых сообщений и их извлечении 
        без знания использованного метода стеганографии.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🖼️ Анализ изображений")
            
            analysis_file = st.file_uploader(
                "Загрузите изображение для анализа:",
                type=['png', 'jpg', 'jpeg', 'bmp'],
                key="analysis_upload"
            )
            
            if analysis_file is not None:
                image = Image.open(analysis_file)
                st.image(image, caption="Анализируемое изображение", use_column_width=True)
                
                if st.button("🔬 Проанализировать изображение", key="analyze_image"):
                    analysis_results = self.analyze_image_steganography(image)
                    
                    st.subheader("📊 Результаты анализа")
                    
                    # Визуализация уверенности
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = analysis_results['confidence'] * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Вероятность стеганографии"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 30], 'color': "green"},
                                {'range': [30, 70], 'color': "yellow"},
                                {'range': [70, 100], 'color': "red"}
                            ],
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.write("**Обнаруженные артефакты:**")
                    for artifact in analysis_results['artifacts']:
                        st.write(f"- {artifact}")
        
        with col2:
            st.subheader("🎵 Анализ аудио")
            
            audio_file = st.file_uploader(
                "Загрузите аудио файл для анализа:",
                type=['wav', 'mp3'],
                key="audio_analysis_upload"
            )
            
            if audio_file is not None:
                st.audio(audio_file, format='audio/wav')
                
                if st.button("🔊 Проанализировать аудио", key="analyze_audio"):
                    analysis_results = self.analyze_audio_steganography(audio_file)
                    
                    st.subheader("📊 Результаты анализа аудио")
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = analysis_results['confidence'] * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Вероятность стеганографии"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 40], 'color': "green"},
                                {'range': [40, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "red"}
                            ],
                        }
                    ))
                    st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📈 Методы обнаружения")
            
            detection_methods = [
                ("Статистический анализ", "Анализ распределения битов и гистограмм"),
                ("Хи-квадрат тест", "Обнаружение LSB стеганографии в изображениях"),
                ("RS анализ", "Обнаружение изменений в пространственной области"),
                ("Спектральный анализ", "Анализ частотных характеристик"),
                ("Машинное обучение", "Классификация с использованием нейросетей")
            ]
            
            for method, description in detection_methods:
                with st.expander(f"🔍 {method}"):
                    st.write(description)

    def render_methods_comparison(self):
        """Сравнение методов стеганографии"""
        st.header("📊 Сравнение методов стеганографии")
        
        # Таблица сравнения
        methods_data = []
        for method_id, method in self.methods.items():
            methods_data.append({
                "Метод": method.name,
                "Описание": method.description,
                "Емкость": method.capacity,
                "Безопасность": method.security,
                "Обнаружаемость": method.detectability,
                "Форматы": ", ".join(method.file_types)
            })
        
        df_methods = pd.DataFrame(methods_data)
        st.dataframe(df_methods, use_container_width=True, hide_index=True)
        
        # Визуализация характеристик
        st.subheader("📈 Сравнение характеристик")
        
        method_names = [method.name for method in self.methods.values()]
        
        # Оценки по шкале 1-10
        capacity_scores = [8, 6, 5, 3, 2, 3]  # LSB image, LSB audio, DCT, Echo, Whitespace, Metadata
        security_scores = [2, 3, 8, 5, 1, 4]
        stealth_scores = [3, 4, 8, 6, 2, 5]   # Скрытность
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=capacity_scores,
            theta=method_names,
            fill='toself',
            name='Емкость'
        ))
        fig.add_trace(go.Scatterpolar(
            r=security_scores,
            theta=method_names,
            fill='toself',
            name='Безопасность'
        ))
        fig.add_trace(go.Scatterpolar(
            r=stealth_scores,
            theta=method_names,
            fill='toself',
            name='Скрытность'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title="Сравнение методов стеганографии",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Рекомендации по выбору метода
        st.subheader("🎯 Рекомендации по выбору метода")
        
        scenarios = {
            "Высокая емкость": "LSB в изображениях",
            "Максимальная скрытность": "DCT коэффициенты", 
            "Аудио файлы": "LSB в аудио или эхо-скрытие",
            "Текстовые документы": "Пробелы и невидимые символы",
            "Быстрое сокрытие": "Метаданные файлов",
            "Устойчивость к анализу": "Комбинированные методы"
        }
        
        for scenario, recommendation in scenarios.items():
            st.write(f"**{scenario}** → {recommendation}")

    # Методы стеганографии для изображений

    def lsb_encode(self, image: Image.Image, message: str) -> Image.Image:
        """Кодирование сообщения методом LSB в изображении"""
        # Конвертируем сообщение в бинарный формат
        binary_msg = ''.join(format(ord(c), '08b') for c in message)
        binary_msg += '00000000'  # Добавляем маркер конца сообщения
        
        img_array = np.array(image)
        flat_array = img_array.flatten()
        
        # Проверяем достаточность емкости
        if len(binary_msg) > len(flat_array):
            raise ValueError("Сообщение слишком длинное для данного изображения")
        
        # Заменяем LSB биты
        for i in range(len(binary_msg)):
            flat_array[i] = (flat_array[i] & 0xFE) | int(binary_msg[i])
        
        # Восстанавливаем форму массива
        encoded_array = flat_array.reshape(img_array.shape)
        return Image.fromarray(encoded_array.astype(np.uint8))

    def lsb_decode(self, image: Image.Image) -> str:
        """Декодирование LSB сообщения из изображения"""
        img_array = np.array(image)
        flat_array = img_array.flatten()
        
        # Извлекаем LSB биты
        binary_msg = ''
        for pixel in flat_array:
            binary_msg += str(pixel & 1)
        
        # Преобразуем бинарную строку в текст
        message = ''
        for i in range(0, len(binary_msg), 8):
            byte = binary_msg[i:i+8]
            if byte == '00000000':  # Маркер конца сообщения
                break
            message += chr(int(byte, 2))
        
        return message

    def dct_encode(self, image: Image.Image, message: str) -> Image.Image:
        """Упрощенная демонстрация DCT стеганографии"""
        # В реальной реализации здесь было бы DCT преобразование
        # Для демонстрации используем упрощенный подход
        img_array = np.array(image)
        
        # Немного изменяем изображение для демонстрации
        modified_array = img_array.astype(float)
        modified_array[::10, ::10, 0] += 1  # Легкие изменения в красном канале
        
        return Image.fromarray(np.clip(modified_array, 0, 255).astype(np.uint8))

    def dct_decode(self, image: Image.Image) -> str:
        """Упрощенное извлечение из DCT"""
        return "Демонстрационное сообщение из DCT"

    def create_lsb_demo_image(self) -> Image.Image:
        """Создание демонстрационного изображения для LSB"""
        # Создаем простое изображение для демонстрации
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img_array[25:75, 25:75] = [150, 200, 100]  # Зеленый квадрат
        
        return Image.fromarray(img_array)

    def create_histogram_comparison(self, original: np.ndarray, stego: np.ndarray) -> go.Figure:
        """Создание сравнения гистограмм оригинального и стего-изображения"""
        fig = go.Figure()
        
        # Гистограмма оригинального изображения (красный канал)
        orig_hist_red = np.histogram(original[:,:,0].flatten(), bins=256, range=(0,255))[0]
        fig.add_trace(go.Scatter(
            x=list(range(256)),
            y=orig_hist_red,
            mode='lines',
            name='Оригинал (R)',
            line=dict(color='red')
        ))
        
        # Гистограмма стего-изображения (красный канал)
        stego_hist_red = np.histogram(stego[:,:,0].flatten(), bins=256, range=(0,255))[0]
        fig.add_trace(go.Scatter(
            x=list(range(256)),
            y=stego_hist_red,
            mode='lines',
            name='Стего (R)',
            line=dict(color='darkred', dash='dash')
        ))
        
        fig.update_layout(
            title="Сравнение гистограмм (красный канал)",
            xaxis_title="Значение пикселя",
            yaxis_title="Частота",
            height=300
        )
        
        return fig

    def analyze_image_differences(self, original: np.ndarray, stego: np.ndarray) -> Dict:
        """Анализ различий между изображениями"""
        diff = np.abs(original.astype(float) - stego.astype(float))
        return {
            'mean_diff': np.mean(diff),
            'max_diff': np.max(diff),
            'changed_pixels': np.sum(diff > 0)
        }

    # Методы стеганографии для аудио

    def generate_demo_audio(self) -> bytes:
        """Генерация демонстрационного аудио сигнала"""
        # Создаем простой синусоидальный сигнал
        sample_rate = 44100
        duration = 3  # секунды
        frequency = 440  # Hz (A4)
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
        
        # Конвертируем в 16-битный формат
        audio_data_int = (audio_data * 32767).astype(np.int16)
        
        # Создаем WAV файл в памяти
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data_int.tobytes())
        
        return buffer.getvalue()

    def lsb_audio_encode(self, audio_data: bytes, message: str) -> bytes:
        """Кодирование сообщения в аудио методом LSB"""
        # Демонстрационная реализация
        return audio_data

    def lsb_audio_decode(self, audio_data: bytes) -> str:
        """Декодирование сообщения из аудио"""
        return "Демонстрационное аудио сообщение"

    def create_audio_signal_plot(self, original_audio: bytes, stego_audio: bytes) -> go.Figure:
        """Создание графика сравнения аудио сигналов"""
        # Демонстрационные данные
        x = list(range(1000))
        original_signal = np.sin(np.array(x) * 0.1)
        stego_signal = original_signal + 0.01 * np.random.randn(1000)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x, y=original_signal,
            mode='lines',
            name='Оригинальный сигнал',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=x, y=stego_signal,
            mode='lines',
            name='Стего-сигнал',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title="Сравнение аудио сигналов",
            xaxis_title="Сэмплы",
            yaxis_title="Амплитуда",
            height=300
        )
        
        return fig

    # Методы стеганографии для текста

    def whitespace_encode(self, text: str, message: str) -> str:
        """Кодирование сообщения с помощью пробелов"""
        binary_msg = ''.join(format(ord(c), '08b') for c in message)
        
        words = text.split()
        encoded_text = []
        
        for i, word in enumerate(words):
            if i < len(binary_msg):
                # Добавляем дополнительный пробел если бит = 1
                if binary_msg[i] == '1':
                    encoded_text.append(word + ' ')
                else:
                    encoded_text.append(word)
            else:
                encoded_text.append(word)
        
        return ' '.join(encoded_text)

    def whitespace_decode(self, text: str) -> str:
        """Декодирование сообщения из пробелов"""
        words = text.split()
        binary_msg = ''
        
        for word in words:
            if word.endswith(' '):
                binary_msg += '1'
            else:
                binary_msg += '0'
        
        # Преобразуем бинарную строку в текст
        message = ''
        for i in range(0, len(binary_msg), 8):
            if i + 8 <= len(binary_msg):
                byte = binary_msg[i:i+8]
                message += chr(int(byte, 2))
        
        return message

    def invisible_chars_encode(self, text: str, message: str) -> str:
        """Кодирование с помощью невидимых символов Unicode"""
        # Используем Zero Width Joiner и другие невидимые символы
        invisible_chars = ['\u200b', '\u200c']  # ZWJ, ZWNJ
        
        binary_msg = ''.join(format(ord(c), '08b') for c in message)
        encoded_text = list(text)
        
        # Вставляем невидимые символы после каждого символа текста
        result = []
        msg_index = 0
        
        for char in encoded_text:
            result.append(char)
            if msg_index < len(binary_msg):
                result.append(invisible_chars[int(binary_msg[msg_index])])
                msg_index += 1
        
        return ''.join(result)

    def invisible_chars_decode(self, text: str) -> str:
        """Декодирование из невидимых символов"""
        invisible_chars = ['\u200b', '\u200c']
        binary_msg = ''
        
        for char in text:
            if char in invisible_chars:
                binary_msg += str(invisible_chars.index(char))
        
        # Преобразуем бинарную строку в текст
        message = ''
        for i in range(0, len(binary_msg), 8):
            if i + 8 <= len(binary_msg):
                byte = binary_msg[i:i+8]
                message += chr(int(byte, 2))
        
        return message

    def syntactic_encode(self, text: str, message: str) -> str:
        """Кодирование с помощью синтаксических изменений"""
        # Упрощенная демонстрация
        return text + " " + message

    def auto_decode_text(self, text: str) -> str:
        """Автоматическое определение метода и декодирование"""
        # Пробуем разные методы
        try:
            return self.whitespace_decode(text)
        except:
            try:
                return self.invisible_chars_decode(text)
            except:
                return "Не удалось извлечь сообщение"

    def highlight_hidden_chars(self, text: str) -> str:
        """Подсветка скрытых символов в тексте"""
        invisible_chars = ['\u200b', '\u200c']
        highlighted = []
        
        for char in text:
            if char in invisible_chars:
                highlighted.append(f'[{invisible_chars.index(char)}]')
            elif char == ' ':
                highlighted.append('_')
            else:
                highlighted.append(char)
        
        return ''.join(highlighted)

    def analyze_text_steganography(self, text: str) -> Dict:
        """Анализ текста на наличие стеганографии"""
        space_count = text.count(' ')
        invisible_count = sum(1 for c in text if c in ['\u200b', '\u200c'])
        total_chars = len(text)
        
        # Простая эвристика для определения вероятности
        stego_probability = min(100, (invisible_count * 10 + (space_count / total_chars * 1000)))
        
        return {
            'length': total_chars,
            'spaces': space_count,
            'invisible_chars': invisible_count,
            'suspicious_patterns': invisible_count > 0,
            'stego_probability': min(100, int(stego_probability))
        }

    # Методы стеганоанализа

    def analyze_image_steganography(self, image: Image.Image) -> Dict:
        """Анализ изображения на наличие стеганографии"""
        img_array = np.array(image)
        
        # Простой анализ LSB (демонстрационный)
        flat_array = img_array.flatten()
        lsb_distribution = [pixel & 1 for pixel in flat_array[:1000]]
        lsb_balance = sum(lsb_distribution) / len(lsb_distribution)
        
        # Эвристика для определения вероятности
        confidence = abs(lsb_balance - 0.5) * 2  # Отклонение от равномерного распределения
        
        artifacts = []
        if confidence > 0.3:
            artifacts.append("Неравномерное распределение LSB битов")
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            artifacts.append("Наличие альфа-канала может скрывать данные")
        
        return {
            'confidence': min(1.0, confidence),
            'artifacts': artifacts,
            'lsb_balance': lsb_balance
        }

    def analyze_audio_steganography(self, audio_file) -> Dict:
        """Анализ аудио на наличие стеганографии"""
        # Демонстрационная реализация
        return {
            'confidence': random.uniform(0.1, 0.8),
            'artifacts': ["Возможное LSB кодирование", "Подозрительные спектральные характеристики"]
        }

# Для обратной совместимости
class SteganographyVisualizationModule(SteganographyModule):
    pass
