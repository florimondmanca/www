# www

[![Build Status](https://dev.azure.com/florimondmanca/public/_apis/build/status/florimondmanca.www?branchName=master)](https://dev.azure.com/florimondmanca/public/_build/latest?definitionId=1&branchName=master)
[![Coverage](https://codecov.io/gh/florimondmanca/www/branch/master/graph/badge.svg?token=IT5DBiSTHK)](https://codecov.io/gh/florimondmanca/www)

Code for https://florimond.dev.

## Prerequisites

Runtime:

- Python 3.9+

Development only:

- Node.js v12
- Yarn
- Heroku CLI - _(optional)_

## Install

```bash
scripts/install [--update]
```

## Usage

- Run the website locally:

```bash
scripts/serve [UVICORN_OPTIONS]
```

- Run the website as it would run in production:

```bash
. venv/bin/activate
heroku local
```

- Run the test suite:

```bash
scripts/test [PYTEST_OPTIONS]
```

- Build assets:

```bash
scripts/build
```

## Deployment

This website is deployed via [Dokku](http://dokku.viewdocs.io/dokku/).

1. _(First time only)_ Setup SSH keys on the remote host. See [Setup SSH key](http://dokku.viewdocs.io/dokku/getting-started/installation/#2-setup-ssh-key-and-virtualhost-settings) and [User Management](http://dokku.viewdocs.io/dokku/deployment/user-management/#adding-ssh-keys).
2. Run the deploy script:

```bash
scripts/deploy
```

## Settings

| Environment variable | Description                                                              | Default |
| -------------------- | ------------------------------------------------------------------------ | ------- |
| `DEBUG`              | Run in debug mode. Enables in-browser tracebacks and content hot reload. | `False` |
| `TESTING`            | Run against mocked resources.                                            | `False` |

## License

- Code is licensed under MIT.
- Writings are my own.
