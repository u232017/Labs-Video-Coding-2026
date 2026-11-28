FROM python:3.12-slim

WORKDIR /app

FROM python:3.12-slim

RUN pip install --no-cache-dir "fastapi[standard]"

COPY main.py .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]