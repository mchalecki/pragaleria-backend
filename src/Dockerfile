FROM python:3.7.0-slim
WORKDIR opt
COPY * /opt/

ENV PYTHONPATH /opt

RUN pip install --upgrade pip
RUN pip install pipenv==2018.6.25
RUN pip install pip==18.0
RUN pipenv install --system

CMD ["python","run.py"]