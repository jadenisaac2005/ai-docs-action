# Dockerfile
FROM python:3.9-slim

# Copy the Python script and requirements into the container
COPY generate_docs.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint for the action
ENTRYPOINT ["python", "/generate_docs.py"]
