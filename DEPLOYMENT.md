# Deployment

Deployment is managed using [Ansible](https://docs.ansible.com/ansible/latest/index.html).

## Deploy the production environment

Cloud VM requirements:

* OS: Linux Debian 11 "bullseye"
* RAM: at least 1 GB
* Networking: ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) must be open to traffic.

Install additional dependencies:

```
make install-deploy
```

Provision the VM:

```
make provision env=prod
```

Deploy:

```
make deploy env=prod
```

### Deploy to a test VM

The Ansible setup can be tested on a local [Vagrant](https://www.vagrantup.com/) VM using the provided `vagrant` environment.

Ensure Vagrant is installed. (You may need to install Virtualbox as well.)

Start the VM:

```
make vagrant-up
```

Deploy to the VM:

```
make provision env=vagrant
make deploy env=vagrant
```

Ensure its port 80 is exposed on `localhost:8080`:

```
make vagrant-ssh
```

Access the deployed site on http//localhost:8080.

To deploy a custom branch, add `ansible/environments/vagrant/group_vars/web.yml` with the following, then deploy.

```yaml
git_version: mybranch
```

To stop the VM:

```
make vagrant-halt
```

### CI deploys

Azure Pipelines is configured to deploy on pushes to the `master` branch.

This requires setting up SSH keys. Initially, it can be created using:

```
cd ansible && make ci-deploy-keys
```

This creates 3 files:

* `ansible/environments/prod/data/azp-id_rsa` - Private key, ignored by git.
  * [Add an `SSH` service connection](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/utility/install-ssh-key?view=azure-devops) under Project settings > Service connections in Azure Pipelines. Set the host name (`florimond.dev`), username (`debian`), service connection name (`florimond-dev-deploy`), and upload the private key.
  * Under Pipelines > Library, upload the private SSH key as a secure file, named `florimond-dev-deploy-id_rsa`.
* `ansible/environments/prod/data/azp-id_rsa.pub` - Public key.
  * Add this manually to `~/.ssh/authorized_keys` on the production server.
* `ansible/environments/prod/data/azp-known_hosts_entry` - Known hosts entry, used by AZP.
  * Copy this into `azure-pipelines.yml`.
