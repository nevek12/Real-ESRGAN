# Используем официальный образ Python
FROM python:3.10.18-slim

# Метаданные
LABEL authors="Владислав Невольский"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install torch torchvision torchaudio

# Применение патчей для basicsr
RUN find /usr/local/lib/python3.10/site-packages/basicsr -name "*.py" -exec sed -i "s/from torchvision.transforms.functional_tensor/from torchvision.transforms.functional/g" {} \;
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/g" /usr/local/lib/python3.10/site-packages/basicsr/data/degradations.py

# Копируем файлы приложения
COPY streamlitesrgan.py .
COPY get_image_4x.py .
COPY weights/net_g_85000.pth ./weights/net_g_85000.pth
COPY realesrgan/utils.py ./realesrgan/utils.py

# Создаем и настраиваем директорию для Streamlit
RUN mkdir -p /.streamlit && \
    chmod -R 777 /.streamlit

# Устанавливаем переменные окружения для Streamlit
ENV STREAMLIT_GLOBAL_CONFIG_PATH=/.streamlit/config.toml
ENV STREAMLIT_GENERATED_CONFIG_PATH=/.streamlit/generated
ENV STREAMLIT_USER_CONFIG_PATH=/.streamlit/user
ENV STREAMLIT_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_STATIC_SERVING=false

# Создаем базовый конфиг
RUN echo "[server]\nport = 8501\naddress = '0.0.0.0'\nheadless = true\nmaxUploadSize = 3\n" > /.streamlit/config.toml

# Открываем порт
EXPOSE 8501

# HEALTHCHECK для Streamlit
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Команда запуска
CMD ["streamlit", "run", "streamlitesrgan.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false", "--server.enableCORS=false"]