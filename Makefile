##
## ----------------
## General
## ----------------
##

all: help

help: # Display this message
	@grep -E '(^[a-zA-Z0-9_\-\.]+:.*?#.*$$)|(^#)' Makefile | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /[33m/'

venv = venv
python_bin = python3
bin = ${venv}/bin/
pysources = server/ tests/ tools/

install: .env install-python # Install

.env:
	cp -n .env.example .env

venv:
	${python_bin} -m venv ${venv}

install-python: venv
	${bin}pip install -U pip wheel
	${bin}pip install -r requirements.txt
	make messagesc

##
## ----------------
## Building
## ----------------
##

build: # Build assets
	make pybuild
	make messagesc

pybuild:
	${bin}python -m tools.pybuild ./server/web/styles/styles.css --outdir ./server/web/static/css ${ARGS}

##
## ----------------
## Serving
## ----------------
##

serve: # Run servers
	make -j serve-uvicorn serve-assets

serve-uvicorn:
	PYTHONUNBUFFERED=1 ${bin}python -m server.main 2>&1 | ${bin}python -m tools.colorprefix blue [server]

serve-assets:
	PYTHONUNBUFFERED=1 make pybuild ARGS="--watch" 2>&1 | ${bin}python -m tools.colorprefix yellow [assets]

##
## ----------------
## Code quality
## ----------------
##

test: # Run the test suite
	${bin}pytest

check: # Run code checks
	${bin}black --check --diff ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}
	${bin}python -m server.tools.mdformat --check

format: # Run automatic code formatting
	${bin}autoflake --in-place --recursive ${pysources}
	${bin}isort ${pysources}
	${bin}black ${pysources}
	${bin}python -m server.tools.mdformat

##
## ----------------
## Translations
## ----------------
##

locale/.init:
		${bin}pybabel init -l fr_FR -i locale/base.pot -d locale
		touch locale/.init

messages: locale/.init # Update translations
	${bin}pybabel extract -F babel.cfg -o locale/base.pot ./server/
	${bin}pybabel update -i locale/base.pot -d locale

messagesc: # Compile translations
	${bin}pybabel compile --domain messages -d locale

##
## ----------------
## Tools
## ----------------
##

imgoptimize: # Optimize images
	${bin}python -m server.tools.imgoptimize

##
## ----------------
## Deployment
## ----------------
##

install-deploy: # Install deployment dependencies
	cd ansible && make install

ping: # Ping (args: env)
	cd ansible && make ping env=${env}

provision: # Provision infrastructure (args: env)
	cd ansible && make provision env=${env}

deploy: # Deploy (args: env)
	cd ansible && make deploy env=${env}

vagrant = cd ansible/environments/vagrant && vagrant

vagrant-up: # Start the test Vagrant VM.
	${vagrant} up

vagrant-halt: # Start the test Vagrant VM.
	${vagrant} halt

vagrant-ssh: # SSH into the Vagrant VM, exposing its deployment on localhost:8080
	${vagrant} ssh -- -L 8080:localhost:80
