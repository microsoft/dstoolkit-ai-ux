FROM python:3.9

ADD app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app app

WORKDIR /app

ENV PORT 80
EXPOSE 8080:80

ENTRYPOINT [ "streamlit", "run", "dashboard.py", "--server.port", "8080" ]
