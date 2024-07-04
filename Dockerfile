# Используем официальный образ Python версии 3.9 в качестве базового
FROM python:3.12.4

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Создаем виртуальную среду и устанавливаем зависимости
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для использования виртуальной среды
ENV PATH="/opt/venv/bin:$PATH"

# Запускаем бота
CMD ["python", "hookahBOT.py"]
