# L'Onde bleue - EveServer

[![Docker pulls](https://img.shields.io/docker/pulls/ondebleue/eve-server.svg)](https://hub.docker.com/r/ondebleue/eve-server/)

## About this project

Source files for the API server of l'Onde bleue.
The API is consumed by our [Progressive Web App](https://github.com/OndeBleue/MobileApp)


## Setup development environment
1. You'll need a [MongoDB](https://docs.mongodb.com/manual/administration/install-community/) instance, installed on your machine or on any accessible server. 
It's a good idea to use [docker](https://hub.docker.com/_/mongo) to install MongoDB.
Version 4.0+ is recommended.
2. Install [pyenv](https://github.com/pyenv/pyenv)
3. Install Python version as specified in [.python-version](.python-version)
4. Create [.env](app/env.exemple) file in app folder, then run
```bash
python -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```
5. Run application with
```bash
cd app
python run.py
```

## Setup production environment
### Requirements
- [Docker CE](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/debian/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Procedure
1. prepare the files
```bash
\curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/setup.sh | bash
# add MONGO_URI, X_DOMAINS and MODE to env file
vi /apps/eveserver/config/env
```
2. comment SSL lines in nginx configuration file
3. pull the images and start
```bash
cd /apps/eveserver
docker-compose pull
docker-compose up -d

```
4. generate SSL certificate
```bash
sudo systemctl start letsencrypt.service
```
5. uncomment SSL lines in nginx configuration file
6. restart the containers and enable the renew timer
```bash
docker-compose down
docker-compose up -d
sudo systemctl enable letsencrypt.timer
sudo systemctl start letsencrypt.timer
# check status with
sudo systemctl list-timers
```

## About l'Onde bleue

L'Onde bleue is a citizen collective, acting to help people demonstrating their commitment for the climate, 
and a way to create local resilient communities, in prevention of a civilizational collapse.

Visit our website at [www.onde-bleue.fr](https://www.onde-bleue.fr/).

## Contributing

Contribution are welcome. 
Please do not hesitate to open a pull request about our different projects, any ideas will be accepted as long as they
keep or improve the code quality.

