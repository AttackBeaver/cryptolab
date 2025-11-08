# 🔐 Интерактивная лаборатория криптографии

## Ссылка доступа: <https://cryptolab-spc.streamlit.app/>

🔐 CryptoLab - Siberian Professional College © 2025 *БПОУ ОО «Сибирский профессиональный колледж»* Преподаватель/разработчик: **Стариков А.В.**

## TODO

- Добавить подробную информацию о платформе
- Практичесие модули реализации "криптоатак" и алгоритмов
- Теория по криптографии
- Визуальная реализация некоторых шифров

## Структура приложения

``` txt
cryptolab/
│
├── app.py                     
├── requirements.txt
├── modules/
│   ├─── classical_ciphers/
│   │    ├── caesar.py
│   │    └── vigenere.py
│   ├─── cryptanalysis/
│   │    ├── frequency_analysis.py
│   │    └── vigenere_break.py
│   ├─── hash_functions/
│   │    └── hash_demo.py
│   ├─── modern_crypto/
│   │    └── rsa_visualizer.py
│   ├─── protocols/
│   │    ├── diffie_hellman.py
│   │    └── digital_signature.py
│   └─── base_module.py
└── utils/
    └─── module_loader.py
```

## Запуск проекта

1. Клонировать репозиторий или скачать проект.
2. Создать и активировать виртуальное окружение:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Запустить Streamlit-приложение:

   ```bash
   streamlit run app.py
   ```

После запуска в терминале появится ссылка, например:

``` txt
Local URL: http://localhost:8501
```

Открой её в браузере.
