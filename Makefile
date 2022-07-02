venv = venv
bin = ${venv}/bin/
python = ${bin}python
pip = ${bin}pip
pysources = server/ tests/

build:
	NODE_ENV=production yarn build

check:
	${bin}black --check --diff ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}
	${python} -m server.tools.mdformat --check

deploy:
	scripts/deploy $(args)

${venv}:
	python3 -m venv ${venv}

install:
	make ${venv}
	${pip} install -U pip wheel
	${pip} install -r requirements-dev.txt
	make messagesc
ifndef CI
	yarn install
endif
	make .env

.env:
	cp .env.example .env

lint:
	${bin}autoflake --in-place --recursive ${pysources}
	${bin}isort ${pysources}
	${bin}black ${pysources}
	${python} -m server.tools.mdformat

messages:
	make locale/.init
	${bin}pybabel extract -F babel.cfg -o locale/base.pot ./server/
	${bin}pybabel update -i locale/base.pot -d locale

locale/.init:
		${bin}pybabel init -l fr_FR -i locale/base.pot -d locale
		touch locale/.init

messagesc:
	${bin}pybabel compile --domain messages -d locale

serve:
	make -j 2 serve-uvicorn serve-tailwind

serve-uvicorn:
	./tools/colorize_prefix.sh [server] 34 "${bin}uvicorn server:app --reload"

serve-tailwind:
	./tools/colorize_prefix.sh [tailwind] 33 "NODE_ENV=production yarn watch"

imgoptimize:
	${bin}python -m server.tools.imgoptimize

test:
	${bin}pytest $(args)
