FROM python:3.12.4

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt


COPY . .

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python", "hookahBOT.py"]
