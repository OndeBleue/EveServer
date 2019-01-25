# EveServer


[![Docker pulls](https://img.shields.io/docker/pulls/ondebleue/eve-server.svg)](https://hub.docker.com/r/ondebleue/eve-server/)
[![Docker Build Status](https://img.shields.io/docker/build/ondebleue/eve-server.svg)](https://hub.docker.com/r/ondebleue/eve-server/builds)

## Setup
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
