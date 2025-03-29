if [ "$(whoami)" = "root" ]; then
  SUDO="sudo"
else
  SUDO=""
fi



# download needeable image
docker pull ollama/ollama:latest


# create volume for ollama if not already exists
echo -n 'INFO: Create volume with ID(name:asuka)...  '
if docker volume ls -q | grep ollama > /dev/null 2>&1; then 
    echo 'volume already exist'
else 
    docker volume create ollama
fi

# create volume for postgres if not already exists
echo -n 'INFO: Create volume with ID(name:asuka)...  '
if docker volume ls -q | grep asuka_datalayer > /dev/null 2>&1; then 
    echo 'volume already exist'
else 
    docker volume create asuka_datalayer
fi

# create volume for asuka app if not already exists
echo -n 'INFO: Create volume with ID(name:asuka)...  '
if docker volume ls -q | grep asuka_app > /dev/null 2>&1; then 
    echo 'volume already exist'
else 
    docker volume create asuka_app
fi



# create network for ollama and asuka communication
echo -n 'INFO: Create network with ID(name:asukaNet)...  '
if docker network ls | grep asukaNet > /dev/null 2>&1; then 
    echo 'network already exist'
else 
    docker network create asukaNet
fi


#. env/bin/activate


# setup configuration for ollama

if [ "$2" = "nvidia" ]; then
    if [ "$1" = "apt" ]; then
        curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
            | $SUDO gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
        curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
            | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
            | $SUDO tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
        $SUDO apt-get update
        
        $SUDO apt-get install -y nvidia-container-toolkit

    elif [ "$1" = "yum" || "$1" = "dnf"]; then
        curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo \
            |$SUDO tee /etc/yum.repos.d/nvidia-container-toolkit.repo
        if [ "$1" = "yum" ]; then
            $SUDO yum install -y nvidia-container-toolkit
        else [ "$1" = "dnf" ]: then
            $SUDO dnf install -y nvidia-container-toolkit

        fi
    fi 
    $SUDO nvidia-ctk runtime configure --runtime=docker
    $SUDO systemctl restart docker

    echo -n 'INFO: Runnin ollama container with ID...  '
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 \
        --network asukaNet \
        --restart unless-stopped \
        --name ollama ollama/ollama:latest

elif [ "$2" = 'amd' ]; then
    echo -n 'INFO: Runnin ollama container with ID...  '
    docker run -d -v ollama:/root/.ollama -p 11434:11434 \
        --restart unless-stopped \
        --device /dev/kfd --device /dev/dri \
        --network asukaNet \
        --name ollama ollama/ollama:rocm
    

else
    # run ollama container only on cpu
    echo -n 'INFO: Runnin ollama container with ID...  '
    docker run -d -v ollama:/root/.ollama -p 11434:11434 \
        --restart unless-stopped \
        --network asukaNet \
        --name ollama ollama/ollama:latest

fi

# download small model
docker exec -it ollama bash -c 'ollama pull llama3.2:1b'
docker exec -it ollama bash -c 'ollama pull qwen2.5:0.5b'
docker exec -it ollama bash -c 'ollama pull qwen2:0.5b'



# setup postgres for asuka app dataalyer
# build custom image
echo -n 'INFO: Build docker image(custom postgres)... '
docker build --rm --no-cache -t postgresasuka:latest datalayer/.
# run this image on a system
echo -n 'INFO: Run this image with'
docker run -d -v asuka_datalayer:/var/lib/postgresql/data -p 5432:5432 \
    --restart unless-stopped \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    --network asukaNet \
    --name postgresAsuka postgresasuka:latest

echo -n 'INFO: Install prisma via npm... ' 
docker exec -it postgresAsuka bash -c 'npm install prisma@6.4.1 --save --global'
echo -n 'INFO: Run prisma... '
docker exec -it postgresAsuka bash -c 'prisma migrate deploy'



# build main asuka app image
docker build --rm --no-cache -t asuka:latest .

# run asuka app image
docker run -d -v asuka_app:/app/mask -p 8080:80 \
    --restart unless-stopped \
    --network asukaNet \
    --name asuka asuka:latest \

docker cp README.md asuka:/app/chainlit.md





# setup admin panel via tmux 
# install needeable package

$SUDO "$1" install btop tmux nvtop


# setup tmux
tmux new -d -s asuka_admin


# second window asuka stdout + nvtop
tmux new-window -t asuka_admin:1 -n "app+nvtop"
tmux split-window -h -t asuka_admin:1 
tmux send-key -t asuka_admin:1.1 'nvtop' C-m
tmux send-key -t asuka_admin:1.0 'docker attach asuka' C-m


# third window for download models with ollama
tmux new-window -t asuka_admin:2 -n 'pull models'
tmux send-key -t asuka_admin:2 'ollama help' C-m
tmux send-key -t asuka_admin:2 'ollama list' C-m
tmux send-key -t asuka_admin:2 "echo 'You can download models with command ollama pull <model_name>'" C-m


# first window with btop
tmux send-keys -t asuka_admin:0 "btop" C-m

alias asuka-dump="docker container stop ollama asuka postgresAsuka; docker container rm ollama asuka postgresAsuka; tmux kill-session -t asuka_admin"
# sleep 1 second for wait while app run and open browser
sleep 1
xdg-open "localhost:8080"


# open tmux for user
tmux attach -t asuka_admin:0









