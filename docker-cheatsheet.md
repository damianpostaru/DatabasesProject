## Deeply with docker-compose
### Start all containers
    docker-compose up -d
### Rebuild
    docker-compose build
### Rebuild and start all containers
    docker-compose up --build

###
### docker container logs
    docker logs home-core --tail 200 -f
### build docker image
    docker build -t home-core .
#### and run the new built image
    docker run --name home-core -d -p 8010:8010 home-core
### Enter the running container
    docker exec -ti home-core /bin/bash


### Useful docker commands
#### Show running containers
    docker ps

#### Stop a container
    docker stop <CONTAINER_NAME_OR_ID>
    
#### Show all containers
    docker container ls -a
    
#### Remove a container
    docker container rm <CONTAINER_NAME_OR_ID>
    
#### Start a container
    docker start <CONTAINER_NAME_OR_ID>

#### Remove all images which are not used by existing containers
    docker image prune -a

#### Remove all stopped containers
    docker container prune

## To solve this issue 
## Error response from daemon: cannot stop container: ...: Cannot kill container ...: unknown error after kill: runc did not terminate sucessfully: container_linux.go:392: signaling init process caused "permission denied": unknown
## run:
    sudo aa-remove-unknown

##
    docker login --username iulianpostaru --password mR%VWqhstR9-7Ng

###### Others
#### https://stackoverflow.com/questions/47223280/docker-containers-can-not-be-stopped-or-removed-permission-denied-error/56134376#56134376


docker logs home-core --tail 200 -f
docker exec -ti home-core /bin/bash
