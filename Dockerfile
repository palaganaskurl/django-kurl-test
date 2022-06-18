FROM python:3.9
WORKDIR /app
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
COPY ./ /app
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv --clear
RUN pipenv install --deploy --system
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
