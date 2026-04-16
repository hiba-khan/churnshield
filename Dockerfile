FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file from root to the container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else (this grabs your api/ and data/ folders)
COPY . .

# Start the API pointing to the main file inside the api folder
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]