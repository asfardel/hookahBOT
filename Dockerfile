# Используем официальный образ Python
FROM python:3.12.4

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Запускаем бота
CMD ["python", "hookahBOT.py"]

