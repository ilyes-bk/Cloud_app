FROM python:3.12

WORKDIR /app

# Copy requirements.txt from the backend directory
COPY ./Backend-app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY ./Backend-app /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "app.app"]