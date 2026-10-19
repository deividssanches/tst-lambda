FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY lambda_function.py app.py ./

EXPOSE 8080
# 2 workers, bind em 0.0.0.0
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]