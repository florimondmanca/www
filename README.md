# www

Code for the apps deployed at https://florimond.dev.

## Apps

- [Root](./root) (domain: florimond.dev)
- [Blog](./blog) (domain: blog.florimond.dev)

## Install

- Add these lines to your `/etc/hosts` file:

```
127.0.0.1 blog.localhost
```

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

## Deployment

```bash
git push dokku master
# Or:
git push dokku $BRANCH:master
```
