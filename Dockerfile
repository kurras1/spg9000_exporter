FROM python:3.12-slim

ENV SPG9000_Exporter_Debug_Mode=False

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "SPG9000_Exporter_HTTP.py"]
