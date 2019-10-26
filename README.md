# www

Code for the apps deployed at https://florimond.dev.

## Install

- Install Python dependencies:

```bash
python -m venv venv
. venv/bin/activate
pip install requirements-dev.txt
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

## Configuration

- `BLOG_ENABLED`: enable the blog application, served at `/blog/`.

## Deployment

```bash
git push dokku master
# Or:
git push dokku $BRANCH:master
```
