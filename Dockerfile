# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster


COPY . /app
RUN pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python","mapper/mapper.py"]
