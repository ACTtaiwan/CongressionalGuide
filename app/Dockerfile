# using https://hub.docker.com/_/node/
FROM node:6.2.0-wheezy

# default port - may need to update for non-testing
EXPOSE 8888

ADD . /code
WORKDIR /code
ADD package.json
RUN npm install