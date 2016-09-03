[Docker Compose](https://docs.docker.com/compose/overview/) is used to building and running the two containers which make up the Congressional Guide service.

## Start
Clone the [ACTtaiwan/CongressionalGuide](https://github.com/ACTtaiwan/CongressionalGuide) to your local drive. To make things easier with Git (unless you are a command line pro), use one of the free Git GUIs:  
* [GitHub Desktop](https://desktop.github.com/)  
* [Sourcetree](https://www.sourcetreeapp.com/)  

### Build & Run
Execute the below command in the root Congressional Guide project folder
`$ docker-compose up`

Access the running webpage at `http://localhost:49170/`

This will drop you into the running services so you can observe the log. To quit, `$ docker-compose down`.

Use `$ docker-compose up -d` to containers in the background. 

### Rebuild
After you make any changes to the code, rebuild with
`$ docker-compose build`

## Containers
### App
The `app` Docker container is based on the [Official Node JS Docker container](https://hub.docker.com/_/node/). The [Dockerizing a Node.js web app tutorial](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/) is a good starting point for understanding how things work in this container.

#### Interaction with the Container or Code
Access the running acttaiwan/cgapp Container bash shell to interact live with both data and running processes
`$ docker exec -it cgapp /bin/bash`

### phpLiteAdmin
phpLiteAdmin is a web-based SQLite database admin tool written in PHP with support for SQLite3. This is used to directly access the data and make updates for adding questionnaire answers for the candidates. Access the admin page at http://localhost:2015/phpliteadmin.php.

## SQLite DB
The SQLite DB is mounted inside the containers from `/db/db.sqlite3`. You can interact directly with the DB on your local drive and those changes should show in the app.

## Candidate Information
The candidate information comes from the Scrapy spiders and is run manually to update and populate the DB. See the [Scrapy Readme](app/candidates/SCRAPY_README.md) for details.
