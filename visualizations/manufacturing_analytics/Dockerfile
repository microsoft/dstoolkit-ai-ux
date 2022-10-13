FROM python:3.9

ADD app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app app

WORKDIR /app

ENV PORT 8081
EXPOSE 8081

ENTRYPOINT [ "streamlit", "run", "dashboard.py", "--server.port", "8080" ]
