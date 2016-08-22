[Docker Compose](https://docs.docker.com/compose/overview/) is used to building and running the two containers which make up the Congressional Guide service.

## Start
Clone the [ACTtaiwan/CongressionalGuide](https://github.com/ACTtaiwan/CongressionalGuide) to your local drive. To make things easier with Git (unless you are a command line pro), use one of the free Git GUIs:  
* [GitHub Desktop](https://desktop.github.com/)  
* [Sourcetree](https://www.sourcetreeapp.com/)  

### Build & Run
Execute the below command in the root Congressional Guide project folder
`$ docker-compose up`

Access the running webpage at `http://localhost:49160/`

This will drop you into the running services so you can observe the log. To quit, `$ docker-compose down`.

Use `$ docker-compose up -d` to containers in the background. 

### Rebuild
After you make any changes to the code, rebuild with
`$ docker-compose build`

## Containers
### App
The `app` Docker container is based on the [Official Node JS Docker container](https://hub.docker.com/_/node/). The [Dockerizing a Node.js web app tutorial](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/) is a good starting point for understanding how things work in this container.

### Interaction with the Container or Code
Access the running acttaiwan/cgapp Container bash shell to interact live with both data and running processes
`$ docker exec -it cgapp /bin/bash`

## SQLite DB
The SQLite DB is mounted inside the containers from `/db/db.sqlite3`. You can interact directly with the DB on your local drive and those changes should show in the app.