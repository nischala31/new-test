# Use full base image (larger attack surface, more OS vulns) instead of slim
FROM python:3.11

# Run as root (misconfiguration)
# USER nobody  # Commented out intentionally

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# Expose port
EXPOSE 5000

# Hardcoded secret in Dockerfile (secret detection)
ENV SECRET_PASSWORD=hardcoded_password_abc

CMD ["python", "app.py"]