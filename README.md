# Portfolio

This is my personal portfolio website.

## Install

Just like your usual Node project:

```bash
$ npm install
```

## Quickstart

Run the server:

```bash
$ npm start
```

## Deployment

Deployment is configured in `.travis.yml`. After a successful CI build:

- Static files are securely uploaded to my server using `rsync`.
- A deploy is triggered via [CaptainDuckDuck](https://captainduckduck.com).
