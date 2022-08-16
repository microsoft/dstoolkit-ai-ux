FROM python:3.8-slim

COPY app app

WORKDIR /app

ENV PORT 3000
EXPOSE 3000

# WORKDIR /app
# COPY . .
RUN pip install -r requirements.txt
CMD ["python", "server.py"]