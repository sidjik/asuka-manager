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
#COPY ./env-chainlit ./.env

RUN echo "DATABASE_URL=postgresql://postgres:password@postgresAsuka:5432/postgres\n" > ./.env
RUN python -m chainlit create-secret | grep 'CHAINLIT_AUTH_SECRET' >> ./.env


# start app
CMD  python -m chainlit run --port 80 --host 0.0.0.0 -h app.py



