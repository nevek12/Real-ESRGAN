FROM ubuntu:latest
LABEL authors="Владислав Невольский"

ENTRYPOINT ["top", "-b"]
FROM python:3.10.18

# Устанавливаем системные зависимости для OpenCV и графических инструментов
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip3 install torch torchvision torchaudio

# Применение патчей для basicsr
RUN find /usr/local/lib/python3.10/site-packages/basicsr -name "*.py" -exec sed -i "s/from torchvision.transforms.functional_tensor/from torchvision.transforms.functional/g" {} \;
RUN sed -i "s/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/" /usr/local/lib/python3.10/site-packages/basicsr/data/degradations.py

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
CMD ["streamlit", "run", "streamlitesrgan.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]