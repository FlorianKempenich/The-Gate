#!/bin/bash

# `-T` option is there to ensure `docker exec` doesn't output CRLF (line endings)
# That makes possible to pipe the output of this script to a file:
#
#     ./cat_loaded_nginx_config.sh > my_current_config.conf
#
docker-compose exec -T proxy cat /etc/nginx/nginx.conf
