 #!/usr/bin/env sh

SERVER_USER=$1
SERVER_IP=$2
SERVER_KEY=$3

chmod 600 deploy
ssh-add deploy
ssh-keyscan -H $SERVER_IP >> ~/.ssh/known_hosts
ssh -i $SERVER_KEY $SERVER_USER@$SERVER_IP "\
    cd pragaleria-backend && \
    docker-compose down && \
    git pull && \
    docker-compose up -d"