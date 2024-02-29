FROM python:3.10.13-slim


WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY .env /app/

RUN python -c 'import os, dotenv; dotenv.load_dotenv(".env")'

EXPOSE 3000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
