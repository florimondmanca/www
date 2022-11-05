# www

[![Build Status](https://dev.azure.com/florimondmanca/public/_apis/build/status/florimondmanca.www?branchName=master)](https://dev.azure.com/florimondmanca/public/_build/latest?definitionId=1&branchName=master)
[![Coverage](https://codecov.io/gh/florimondmanca/www/branch/master/graph/badge.svg?token=IT5DBiSTHK)](https://codecov.io/gh/florimondmanca/www)

Code for https://florimond.dev.

## Prerequisites

Runtime:

- Python 3.10+

Development only:

- Node.js 16.x
- Heroku CLI - _(optional)_

## Install

```bash
make install
```

## Usage

- Run the website locally:

```bash
make serve
```

- Run the website as it would run in production:

```bash
. venv/bin/activate
heroku local
```

- Run the test suite:

```bash
make test

# With options:
make args=[PYTEST_OPTIONS] test
```

- Build assets:

```bash
make build
```

## Settings

| Environment variable | Description                                                              | Default |
| -------------------- | ------------------------------------------------------------------------ | ------- |
| `DEBUG`              | Run in debug mode. Enables in-browser tracebacks and content hot reload. | `False` |
| `TESTING`            | Run against mocked resources.                                            | `False` |
| `EXTRA_CONTENT_DIRS` | Include content from extra directories.                                  | None    |

## Deployment

Once the [Infrastructure](#infrastructure) is set up, deploy to the [Dokku](http://dokku.viewdocs.io/dokku/) instance using:

```bash
make deploy
```

### Infrastructure

The Dokku instance is managed using [Ansible](https://docs.ansible.com/ansible/latest/index.html).

Cloud VM requirements:

* Linux: Debian 11 "bullseye"
* RAM: at least 1 GB
* Networking: ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) should be opened to traffic.

Install additional dependencies:

```
make install-infra
```

Review `ansible/hosts.ini`, then:

```
make infra
```

This should configure the Linux box and deploy the app. For subsequent deploys, see [Deployment](#deployment).

### CI

Azure Pipelines is configured to deploy on pushes to the `master` branch.

This requires setting up SSH keys. Initially, it can be created using:

```
make infra-ci-deploy-keys
```

This creates 3 files:

* `ansible/data/azp-id_rsa` - Private key, ignored by git.
  * Use this to [add an `SSH` service connection](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/utility/install-ssh-key?view=azure-devops) in Azure Pipelines. Set the host, username (`dokku`), service connection name, and upload the private key.
  * Upload the private SSH key as a secure file, named `florimond-dev-deploy-id_rsa`.
* `ansible/data/azp-id_rsa.pub` - Public key, used to add the AZP SSH key to the Dokku instance ([dokku_users](https://github.com/dokku/ansible-dokku#dokku_users)).
  * This is referenced in the Ansible playbook.
* `ansible/data/azp-known_hosts_entry` - Known hosts entry, used by AZP.
  * Copy this into `azure-pipelines.yml`.

## License

- Code is licensed under MIT.
- Writings are my own.
