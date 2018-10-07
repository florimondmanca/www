# Portfolio

[![Build Status](https://img.shields.io/travis-ci/florimondmanca/personal.svg?style=flat-square)](https://travis-ci.org/florimondmanca/portfolio)
[![content](https://img.shields.io/badge/content-static-black.svg?style=flat-square)](https://www.florimondmanca.com)
[![speed](https://img.shields.io/badge/speed-blazing_fast-orange.svg?style=flat-square)](https://www.florimondmanca.com)
[![gzip](https://img.shields.io/badge/gzip_size-148kB-indigo.svg?style=flat-square)](https://www.florimondmanca.com)

This is my personal portfolio website. The code for it, at least.

## Install

Fairly straight-forward:

```bash
$ npm install
```

## Quickstart

Run the server using `$ npm start`:

```bash
$ npm start
Server listening on http://localhost:4200
```

## Settings

| Environment variable | Description |
|------|-------------|
| `HOST` | Host on which the server runs. Defaults to `localhost`. |
| `PORT` | Port used by the server. Defaults to `4200`. |

## Deployment

Deployment is configured in `.travis.yml`.

After a successful CI build:

- Static files are securely uploaded to my server using `rsync`.
- A deploy is triggered via [CaptainDuckDuck](https://captainduckduck.com).
