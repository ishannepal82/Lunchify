from flask import request,jsonify
from .. import auth_bp
from ..utils.mail_token_helper import confirm_verification_token
from ....models.user_model import User
from ....extensions import db 

@auth_bp.route('/verify_email_token/<token>')
def verify_email_token(token):
    email =  confirm_verification_token(token)
    
    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg":'user not found'}), 404
    
    if user.is_verified:
        return jsonify({"msg":'user already verified'}), 400
    
    user.is_verified = True
    db.session.commit()

    return jsonify({"msg": 'email verified sucessfully'}), 200

    
    
    