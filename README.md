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