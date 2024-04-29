from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy

from DB_config.models import User

from flask import current_app as app
from DB_config import db

db = SQLAlchemy()

serializer = URLSafeTimedSerializer('your_secret_key')

regions = ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Australia']


def send_verification_email(email, verification_link):
    sender_email = 'tharwinn1997@gmail.com'
    message = MIMEText(f'Click the following link to generate your password: {verification_link}')
    message['Subject'] = 'Verification Link for Password Generation'
    message['From'] = sender_email
    message['To'] = email

    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login('tharwinn1997@gmail.com', 'rtiv wqiq xbax nyai')  # Change to your password
        smtp_server.sendmail(sender_email, [email], message.as_string())
        smtp_server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/api/register', methods=['POST'])
def handle_request():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'No data provided'}), 400

    if 'company_name' in data and 'email' in data:
        return register(data)
    elif 'token' in data and 'new_password' in data:
        return set_new_password(data.get('token'), data)
    elif 'email' in data:
        return reset_password(data)
    elif 'regions' in data:
        return select_regions(data)
    elif 'email' in data and 'password' in data:
        return login(data)
    else:
        return jsonify({'error': 'Invalid request format'}), 400

def register(data):
    company_name = data.get('company_name')
    email = data.get('email')

    if not company_name or not email:
        return jsonify({'error': 'Missing company name or email'}), 400

    user = User(company_name=company_name, email=email)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User with this email already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    token = serializer.dumps(email)
    verification_link = f"http://yourdomain.com/generate_password/{token}"

    if not send_verification_email(email, verification_link):
        return jsonify({'error': 'Failed to send verification email'}), 500

    return jsonify({'message': 'Verification link sent successfully', 'link': verification_link}), 200

def set_new_password(token, data):
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'Missing new password'}), 400

    try:
        email = serializer.loads(token, max_age=3600)
    except:
        return jsonify({'error': 'Invalid or expired token'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.password = new_password

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

    return jsonify({'message': 'Password SET successfully'}), 200

def reset_password(data):
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Missing email'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    token = serializer.dumps(email)
    reset_password_link = f"http://yourdomain.com/reset_password/{token}"

    if not send_verification_email(email, reset_password_link):
        return jsonify({'error': 'Failed to send reset password email'}), 500

    return jsonify({'message': 'Reset password link sent successfully', 'link': reset_password_link}), 200

def select_regions(data):
    if 'regions' not in data:
        return jsonify({'error': 'Missing regions in JSON data'}), 400

    regions_str = data['regions']
    selected_regions = [region.strip() for region in regions_str.split(',')]

    if not selected_regions:
        return jsonify({'error': 'No regions provided'}), 400

    invalid_regions = [region for region in selected_regions if region not in regions]
    if invalid_regions:
        return jsonify({'error': f'Invalid regions: {", ".join(invalid_regions)}'}), 400

    return jsonify({'message': f'Selected regions: {", ".join(selected_regions)}'}), 200

def login(data):
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


with app.app_a_context():
        db.create_all()
