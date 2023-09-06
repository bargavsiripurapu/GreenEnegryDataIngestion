# Use the official Python image from Docker Hub
FROM python:3.10

# Set environment variables (optional)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Collect static files (if required)
# RUN python manage.py collectstatic --noinput

# Expose the Django development server port (default: 8000)
EXPOSE 8000:8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
