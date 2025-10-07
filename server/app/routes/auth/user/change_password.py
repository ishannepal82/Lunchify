from . import auth_bp
from flask import jsonify, request
from ....models.user_model import User
from ....extensions import db
from ..utils.mail_token_helper import send_password_change_email


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    if not request.is_json:
        return jsonify({"msg": 'missing json in request'}), 400
    
    email = request.json.get('email', None)
    old_password = request.json.get('old_password', None)
    new_password = request.json.get('new_password', None)

    if not email:
        return jsonify({"msg": 'missing email parameter'}), 400
    
    if not old_password:
        return jsonify({"msg": 'missing old_password parameter'}), 400
    
    if not new_password:
        return jsonify({"msg": 'missing new_password parameter'}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(old_password):
        return jsonify({"msg": 'bad username or password'}), 401
    
    user.set_password(new_password)
    
    db.session.commit()
    send_password_change_email(user)
    return jsonify({"msg": 'password changed successfully'}), 200
