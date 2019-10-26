# www

Code for the apps deployed at https://florimond.dev.

## Install

- Install Python dependencies:

```bash
python -m venv venv
. venv/bin/activate
pip install requirements-dev.txt
```

- You may want to add a `.env` file:

```bash
# Feature flags.
BLOG_ENABLED=true

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

- Build assets:

```bash
scripts/build
```

- Run the website as it would in production:

```bash
heroku local
```

- Deploy:

```bash
scripts/deploy
```
