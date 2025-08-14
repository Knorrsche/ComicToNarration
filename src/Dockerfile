FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /app

EXPOSE 8000
