FROM python:3

WORKDIR /usr/src/app

COPY scrapers scrapers/
COPY pyproject.toml ./
COPY poetry.lock ./

RUN pip install poetry 
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root

CMD python ./scrapers/asktheeu.py
