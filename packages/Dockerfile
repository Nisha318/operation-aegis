# Skyline Financial Tech — Demo API container
# NOTE: intentionally uses a non-slim base image and runs as root
# for Trivy image scanning demonstration.

FROM python:3.11

# VULN-007: Running as root (detected by Trivy / Checkov)
# A hardened image would add a non-root user here.
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# VULN-008: Exposing debug port and running with default uvicorn reload
# not appropriate for production
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
