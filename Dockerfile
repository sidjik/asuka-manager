FROM python:latest AS python

WORKDIR /app

# set port, our app working on 80
EXPOSE 80


# create environment
RUN python -m venv env
RUN ls
RUN . ./env/bin/activate 


# setup reqs
COPY requirements.txt .
RUN pip install -U pip --root-user-action ignore
RUN pip install -r requirements.txt --root-user-action ignore


# copy project file
COPY ./app.py .
COPY ./OllamaModel.py .
COPY ./start-chainlit.bash .
COPY ./env-chainlit ./.env

# start app
CMD  python -m chainlit run --port 80 --host 0.0.0.0 -h app.py



