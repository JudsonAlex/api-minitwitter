
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    build-essential


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


# CMD ["python", "manage.py", "migrate","&&","python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN echo '#!/bin/sh\n\
python3 manage.py migrate\n\
exec python3 manage.py runserver 0.0.0.0:8000' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Use o script de entrada
ENTRYPOINT ["/entrypoint.sh"]

