FROM python:3.9

ADD app/requirements.txt ./
RUN pip install -r requirements.txt

COPY app app

WORKDIR /app

EXPOSE 8080:8080/udp
EXPOSE 8080:8080/tcp

ENTRYPOINT [ "streamlit", "run", "dashboard.py", "--server.port", "8080" ]
