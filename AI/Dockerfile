FROM python:3.10-slim
WORKDIR /app
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]