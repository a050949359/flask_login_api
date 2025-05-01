from flask import Blueprint, current_app, g, jsonify, request 
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__)

@auth_bp.before_request
def get_db_connection():
    if app.config['DB_TYPE'] == "sqlite":
        if 'db_conn' not in g:
            g.db_conn = current_app.db_pool
    elif app.config['DB_TYPE'] == "mysql":
        if 'db_conn' not in g:
            g.db_conn = current_app.db_pool.get_connection()


@auth_bp.teardown_request
def close_db_connection(exception=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()


@auth_bp.route("/register", methods=['POST'])
def register():
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


def register_user(cursor, email, password, ):
    now = datetime.now()
    expired_at = now + timedelta(days=30)

    # 轉成 SQLite 支援的字串格式
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    expired_str = expired_at.strftime('%Y-%m-%d %H:%M:%S')
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
  password,
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