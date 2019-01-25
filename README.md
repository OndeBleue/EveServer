# EveServer


[![Docker pulls](https://img.shields.io/docker/pulls/ondebleue/eve-server.svg)](https://hub.docker.com/r/ondebleue/eve-server/)

## Setup dev
1. Install [pyenv](https://github.com/pyenv/pyenv)
2. Install Python version as specified in [.python-version](.python-version)
3. Create [.env](app/env.exemple) file in app folder, then run
```bash
python -m venv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```
4. Run application with
```bash
gunicorn --chdir app -w 4 run:app -b localhost:8000
```

## Setup prod
### Requirements
- [Docker CE](https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/debian/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Procedure
1. prepare the files
```bash
\curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/setup.sh | bash
# add MONGO_URI and X_DOMAINS to env file
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
6. restart the containers and ensable the renew timer
```bash
docker-compose down
docker-compose up -d
sudo systemctl enable letsencrypt.timer
sudo systemctl start letsencrypt.timer
# check status with
sudo systemctl list-timers
```
