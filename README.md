# www

Code for the apps deployed at https://florimond.dev.

## Apps

- [Root](./root) (domain: florimond.dev)
- [Blog](./blog) (domain: blog.florimond.dev)

## Install

```bash
python -m venv venv
. venv/bin/activate
pip install requirements-dev.txt
```

## Quickstart

```bash
# Using Heroku CLI:
heroku local
# Vanilla:
uvicorn app:app
```

## Deployment

```bash
git push dokku master
# Or:
git push dokku $BRANCH:master
```
