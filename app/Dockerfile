# using https://hub.docker.com/_/node/
FROM node:6.2.0-wheezy

# use changes to package.json to force Docker not to use the cache
# when we change our application's nodejs dependencies:
ADD package.json /tmp/package.json
RUN cd /tmp && npm install

# Create app directory
RUN mkdir -p /opt/app && cp -a /tmp/node_modules /opt/app/

# From here we load the application's code in, therefore the previous docker
# "layer" thats been cached will be used if possible
WORKDIR /opt/app
# Bundle app source
ADD . /opt/app

# default ports
# testing
EXPOSE 8080
# express
EXPOSE 3000

# basic npm start which will run node server.js to start the server
CMD [ "npm", "start" ]
