# stop asuka use containers
docker container stop ollama asuka postgresAsuka
# remove asuka containers
docker container rm ollama asuka postgresAsuka
# delte admin session running on tmux
tmux kill-session -t asuka_admin
