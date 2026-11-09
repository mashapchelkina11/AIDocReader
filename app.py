import numpy as np
from PIL import Image
import easyocr
import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Wabi-Sabi",
    page_icon="🍵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Кастомный CSS: спокойные тона, много воздуха, тонкие линии
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@300;400&family=Noto+Sans+JP:wght@300;400&display=swap');

        /* Фон цвета рисовой бумаги */
        .stApp {
            background-color: #f5f2eb;
        }

        /* Базовые шрифты */
        html, body, [class*="css"] {
            font-family: 'Noto Sans JP', sans-serif;
            color: #4a4a4a;
        }

        h1, h2, h3, h4 {
            font-family: 'Noto Serif JP', serif !important;
            font-weight: 300 !important;
            color: #2c2c2c !important;
            letter-spacing: 2px;
        }

        /* Медленное чтение: увеличиваем межстрочный интервал */
        p, span, label, div {
            font-size: 1.05rem;
            line-height: 1.8;
            letter-spacing: 1px;
            color: #4a4a4a !important;
        }

        /* Контейнер с большими отступами (воздух) */
        .block-container {
            max-width: 700px;
            padding-top: 4rem;
            padding-bottom: 4rem;
        }

        /* Шапка */
        .zen-header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .zen-title {
            font-family: 'Noto Serif JP', serif;
            font-size: 2.5rem;
            font-weight: 300;
            color: #2c2c2c;
            margin-bottom: 0.5rem;
        }

        .zen-kanji {
            font-size: 1.2rem;
            color: #8a8a8a;
            letter-spacing: 5px;
            text-transform: uppercase;
        }

        .zen-divider {
            width: 40px;
            height: 1px;
            background-color: #c0b8a8;
            margin: 1.5rem auto;
        }

        /* Тонкая рамка загрузки */
        div[data-testid="stFileUploader"] {
            background-color: transparent;
            border: 1px solid #d4ccc0;
            padding: 1.5rem;
            border-radius: 0;
        }

        div[data-testid="stFileUploader"] button {
            background-color: transparent !important;
            color: #4a4a4a !important;
            border: 1px solid #4a4a4a !important;
            border-radius: 0 !important;
            font-family: 'Noto Sans JP', sans-serif !important;
            padding: 0.4rem 1.2rem !important;
            transition: all 0.3s ease;
        }

        div[data-testid="stFileUploader"] button:hover {
            background-color: #4a4a4a !important;
            color: #f5f2eb !important;
        }

        /* Вкладки */
        div[data-testid="stTabs"] button {
            font-family: 'Noto Serif JP', serif;
            font-size: 1rem;
            color: #8a8a8a;
            border-bottom: 1px solid transparent;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #2c2c2c;
            border-bottom: 1px solid #2c2c2c;
        }

        /* Строки текста */
        .zen-text {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1.05rem;
            line-height: 2;
            color: #3a3a3a !important;
            padding: 0.5rem 0;
            border-bottom: 1px dotted #d4ccc0;
        }

        .zen-text:last-child {
            border-bottom: none;
        }

        /* Информация о сохранении */
        .zen-note {
            text-align: center;
            font-size: 0.9rem;
            color: #8a8a8a;
            margin-top: 2rem;
            font-style: italic;
        }

        /* Скрываем лишнее */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Шапка
st.markdown(
    """
    <div class="zen-header">
        <div class="zen-kanji">侘寂</div>
        <div class="zen-title">Wabi-Sabi</div>
        <div class="zen-divider"></div>
        <p style="color: #8a8a8a; font-size: 0.95rem;">Красота в простоте. Распознавание текста.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Загрузка модели
@st.cache_resource(show_spinner=False)
def load_zen_engine():
    return easyocr.Reader(['ru', 'en'], gpu=False)

engine = load_zen_engine()

# Зона загрузки
uploaded = st.file_uploader(
    "Выберите изображение (JPG, PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded:
    image = Image.open(uploaded)
    
    # Создаем вкладки для разделения картинки и текста
    tab1, tab2 = st.tabs(["🖼️ Исходное изображение", "📜 Распознанный текст"])
    
    with tab1:
        st.image(image, use_container_width=True)
        
    with tab2:
        with st.spinner("Медитативное чтение..."):
            img_array = np.array(image)
            result_lines = engine.readtext(img_array, detail=0)
            
        if result_lines:
            for line in result_lines:
                st.markdown(f'<div class="zen-text">{line}</div>', unsafe_allow_html=True)
            
            # Сохранение
            save_path = f"wabi_sabi_{uploaded.name}.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write("\n".join(result_lines))
            
            st.markdown(
                f'<div class="zen-note">Текст сохранен в файл: {save_path}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<p style="color: #a88888; text-align: center;">Пустота. Текст не найден.</p>',
                unsafe_allow_html=True
            )