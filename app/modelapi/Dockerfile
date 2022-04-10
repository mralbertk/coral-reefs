FROM python:3.10.4-slim
LABEL author="akonrad - albert.konrad@edu.dsti.institute"
COPY . /fastapi
RUN mkdir storage && cd storage && mkdir export && mkdir preview
WORKDIR ../fastapi
RUN python3 -m pip install -r requirements-docker.txt
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0
