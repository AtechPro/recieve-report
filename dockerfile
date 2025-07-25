# Use Python 3.11 slim image as base
FROM python:3.12.10-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV, Pillow, and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories (if not already present) and set ownership to appuser
RUN mkdir -p static/temp_images \
    static/temp_excel \
    static/images \
    generated_pdfs \
    stamp && \
    chown -R root:root static/temp_images static/temp_excel static/images generated_pdfs stamp

# Set environment variables
ENV FLASK_APP=recweb.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5300

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5300/ || exit 1

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5300", "--timeout", "120", "recweb:app"]
