This Docker container is based on the [Official Node JS Docker container](https://hub.docker.com/_/node/).

## Build the Docker Node.js image 
`$ docker build -t cgapp .`

## Run the Docker Container
`$ docker run -it --rm --name cgapp cgapp`

## Interaction with the Container or Code
Access the running kosahappbundle Container bash shell to interact live with both data and running processes
`$ docker exec -it cgapp bash`