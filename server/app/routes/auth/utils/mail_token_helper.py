from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app as app
from flask import url_for
from ....extensions import mail

def generate_verification_token(email):
    searializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = searializer.dumps(email, salt='email-confirm-salt')
    return token

def confirm_verification_token(token, expiration=3600):
    searializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        return searializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except (SignatureExpired, BadSignature):
        return None
    
def send_verification_email(user_data):
    from flask_mail import Message

    token = generate_verification_token(user_data.email)
    verify_url = url_for('auth.verify_email_token', token=token, _external=True)
    html = f"""
    <h3>Hello {user_data.username},</h3>
    <p>Click below to verify your email:</p>
    <a href="{verify_url}">{verify_url}</a>
    """
    msg  = Message(subject='Email Verification', recipients=[user_data.email], sender="Flask_APP", html=html)
    mail.send(msg)

def send_password_change_email(user_data):
    from flask_mail import Message

    token = generate_verification_token(user_data.email)
    verify_url = url_for('auth.verify_email_token', token=token, _external=True)
    html = f"""
    <h3>Hello {user_data.username},</h3>
    <p>Your Password has been changed </p>
    <p>Click below to verify your email:</p>
    <a href="{verify_url}">{verify_url}</a>
    """
    msg  = Message(subject='Passwrod Change Verification', recipients=[user_data.email], sender="Flask_APP", html=html)
    mail.send(msg)
    