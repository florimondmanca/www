export ANSIBLE_CONFIG = ./ansible.cfg

venv = ../venv
bin = ${venv}/bin/
env-opts = -i ./environments/${env}/hosts.ini
playbook = ${bin}ansible-playbook ${env-opts} playbook.yml

install:
	${bin}pip install -r requirements.txt

ping:
	${bin}ansible ${env-opts} web -m ping

provision:
	${playbook} -t provision

deploy:
	${playbook} -t deploy

ci-deploy-keys: # Generate CI deploy SSH keys
	ssh-keygen -t rsa -b 4096 -f environments/prod/data/azp-id_rsa
	ssh-keyscan -f environments/prod/data/azp-id_rsa.pub -t ecdsa florimond.dev > environments/prod/data/azp-known_hosts_entry
