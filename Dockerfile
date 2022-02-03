FROM python:3

WORKDIR /usr/src/app

USER 54545645

COPY . .

RUN pip install --user --upgrade pip && pip install --user --upgrade pipenv && pipenv install

ENTRYPOINT ["tail", "-f", "/dev/null"]
