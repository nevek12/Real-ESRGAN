import streamlit as st
from PIL import Image
from io import BytesIO
from get_image_4x import process_image_with_esrgan
import os

# Настройка страницы
st.set_page_config(
    page_title="Улучшение качества фото в 4 раза",
    page_icon="🖼️",
    layout="centered"
)

# Инициализация состояния сессии
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'original_filename' not in st.session_state:
    st.session_state.original_filename = None

# Заголовок и описание
st.title("🖼️ Улучшение качества фотографий в 4 раза")
st.markdown("""
### Добро пожаловать!
Это приложение использует нейросеть **REAL-ESRGAN** для улучшения качества ваших фотографий в **4 раза**.
""")
st.write("---")

# Форма загрузки изображения
uploaded_file = st.file_uploader(
    "Загрузите ваше изображение (JPG/PNG/WEBP):",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=False
)

# Сброс состояния при загрузке нового файла
if uploaded_file is not None:
    if st.session_state.original_filename != uploaded_file.name:
        st.session_state.processed_image = None
        st.session_state.original_filename = uploaded_file.name
    st.write("Файл успешно загружен")

    try:
        original_image = Image.open(uploaded_file)
        st.subheader("Ваше оригинальное изображение:")
        st.image(original_image, use_container_width=True)

        # Кнопка для запуска обработки
        if st.button("Улучшить качество (4x)", type="primary"):
            with st.spinner("обработка изображения, среднее время ожидания ~5 минут..."):
                enhanced_image = Image.fromarray(process_image_with_esrgan(original_image))
                st.session_state.processed_image = enhanced_image

            # Отображение результата
            st.subheader("Результат улучшения:")
            st.image(st.session_state.processed_image, use_container_width=True)
            st.success(
                f"Размер улучшенного изображения: {st.session_state.processed_image.size[0]}x{st.session_state.processed_image.size[1]}")

        # Отображение кнопок скачивания, если есть обработанное изображение
        if st.session_state.processed_image is not None:
            base_name = os.path.splitext(uploaded_file.name)[0]

            st.subheader("Скачать в формате:")
            col1, col2, col3 = st.columns(3)

            # PNG
            with col1:
                png_buffer = BytesIO()
                st.session_state.processed_image.save(png_buffer, format="PNG")
                st.download_button(
                    label="PNG",
                    data=png_buffer.getvalue(),
                    file_name=f"{base_name}_enhanced.png",
                    mime="image/png",
                    key="png-download"
                )

            # JPEG
            with col2:
                jpeg_buffer = BytesIO()
                # Конвертируем в RGB, если изображение с альфа-каналом
                if st.session_state.processed_image.mode in ("RGBA", "P"):
                    rgb_image = st.session_state.processed_image.convert("RGB")
                    rgb_image.save(jpeg_buffer, format="JPEG", quality=95)
                else:
                    st.session_state.processed_image.save(jpeg_buffer, format="JPEG", quality=95)

                st.download_button(
                    label="JPEG",
                    data=jpeg_buffer.getvalue(),
                    file_name=f"{base_name}_enhanced.jpg",
                    mime="image/jpeg",
                    key="jpeg-download"
                )

            # WEBP
            with col3:
                webp_buffer = BytesIO()
                st.session_state.processed_image.save(webp_buffer, format="WEBP", quality=90)

                st.download_button(
                    label="WEBP",
                    data=webp_buffer.getvalue(),
                    file_name=f"{base_name}_enhanced.webp",
                    mime="image/webp",
                    key="webp-download"
                )

    except Exception as e:
        st.error(f"Ошибка обработки изображения: {str(e)}")
        st.exception(e)
else:
    st.session_state.processed_image = None
    st.session_state.original_filename = None
    st.info("👆 Пожалуйста, загрузите изображение для улучшения качества")

# Информация в футере
st.write("---")
st.markdown("""
### Процесс обработки:
1. Ваше изображение передается напрямую в обработчик
2. Запускается обработка вашего изображения дообученой на датасете Flickr2K нейросети Real_ESRGAN
3. Результат возвращается из временной памяти
4. Обработанное изображение отображается для скачивания в форматах jpg png webp
""")