FROM python:3.7.0-slim
WORKDIR opt
COPY * /opt/

ENV PYTHONPATH /opt

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system

CMD ["python","run.py"]