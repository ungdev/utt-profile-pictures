FROM python:3

WORKDIR /usr/src/app

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir --upgrade pipenv && chmod -R g+rwx /.local

USER 54545645

COPY . .

RUN pipenv install

ENTRYPOINT ["tail", "-f", "/dev/null"]
