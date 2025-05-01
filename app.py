from flask import Flask, current_app, g, jsonify
from flask_jwt_extended import JWTManager, jwt_required
from datetime  import timedelta
from dotenv import load_dotenv
from .db import init_db_pool
from .auth import auth_bp, register_user, login_user

import sqlite3
import os

load_dotenv()

app = Flask(__name__)

app.config['DB_TYPE'] = os.getenv("DB_TYPE")

init_db_pool(app)

# api = Api(app)
# api.add_resource(TestAPI, '/api/test')

app.register_blueprint(auth_bp, url_prefix='/auth')

# 設定 JWT 密鑰
jwt = JWTManager()
app.config['JWT_SECRET_KEY'] = 'secret_2025'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt.init_app(app)


# test
conn = app.db_pool
cursor = conn.cursor()
register_user(cursor, "test@test.com", "123456")

conn.commit()

login_user(cursor, "test@test.com", "123456")

cursor.close()
conn.close()