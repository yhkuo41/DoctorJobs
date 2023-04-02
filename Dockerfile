FROM python:3.10-slim
WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

COPY ./*.py ./
COPY ./app ./app

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]