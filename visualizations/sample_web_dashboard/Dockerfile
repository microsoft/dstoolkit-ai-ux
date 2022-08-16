FROM python:3.8-slim

COPY app app

WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install gunicorn
ENV PORT 3000
EXPOSE 3000

ENTRYPOINT ["gunicorn", "--timeout", "600", "--access-logfile", "'-'", "--error-logfile", "'-'", "app:app"]




