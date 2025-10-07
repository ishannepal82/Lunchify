from . import auth_bp
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from ...auth.utils.mail_token_helper import send_verification_email
from ....models.user_model import User
from ....extensions import db

@auth_bp.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email', None)


    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    # Here you would add your logic to verify the username and password
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'msg': "User already exists"})
    
    new_user =  User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    send_verification_email(new_user)

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    resp = jsonify({'msg': 'registration successful, please verify your email'})
    resp.set_cookie('access_token_cookie', access_token)

    return resp, 200

