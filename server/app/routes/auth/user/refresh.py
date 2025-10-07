from .. import auth_bp
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    resp = jsonify({'msg': 'token refreshed'})
    resp.set_cookie('access_token_cookie', access_token)
    return resp, 200