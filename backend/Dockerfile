# FROM python:3.11

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# ENV PYTHONPATH=/app/src

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
# FROM python:3.10

# # WORKDIR /app
# WORKDIR /app/src


# COPY backend/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
