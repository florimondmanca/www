# www

[![Build Status](https://travis-ci.org/florimondmanca/www.svg?branch=master)](https://travis-ci.org/florimondmanca/www)
[![Coverage](https://codecov.io/gh/florimondmanca/www/branch/master/graph/badge.svg?token=IT5DBiSTHK)](https://codecov.io/gh/florimondmanca/www)

Code for https://florimond.dev.

## Prerequisites

Runtime:

- Python 3.7+

Development only:

- Node.js v10
- Yarn
- Heroku CLI - *(optional)*

## Install

- Install Python and Node dependencies:

```bash
scripts/install
```

- You may want to add a `.env` file:

```bash
# Starlette debug mode.
DEBUG=true

# Heroku configuration.
PYTHONUNBUFFERED=True
PORT=8000
```

## Usage

- Run the website locally:

```bash
scripts/serve
```

- Run the website as it would run in production:

```bash
. venv/bin/activate
heroku local
```

- Build assets:

```bash
scripts/build
```

- Deploy:

```bash
scripts/deploy
```

## License

- Code is licensed under GPL-3.
- Writings are my own.
