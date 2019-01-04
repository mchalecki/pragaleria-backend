## Deployment Guide

1. Install [docker](https://www.docker.com/) according to the instructions in the following link:
- https://docs.docker.com/install/
2. Install [docker-compose](https://docs.docker.com/compose/overview/) according to the instructions in the following link
- https://docs.docker.com/compose/install/#install-compose
 3. Edit [docker-compose.yml](docker-compose.yml). Edit enviroment section(lines 11-15).
 * Set config=deploy
 * Fill DB_HOST, MYSQL_ROOT_PASSWORD, MYSQL_DATABASE with database credentials.
   * MYSQL_HOST - address of the database to connect to
   * MYSQL_DATABASE - name of the database
   * MYSQL_USER- user which is used for login
   * MYSQL_PASSWORD - user password
 
 4. Execute this command in shell:
 ```bash
 sudo docker-compose up
 ```
 
 ### Logs browsing
 Logs are located in directory [logs](logs). Each service produce different logs.
 - [gunicorn logs](logs/gunicorn)
 - [ngnix](logs/ngnix)
 - [redis](logs/redis)
 
 Example usage:
 To display current web server logs run:
 ```bash
 tail -f logs/gunicorn/errorlog.log
 ```
