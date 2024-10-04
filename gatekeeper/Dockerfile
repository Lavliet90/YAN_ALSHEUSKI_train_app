FROM python:3.9
WORKDIR /app
COPY requirements_gatekeeper.txt .
RUN pip install --no-cache-dir -r requirements_gatekeeper.txt
COPY . .
CMD ["python", "app.py"]
