# Use the official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code into the image
COPY app.py .

# Expose the port where the app runs
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]