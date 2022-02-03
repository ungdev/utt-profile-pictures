FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install --upgrade pipenv

USER 54545645

COPY . .

RUN pipenv install

ENTRYPOINT ["tail", "-f", "/dev/null"]
