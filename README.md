# Welcome to Asuka (local llm chat app + monitor in terminal)

Hi there! This application offers a build of an application for chat locally with the language model and monitoring the system from the terminal. 
This version is usefull only for linux, because the necessary software components and convenience for which the application was created are only available on it. For windows users is necessary install WSL, prefer Debian distro.

**Tmux** is used to track the consumption of system resources and monitor the life cycle of the application. 
The main application uses the design from [Chainlit](https://github.com/Chainlit/chainlit). Chat history support, necessary (in the author's opinion) settings are included, support for using vision models(not fully tested...).

**Default user name and pass is** `admin admin`.

You can always check README on the web app, just open Readme buttom on the right top corner.

You should have can execute docker command without sudo, or go to root and execute `start-app.bash`. And preinstalled ollama is required, [install ollama](https://ollama.com/download).



## Images
1. Ollama([Docker Hub](https://hub.docker.com/r/ollama/ollama))
    - volume: ollama
    - network: asukaNet
    - port: 11434:11434(original ollama port)
2. Custom postgres with prisma official schema from chainlit, build from postgres latest image([Docker Hub](https://hub.docker.com/_/postgres))
    - volume: asuka\_datalayer
    - network: asukaNet
    - port: 5432:5432(original postgres port)
3. Custom asuka app, build from python latest image([Docker Hub](https://hub.docker.com/_/python))
    - volume: asuka\_app
    - network: asukaNet
    - port: 8080:80


## Usage
1. Execute `start-app.bash` script with paramenters `start-app.bash apt/yum/dnf nvidia/radeon/<none>`. During installation you will be asked to enter a sudo password, to download `btop tmux nvtop` via your package manager. 
    - cpu only example with apt `./start-app.bash apt`
    - nvidia gpu example with yum `./start-app.bash yum nvidia`
    - amd gpu example with dnf `./start-app.bash dnf radeon`

2. For remove all containers, volumes, images(*ollama on it too*), execute `end-app.bash`.
3. You can add alias `alias asuka-dump="docker container stop ollama asuka postgresAsuka; docker container rm ollama asuka postgresAsuka; tmux kill-session -t asuka_admin"` for quick dump all containers and tmux session. After that you can use `start-app.bash` with healthy execution. You can remove this alias with command `unalias asuka-dump`.


## Tmux overview
- First window have **btop** to check your cpu, ram, process, ...
- Second window have asuka web logging on the left side and nvtop on the right side
- Third window get be able to pull onother models via terminal 
*You can use **tmux** it however you want, open and run whatever you want, it's just basic.*


## Basic tmux commands
### Starting tmux
- `tmux` Start a new tmux session.
- `tmux new -s <session_name>` Start a new session with a specific name.

### Session Management
- `Ctrl+b d` Detach from the current session.
- `tmux ls` List all active sessions.
- `tmux attach -t session_name` Reattach to a session by its name.

### Window Management
- `Ctrl+b c` Create a new window.
- `Ctrl+b n` Move to the next window.
- `Ctrl+b p` Move to the previous window.

### Pane Management
- `Ctrl+b "` Split the window horizontally.
- `Ctrl+b %` Split the window vertically.
- `Ctrl+b o` Cycle through panes.
- `Ctrl+b x` Close the current pane.

### Kill session
- `tmux kill-session -t <session_name>` Kill session by name

### Additional Command
- `Ctrl+b ?` Display a list of key bindings.
