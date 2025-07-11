import streamlit as st
from PIL import Image
from io import BytesIO
from proverka import process_image_with_esrgan
import os

# Настройка страницы
st.set_page_config(
    page_title="Улучшение качества фото в 4 раза",
    page_icon="🖼️",
    layout="centered"
)

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
if uploaded_file is not None:
    # Отображение оригинального изображения
    try:
        original_image = Image.open(uploaded_file)
        st.subheader("Ваше оригинальное изображение:")
        st.image(original_image, use_container_width=True)

        # Кнопка для запуска обработки
        if st.button("Улучшить качество (4x)", type="primary"):


                # Запускаем реальную обработку
                with st.spinner("Запуск REAL-ESRGAN..."):
                    enhanced_image = Image.fromarray(process_image_with_esrgan(original_image))




                # Отображение результата
                st.subheader("Результат улучшения:")
                st.image(enhanced_image, use_container_width=True)

                # Подготовка изображения для скачивания
                buffered = BytesIO()
                enhanced_image.save(buffered, format="PNG")

                # Кнопка скачивания
                st.download_button(
                    label="Скачать улучшенное изображение",
                    data=buffered.getvalue(),
                    file_name=f"enhanced_{uploaded_file.name}",
                    mime="image/png",
                    type="primary"
                )

                st.success(f"Размер улучшенного изображения: {enhanced_image.size[0]}x{enhanced_image.size[1]}")


    except Exception as e:
        st.error(f"Ошибка обработки изображения: {str(e)}")
else:
    st.info("👆 Пожалуйста, загрузите изображение для улучшения качества")

# Информация в футере
st.write("---")
st.markdown("""
### Процесс обработки:
1. Ваше изображение передается напрямую в обработчик
2. Запускается команда:
   ```bash
   python inference_realesrgan.py -n net_g_85000.pth -i [temp] -o [temp] --outscale 4
Результат возвращается из временной памяти

Обработанное изображение отображается для скачивания

Технология: REAL-ESRGAN - современная нейросеть для улучшения изображений
""")