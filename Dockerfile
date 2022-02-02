FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip && pip install --upgrade pipenv && pipenv install

ENTRYPOINT ["tail", "-f", "/dev/null"]
