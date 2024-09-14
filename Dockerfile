FROM python:3.11

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

ENV PIPENV_VENV_IN_PROJECT=1

RUN pipenv install

COPY ./app .

CMD ["pipenv", "run", "python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"] 