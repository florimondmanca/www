# www

[![Build Status](https://dev.azure.com/florimondmanca/public/_apis/build/status/florimondmanca.www?branchName=master)](https://dev.azure.com/florimondmanca/public/_build/latest?definitionId=1&branchName=master)
[![Coverage](https://codecov.io/gh/florimondmanca/www/branch/master/graph/badge.svg?token=IT5DBiSTHK)](https://codecov.io/gh/florimondmanca/www)

Code for https://florimond.dev.

## Prerequisites

- Python 3.11+
- Node.js 18.x

## Install

```bash
make install
```

## Usage

Run the website locally:

```
make serve
```

Run the test suite:

```
make test
```

Run automatic code formatting:

```
make format
```

Run code checks:

```
make check
```

Build assets:

```
make build
```

## Settings

| Environment variable | Description                                                                  | Default |
| -------------------- | ---------------------------------------------------------------------------- | ------- |
| `WWW_DEBUG`              | Run in debug mode. Enables in-browser tracebacks and content hot reload. | `False` |
| `WWW_TESTING`            | Run against mocked resources.                                            | `False` |
| `WWW_EXTRA_CONTENT_DIRS` | Include content from extra directories.                                  | None    |

## Deployment

Install deploy dependencies:

```
make install-deploy
```

Deploy:

```bash
make deploy env=prod
```

For more information, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## License

- Code is licensed under MIT.
- Writings are my own.
