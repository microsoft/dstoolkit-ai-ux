FROM python:3.9

ADD app/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app

WORKDIR /app

ENV PORT 8081
EXPOSE 8081

ENTRYPOINT ["gunicorn", "--timeout", "600", "--access-logfile", "'-'", "--error-logfile", "'-'", "app:app"]
