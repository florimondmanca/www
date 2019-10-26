# www

Code for the apps deployed at https://florimond.dev.

## Install

- Install Python and Node dependencies:

```bash
scripts/install
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

- Serve the blog only:

```bash
cd apps/blog
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

- Run the website as it would in production:

```bash
heroku local
```

- Deploy:

```bash
scripts/deploy
```
