# flask_login_api
flask jwt bcrypt sqlite3 mysql docker

``` shell
$ apt update -y
$ apt upgrade -y
$ apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev git sqlite3
$ wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz
$ tar -xf Python-3.12.10.tgz
$ cd Python-3.12.10
$ ./configure --enable-optimizations
$ make -j 4
$ make altinstall
$ python -m venv DevEnv
$ source DevEnv/bin/activate
$ pip install --upgrade pip
$ pip3.12 install flask flask_jwt_extended mysql-connector flask-restful pysqlite3 python-dotenv bcrypt
```

content of .env 
```config
# sqlite or mysql
DB_TYPE=sqlite

# 
SQLITE_INIT_FILE=lib/db/user.sql

# store/flask.db or :memory:
SQLITE_DB_PATH=store/flask.db

MYSQL_HOST=192.168.4.4
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=flask_test
```

if use docker-compose modify yml's volumes settings and run commands
``` shell
$ docker network create --driver=bridge --subnet=192.168.4.0/24  ohya-network
$ docker-compose up -d
```