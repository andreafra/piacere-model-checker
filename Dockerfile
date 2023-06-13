FROM python:3.11.3-buster AS requirements-stage

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./mc_openapi /code/mc_openapi
COPY ./tests /code/tests

EXPOSE 80

CMD ["uvicorn", "mc_openapi.api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
