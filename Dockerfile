# Используем официальный образ Python версии 3.9 в качестве базового
FROM python:3.12.4

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости 
RUN pip install -r /app/requirements.txt
# Копируем все файлы проекта в рабочую директорию
COPY . .

# Определяем команду для запуска приложения
CMD ["python", "hookahBOT.py"]


