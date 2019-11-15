# www

[![Build Status](https://travis-ci.org/florimondmanca/www.svg?branch=master)](https://travis-ci.org/florimondmanca/www)
[![Coverage](https://codecov.io/gh/florimondmanca/www/branch/master/graph/badge.svg?token=IT5DBiSTHK)](https://codecov.io/gh/florimondmanca/www)

Code for https://florimond.dev.

## Prerequisites

- Python 3.7+
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

- Serve the blog only (for development, w/ hot reload):

```bash
npm start
```

- Build assets:

```bash
scripts/build
```

- Run the website locally:

```bash
scripts/serve
```

- Run the website as it would run in production:

```bash
heroku local
```

- Deploy:

```bash
scripts/deploy
```
