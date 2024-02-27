FROM python:3.10.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10.11
WORKDIR /app/Mountain-Peaks
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY mountain_peaks .
COPY tests .
EXPOSE 8000
