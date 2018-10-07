echo "Copying public/ folder to Captain shared Nginx folder on remote…"
rsync -r --delete-after --quiet $TRAVIS_BUILD_DIR/public root@captain.florimondmanca.com:/captain/nginx-shared/portfolio

echo "Deploying using CaptainDuckDuck CLI…"
captainduckduck deploy -s -h https://captain.florimondmanca.com -a www -p $CAPTAIN_PASSWORD
