from flask import Blueprint, current_app, g, jsonify, request 
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import bcrypt
from datetime import datetime, timedelta
import sqlite3


auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def get_db_connection():
    if current_app.config['DB_TYPE'] == "sqlite":
        if 'db_conn' not in g:
            g.db_conn = current_app.db_pool
    elif current_app.config['DB_TYPE'] == "mysql":
        if 'db_conn' not in g:
            g.db_conn = current_app.db_pool.get_connection()


@auth_bp.teardown_request
def close_db_connection(exception=None):
    conn = g.pop('db_conn', None)
    if conn is not None and current_app.config['DB_TYPE'] == "mysql":
        conn.close()


@auth_bp.route("/register", methods=['POST'])
def register():
    data = request.json
    email = data['email']
    password = data['password'].encode('utf-8')

    if not email or not password:
        return jsonify({'error': '缺少 username 或 password'}), 400
    
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor = g.db_conn.cursor()
    cursor.execute("SELECT NOW()")
    now = cursor.fetchone()[0]
    cursor.close()
    return jsonify({'msg':'SUCCESS', 'time':now}), 200


@auth_bp.route("/login", methods=['POST'])
def login():
    user_id = request.args.get('id') 
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    return jsonify(msg="SUCCESS", access_token=access_token, refresh_token=refresh_token), 200


@auth_bp.route("/logout", methods=['GET'])
@jwt_required()
def logout():
    return jsonify({'msg':'SUCCESS'}), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


def register_user(cursor, email, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    now = datetime.now()
    expired_at = now + timedelta(days=30)
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    expired_str = expired_at.strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("""
            INSERT INTO users (
            email,
            password_hash,
            is_active,
            is_locked,
            is_force_pw_ch,
            failed_login_attempts,
            locked_until,
            last_login_at,
            last_failed_login_at,
            password_updated_at,
            password_expired_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            email,
            hashed_pw,
            1,
            0,
            0,
            0,
            None,
            None,
            None,
            now_str,
            expired_str
        ))
    except sqlite3.IntegrityError as e:
        print(f"❌ 資料庫完整性錯誤（可能是 email 重複）：{e}")

    except sqlite3.OperationalError as e:
        print(f"❌ SQL 操作錯誤：{e}")

    except Exception as e:
        print(f"❌ 其他錯誤：{e}")

def login_user(cursor, email, password):
    cursor.execute("""
        select password_hash from users where email = ? AND is_active = 1 AND is_locked = 0;
    """, (
        email,
    ))

    row = cursor.fetchone()
    if row is None:
        print("找不到使用者")
        return 2
    
    stored_hash = row[0]
    print("stored_hash:", stored_hash)
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        print("登入成功")
        return 0
    else:
        print("登入失敗")
        return 1


