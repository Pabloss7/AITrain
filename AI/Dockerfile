FROM python:3.10-slim
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "src.fastapi_server:app", "--host", "0.0.0.0", "--port", "5000"]