FROM python:3.8.1

COPY . /opt/DatabasesProject/

WORKDIR /opt/DatabasesProject/

RUN pip install -r requirements.txt


ENTRYPOINT ["python3", "main.py"]