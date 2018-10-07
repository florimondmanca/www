echo "Setting up deploy SSH keys…"
openssl aes-256-cbc -K $encrypted_e4f690c90820_key -iv $encrypted_e4f690c90820_iv -in deploy_rsa.enc -out /tmp/deploy_rsa -d
eval "$(ssh-agent -s)"
chmod 600 /tmp/deploy_rsa
ssh-add /tmp/deploy_rsa

echo "Installing CaptainDuckDuck CLI…"
npm install -g captainduckduck
