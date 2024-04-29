from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class  User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
# db.create_all()
with app.app_context():
     db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')


    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400


    user = User.query.filter_by(email=email).first()


    if user and user.password == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    if not email or not new_password:
        return jsonify({'error': 'Missing email or new password'}), 400

    user = User.query.filter_by(email=email).first()

    if user:

        user.password = new_password
        db.session.commit()
        return jsonify({'message': 'Password reset successfully', 'new_password': new_password}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


# @app.route('/create_account', methods=['POST'])
# def create_account():
#
#     data = request.get_json()
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#
#
#     if not username or not email or not password:
#         return jsonify({'error': 'Missing username, email, or password'}), 400
#
#
#     new_user = User(username=username, email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()
#
#     return jsonify({'message': 'User created successfully'}), 201


@app.route('/verify_email', methods=['POST'])
def verify_email():

    data = request.get_json()
    email = data.get('email')


    if not email:
        return jsonify({'error': 'Missing email'}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        user.is_verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)