# syntax=docker/dockerfile:1

## Python env settings
# Create a new build stage from a python base image.
# (it is a big image, used for installing a venv with all dev dependencies needed)
FROM python:3.10.11-buster as builder
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

## Poetry settings
# Because Poetry is the dependency Manager, make sure it is installed
RUN pip install poetry==1.4.2
# Cleaning Poetry cache
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# set WORKDIR env var explicitly to avoid unintended operations in unknown directories
WORKDIR /app

COPY pyproject.toml poetry.lock ./
# create an empty README.md file for satisfying poetry requirement...
RUN touch README.md

# Install the project in the venv without installing development dependencies
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment 
# with the minimal dependencies
FROM python:3.10.11-slim-buster as runtime

# Poetry isn’t useful at runtime stage (venv is built). 
# Setting VIRTUAL_ENV variable to let Python recognize the right virtual environment.
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the source code into the container but just the necessary
COPY . ./app

# set the project’s entrypoint
# ENTRYPOINT ["python", "-m", "mountain_peaks.main"]

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD cd ./app/mountain-peaks ; uvicorn --reload main:app --host=0.0.0.0 --port=8000
