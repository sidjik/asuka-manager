#stop containers
docker container stop ollama asuka postgresAsuka
docker container rm ollama asuka postgresAsuka

# delete network
docker network rm asukaNet

#delete volume
docker volume rm ollama asuka_datalayer asuka_app

# delete images
docker image rm asuka postgresasuka postgres:15.12-bookworm
