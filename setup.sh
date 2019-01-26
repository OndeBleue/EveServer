 #!/bin/bash

prepare_config()
{
  EVESERVER_PATH=${1:-/apps/eveserver}
  
  mkdir -p "$EVESERVER_PATH/config/nginx/ssl"
  mkdir -p "$EVESERVER_PATH/letsencrypt/config"
  mkdir -p "$EVESERVER_PATH/letsencrypt/etc/webrootauth"

  # nginx configuration
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/nginx.conf > "$EVESERVER_PATH/config/nginx/nginx.conf"

  # let's encrypt configuration
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/webroot.ini > "$EVESERVER_PATH/letsencrypt/config/webroot.ini"

  # docker-compose
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/docker-compose.yml > "$EVESERVER_PATH/docker-compose.yml"
}

prepare_ssl()
{
  SSL_PATH="$EVESERVER_PATH/config/nginx/ssl"
  
  openssl dhparam -out "$SSL_PATH/dhparam.pem" 4096
  
  # let's encrypt service
  docker pull quay.io/letsencrypt/letsencrypt:latest
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/letsencrypt.service > "/etc/systemd/system/letsencrypt.service"
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/letsencrypt.timer > "/etc/systemd/system/letsencrypt.timer"
}

prepare_fail2ban()
{
  apt update && apt install fail2ban
  
  # config files
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/fail2ban/filter.d/nginx-401.conf > "/etc/fail2ban/filter.d/nginx-401.conf"
  \curl -sSL https://raw.githubusercontent.com/OndeBleue/EveServer/master/conf/fail2ban/jail.local > "/etc/fail2ban/jail.local"
  
  systemctl reload fail2ban.service
  
  iptables -I DOCKER-USER 1 f2b-nginx-401
  iptables -I DOCKER-USER 2 -j f2b-nginx-http-auth
}

prepare_config "$@"
prepare_ssl
prepare_fail2ban
