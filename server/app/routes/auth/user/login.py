from . import auth_bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from ....models.user_model import User
from ....extensions import db

@auth_bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg":'bad username or passwrod'}), 401
    
    access_token = create_access_token(identity=user.username)
    resp = jsonify({'msg': 'login successful'})
    
    resp.set_cookie('access_token_cookie', access_token)
    return resp, 200