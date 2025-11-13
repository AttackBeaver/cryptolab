from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import binascii

class DigitalSignatureModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Электронные подписи"
        self.description = "Аутентификация и целостность цифровых документов"
        self.category = "protocols"
        self.icon = ""
        self.order = 3
    
    def render(self):
        st.title("🖊️ Электронные подписи")
        st.subheader("Аутентификация и целостность цифровых документов")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Цифровые подписи
            
            **Принцип работы:**
            1. **Генерация ключей** - создается пара ключей (приватный и публичный)
            2. **Подписание** - отправитель хеширует документ и шифрует хеш своим приватным ключом
            3. **Проверка** - получатель расшифровывает подпись публичным ключом и сравнивает с хешем документа
            
            **Свойства цифровой подписи:**
            - **Аутентичность** - подтверждает личность подписанта
            - **Целостность** - гарантирует, что документ не изменен
            - **Неотрекаемость** - подписант не может отрицать подписание
            
            **Алгоритмы:**
            - **RSA-PSS** - современная схема на основе RSA
            - **DSA** - Digital Signature Algorithm
            - **ECDSA** - Elliptic Curve DSA
            
            **Применения:**
            - Юридические документы
            - Обновления ПО
            - SSL/TLS сертификаты
            - Криптовалюты
            """)
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Создание и проверка подписи", "🎭 Атаки и подделка", "📊 Сравнение алгоритмов"],
            horizontal=True
        )
        
        if mode == "🔐 Создание и проверка подписи":
            self.render_signature_creation()
        elif mode == "🎭 Атаки и подделка":
            self.render_attacks_demo()
        else:
            self.render_algorithms_comparison()
    
    def render_signature_creation(self):
        """Режим создания и проверки подписи"""
        st.markdown("### 🔐 Создание и проверка электронной подписи")
        
        # Инициализация состояния
        if 'private_key' not in st.session_state:
            st.session_state.private_key = None
        if 'public_key' not in st.session_state:
            st.session_state.public_key = None
        if 'document_content' not in st.session_state:
            st.session_state.document_content = "Важный документ: Соглашение о сотрудничестве\nСумма: 100 000 руб.\nСрок: 30 дней"
        if 'signature' not in st.session_state:
            st.session_state.signature = None
        if 'document_hash' not in st.session_state:
            st.session_state.document_hash = None
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 1. Генерация ключей")
            
            if st.button("🔑 Сгенерировать ключи RSA", key="generate_keys"):
                with st.spinner("Генерирую ключи..."):
                    private_key = rsa.generate_private_key(
                        public_exponent=65537,
                        key_size=2048,
                    )
                    public_key = private_key.public_key()
                    
                    st.session_state.private_key = private_key
                    st.session_state.public_key = public_key
                    st.rerun()
            
            if st.session_state.private_key:
                st.success("✅ Ключи сгенерированы!")
                
                # Показываем информацию о ключах
                private_numbers = st.session_state.private_key.private_numbers()
                st.info(f"**Размер ключа:** 2048 бит")
                st.info(f"**Публичная экспонента:** 65537")
        
        with col2:
            st.markdown("#### 2. Документ для подписания")
            
            document = st.text_area(
                "Содержимое документа:",
                st.session_state.document_content,
                height=150,
                key="document_input"
            )
            st.session_state.document_content = document
            
            if st.session_state.private_key and st.button("🖊️ Подписать документ", key="sign_document"):
                with st.spinner("Подписываю документ..."):
                    # Вычисляем хеш документа
                    document_hash = hashlib.sha256(document.encode('utf-8')).digest()
                    st.session_state.document_hash = document_hash
                    
                    # Создаем подпись
                    signature = st.session_state.private_key.sign(
                        document_hash,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    
                    st.session_state.signature = signature
                    st.rerun()
        
        # Показываем результаты если подпись создана
        if st.session_state.signature:
            st.markdown("---")
            st.markdown("#### 3. Результаты подписания")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("**Подпись создана!**")
                signature_hex = binascii.hexlify(st.session_state.signature).decode()
                st.text_area("Цифровая подпись (HEX):", signature_hex[:128] + "...", height=100)
                st.info(f"**Размер подписи:** {len(st.session_state.signature)} байт")
            
            with col2:
                document_hash_hex = binascii.hexlify(st.session_state.document_hash).decode()
                st.text_area("Хеш документа (SHA-256):", document_hash_hex, height=100)
            
            # Проверка подписи
            st.markdown("---")
            st.markdown("#### 4. Проверка подписи")
            
            verification_document = st.text_area(
                "Документ для проверки:",
                st.session_state.document_content,
                height=150,
                key="verification_doc"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Проверить подпись", key="verify_signature"):
                    try:
                        # Вычисляем хеш проверяемого документа
                        verify_hash = hashlib.sha256(verification_document.encode('utf-8')).digest()
                        
                        # Проверяем подпись
                        st.session_state.public_key.verify(
                            st.session_state.signature,
                            verify_hash,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                        )
                        
                        st.success("🎉 Подпись действительна! Документ не изменен.")
                        
                    except InvalidSignature:
                        st.error("❌ Подпись недействительна! Документ был изменен.")
                    
                    except Exception as e:
                        st.error(f"❌ Ошибка проверки: {e}")
            
            with col2:
                if st.button("🔍 Проверить измененный документ", key="verify_modified"):
                    # Создаем измененный документ
                    modified_doc = verification_document + "\n[ИЗМЕНЕНО]"
                    st.text_area("Измененный документ:", modified_doc, height=150, key="modified_doc")
                    
                    try:
                        verify_hash = hashlib.sha256(modified_doc.encode('utf-8')).digest()
                        st.session_state.public_key.verify(
                            st.session_state.signature,
                            verify_hash,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                        )
                        st.error("❌ ОШИБКА: Подпись должна быть недействительной!")
                    except InvalidSignature:
                        st.success("✅ Корректно: Подпись недействительна для измененного документа")
    
    def render_attacks_demo(self):
        """Режим демонстрации атак и подделки"""
        st.markdown("### 🎭 Атаки на электронные подписи")
        
        st.warning("""
        ⚠️ **Учебная демонстрация** 
        Эти атаки показывают важность защиты приватных ключей и использования надежных алгоритмов.
        """)
        
        # Инициализация состояния для атак
        if 'attack_private_key' not in st.session_state:
            st.session_state.attack_private_key = None
        if 'attack_public_key' not in st.session_state:
            st.session_state.attack_public_key = None
        if 'attack_document' not in st.session_state:
            st.session_state.attack_document = "Перевод: Alice → Bob: 1000 USD"
        if 'attack_signature' not in st.session_state:
            st.session_state.attack_signature = None
        
        attack_type = st.selectbox(
            "Выберите тип атаки:",
            ["Кража приватного ключа", "Подделка документа", "Атака повторного использования"]
        )
        
        if attack_type == "Кража приватного ключа":
            self.show_private_key_theft_attack()
        elif attack_type == "Подделка документа":
            self.show_document_forgery_attack()
        else:
            self.show_replay_attack()
    
    def show_private_key_theft_attack(self):
        """Демонстрация атаки кражи приватного ключа"""
        st.markdown("#### 🔓 Кража приватного ключа")
        
        if st.session_state.attack_private_key is None:
            # Генерируем ключи для демонстрации
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()
            
            st.session_state.attack_private_key = private_key
            st.session_state.attack_public_key = public_key
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👨 Алиса (законный пользователь)**")
            st.info("Приватный ключ защищен")
            
            document = st.text_input("Документ Алисы:", "Договор №123", key="alice_doc")
            
            if st.button("🖊️ Алиса подписывает", key="alice_sign"):
                document_hash = hashlib.sha256(document.encode('utf-8')).digest()
                signature = st.session_state.attack_private_key.sign(
                    document_hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                st.session_state.attack_signature = signature
                st.success("✅ Алиса подписала документ")
        
        with col2:
            st.markdown("**👤 Злоумышленник (украл ключ)**")
            st.error("Приватный ключ скомпрометирован!")
            
            malicious_doc = st.text_input("Поддельный документ:", "Договор №999", key="malicious_doc")
            
            if st.button("💀 Подписать чужим ключом", key="forged_sign"):
                if st.session_state.attack_private_key:
                    document_hash = hashlib.sha256(malicious_doc.encode('utf-8')).digest()
                    signature = st.session_state.attack_private_key.sign(
                        document_hash,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    st.error("💀 Подпись успешно подделана!")
                    st.warning("**Вывод:** Защита приватных ключей критически важна!")
        
        # Демонстрация проверки
        if st.session_state.attack_signature:
            st.markdown("---")
            st.markdown("#### 🔍 Проверка подписей")
            
            test_document = st.text_input("Документ для проверки:", "Договор №123", key="verify_test_doc")
            
            if st.button("🔎 Проверить подлинность", key="verify_authenticity"):
                try:
                    document_hash = hashlib.sha256(test_document.encode('utf-8')).digest()
                    st.session_state.attack_public_key.verify(
                        st.session_state.attack_signature,
                        document_hash,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    st.success("✅ Подпись действительна")
                except InvalidSignature:
                    st.error("❌ Подпись недействительна")
    
    def show_document_forgery_attack(self):
        """Демонстрация атаки подделки документа"""
        st.markdown("#### 📝 Подделка документа")
        
        st.info("""
        **Атака:** Злоумышленник пытается найти другой документ, который дает тот же хеш
        (коллизия хеш-функции), чтобы использовать существующую подпись.
        """)
        
        original_doc = st.text_area("Оригинальный документ:", 
                                   "Одобрить премию: 5000 руб.", 
                                   height=100,
                                   key="original_doc")
        
        forged_doc = st.text_area("Целевой поддельный документ:",
                                 "Одобрить премию: 50000 руб.",
                                 height=100,
                                 key="forged_doc_target")
        
        if st.button("🔍 Попытаться найти коллизию", key="find_collision"):
            with st.spinner("Ищу коллизию (учебная демонстрация)..."):
                # Упрощенная демонстрация
                original_hash = hashlib.sha256(original_doc.encode('utf-8')).hexdigest()
                forged_hash = hashlib.sha256(forged_doc.encode('utf-8')).hexdigest()
                
                st.markdown("**Результаты:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text_area("Хеш оригинала:", original_hash, height=100)
                
                with col2:
                    st.text_area("Хеш подделки:", forged_hash, height=100)
                
                if original_hash == forged_hash:
                    st.error("💀 Коллизия найдена! Атака успешна!")
                else:
                    st.success("✅ Коллизия не найдена. SHA-256 устойчив к таким атакам.")
                    
                    # Показываем различия
                    diff_count = self.count_hash_differences(original_hash, forged_hash)
                    st.info(f"**Хеши отличаются в {diff_count} из 64 шестнадцатеричных символов**")
    
    def show_replay_attack(self):
        """Демонстрация атаки повторного использования"""
        st.markdown("#### 🔁 Атака повторного использования")
        
        st.info("""
        **Атака:** Злоумышленник перехватывает подписанное сообщение и отправляет его повторно.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📨 Оригинальная транзакция**")
            original_tx = st.text_input("Транзакция:", "Перевод: Bob → Alice: 100 USD", key="original_tx")
            st.info("Подписана и отправлена")
        
        with col2:
            st.markdown("**🕵️ Повторная отправка**")
            st.text_input("Та же транзакция:", original_tx, key="replayed_tx", disabled=True)
            st.error("Злоумышленник повторяет транзакцию!")
        
        st.markdown("---")
        st.markdown("#### 🛡️ Защита от повторной атаки")
        
        protection_methods = {
            "Номер транзакции": "Каждая транзакция имеет уникальный номер",
            "Временная метка": "Подпись включает время создания",
            "Nonce": "Одноразовое случайное число в каждой подписи",
            "Счетчик": "Последовательный номер для каждой операции"
        }
        
        for method, description in protection_methods.items():
            with st.expander(f"✅ {method}"):
                st.write(description)
    
    def render_algorithms_comparison(self):
        """Режим сравнения алгоритмов подписи"""
        st.markdown("### 📊 Сравнение алгоритмов электронной подписи")
        
        algorithms_info = {
            "RSA-PSS": {
                "description": "RSA с вероятностной схемой подписи",
                "key_size": "2048-4096 бит",
                "security": "Высокая (при достаточном размере ключа)",
                "performance": "Средняя",
                "usage": "Широко распространен"
            },
            "DSA": {
                "description": "Digital Signature Algorithm",
                "key_size": "2048-3072 бит", 
                "security": "Высокая",
                "performance": "Быстрая подпись, медленная проверка",
                "usage": "Правительственные организации"
            },
            "ECDSA": {
                "description": "Elliptic Curve Digital Signature Algorithm",
                "key_size": "256-521 бит",
                "security": "Очень высокая",
                "performance": "Очень быстрая",
                "usage": "Криптовалюты, мобильные устройства"
            },
            "Ed25519": {
                "description": "Кривая Эдвардса",
                "key_size": "256 бит", 
                "security": "Очень высокая",
                "performance": "Очень быстрая",
                "usage": "Современные приложения"
            }
        }
        
        # Таца сравнения
        comparison_data = []
        for algo, info in algorithms_info.items():
            comparison_data.append({
                'Алгоритм': algo,
                'Описание': info['description'],
                'Размер ключа': info['key_size'],
                'Безопасность': info['security'],
                'Производительность': info['performance'],
                'Применение': info['usage']
            })
        
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
        
        # Визуализация
        st.markdown("---")
        st.markdown("#### 📈 Сравнительные характеристики")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        algorithms = list(algorithms_info.keys())
        
        # Безопасность (условные оценки)
        security_scores = [85, 80, 95, 95]  # RSA, DSA, ECDSA, Ed25519
        
        bars1 = ax1.bar(algorithms, security_scores, color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax1.set_title('Уровень безопасности')
        ax1.set_ylabel('Оценка (0-100)')
        ax1.set_ylim(0, 100)
        ax1.tick_params(axis='x', rotation=45)
        
        for bar, score in zip(bars1, security_scores):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{score}', ha='center', va='bottom')
        
        # Производительность (условные оценки)
        performance_scores = [70, 60, 90, 95]  # RSA, DSA, ECDSA, Ed25519
        
        bars2 = ax2.bar(algorithms, performance_scores, color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax2.set_title('Производительность')
        ax2.set_ylabel('Оценка (0-100)')
        ax2.set_ylim(0, 100)
        ax2.tick_params(axis='x', rotation=45)
        
        for bar, score in zip(bars2, performance_scores):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{score}', ha='center', va='bottom')
        
        # Размер ключа (максимальные значения)
        key_sizes = [4096, 3072, 521, 256]  # RSA, DSA, ECDSA, Ed25519
        
        bars3 = ax3.bar(algorithms, key_sizes, color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax3.set_title('Максимальный размер ключа (бит)')
        ax3.set_ylabel('Биты')
        ax3.tick_params(axis='x', rotation=45)
        
        for bar, size in zip(bars3, key_sizes):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{size}', ha='center', va='bottom')
        
        # Популярность (условные оценки)
        popularity = [90, 40, 80, 70]  # RSA, DSA, ECDSA, Ed25519
        
        bars4 = ax4.bar(algorithms, popularity, color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax4.set_title('Распространенность')
        ax4.set_ylabel('Оценка (0-100)')
        ax4.set_ylim(0, 100)
        ax4.tick_params(axis='x', rotation=45)
        
        for bar, pop in zip(bars4, popularity):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{pop}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Рекомендации
        st.markdown("---")
        st.markdown("#### 🎯 Рекомендации по выбору алгоритма")
        
        recommendations = [
            "**RSA-PSS**: Для совместимости с существующими системами",
            "**DSA**: Для правительственных и корпоративных систем", 
            "**ECDSA**: Для высокопроизводительных приложений и криптовалют",
            "**Ed25519**: Для новых проектов, где важна производительность и безопасность"
        ]
        
        for rec in recommendations:
            st.write(f"- {rec}")
    
    def count_hash_differences(self, hash1, hash2):
        """Считает количество различий между двумя хешами"""
        return sum(1 for a, b in zip(hash1, hash2) if a != b)