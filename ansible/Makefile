export ANSIBLE_CONFIG = ./ansible.cfg

venv = ../venv
bin = ${venv}/bin/
playbook = ${bin}ansible-playbook -i ./hosts.ini playbook.yml

run:
	make run-common
	make run-dokku
	make run-app

run-common:
	${playbook} -t common

run-dokku:
	${playbook} -t dokku

run-app:
	${playbook} -t app

install:
	${bin}pip install -r requirements-infra.txt
	${bin}ansible-galaxy install -r requirements.yml

ci-deploy-keys: # Generate CI deploy SSH keys
	ssh-keygen -t rsa -b 4096 -f data/azp-id_rsa
	ssh-keyscan -f data/azp-id_rsa.pub -t ecdsa infomaniak.florimond.dev > data/azp-known_hosts_entry
