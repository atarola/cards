# start with the Javascript Build
FROM node:16-alpine3.11 AS webpack
COPY ./src/js /build
WORKDIR /build
RUN yarn install
RUN yarn run build

# setup the python build
FROM python:3.9.6-alpine3.13
COPY ./src/py /app
COPY --from=webpack /build/bin/bundle.js /app/static
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main.py"]
