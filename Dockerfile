FROM ubuntu:latest
LABEL authors="Владислав Невольский"

ENTRYPOINT ["top", "-b"]
FROM python:3.10.18

# Устанавливаем системные зависимости для OpenCV и графических инструментов
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем файлы приложения и модель
COPY streamlitesrgan.py /app/streamlitesrgan.py
COPY proverka.py /app/proverka.py
COPY weights/net_g_85000.pth /app/weights/net_g_85000.pth
COPY realesrgan/utils.py /app/realesrgan/utils.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт для Streamlit
EXPOSE 8501

# Запускаем Streamlit-приложение
CMD ["streamlit", "run", "streamlitesrgan.py", "--server.port=8501", "--server.address=0.0.0.0"]