# using https://hub.docker.com/_/node/
FROM node:6.2.0-wheezy

# default port - may need to update for non-testing
EXPOSE 8888

ADD package.json /usr/src/app/package.json
RUN npm install