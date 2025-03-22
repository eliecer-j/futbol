FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Playwright y navegadores
RUN playwright install chromium --with-deps

COPY . .

CMD ["python", "tu_script.py"]
