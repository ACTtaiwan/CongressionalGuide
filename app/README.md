This Docker container is based on the [Official Node JS Docker container](https://hub.docker.com/_/node/). Before doing anything here, we recommend you have gone through the [Dockerizing a Node.js web app tutorial](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/).

## Build the Docker Node.js image 
`$ docker build -t acttaiwan/cgapp .`

## Run the Docker Container
`$ docker run -it --rm -p 49160:3000 --name cgapp acttaiwan/cgapp`

### Local Directory
If you are running locally where you are changing and working with the code, run the container via:
`$ docker run -it --rm -p 49160:3000 -v "$PWD":/opt/app acttaiwan/cgapp /bin/bash`

* The -v option mounts the current directory you are in to the container, any changes made in this directory will immediately be available.
* You will be dropped into the `/opt/app` directory where you can run commands. Changes that are then made to this directly will all change the directly locally.
* You can run commands such as `node server.js`
* Note you may need to run `npm install` to install nodejs dependencies locally.

## Interaction with the Container or Code
Access the running acttaiwan/cgapp Container bash shell to interact live with both data and running processes
`$ docker exec -it cgapp /bin/bash`