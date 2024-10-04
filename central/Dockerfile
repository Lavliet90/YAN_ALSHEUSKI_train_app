FROM python:3.9
WORKDIR /app
COPY requirements_central.txt .
RUN pip install --no-cache-dir -r requirements_central.txt
COPY . .
CMD ["python", "app.py"]
