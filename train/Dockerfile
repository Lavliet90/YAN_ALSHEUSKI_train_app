FROM python:3.9
WORKDIR /app
COPY requirements_train.txt .
RUN pip install --no-cache-dir -r requirements_train.txt
COPY . .
CMD ["python", "app.py"]
