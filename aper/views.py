from aper import app
from flask_login import login_required, current_user
from flask import jsonify, request
from .models import User
from .db import db_session
import datetime


@app.route('/')
@login_required
def index():
    return 'Hello {}!'.format(current_user.name)


@app.route('/users', methods=['GET'])
@login_required
def users():
    users = [u.serialize() for u in User.query.all()]
    return jsonify(users)


@app.route('/open_gate', methods=['GET'])
@login_required
def open_gate():
    allowed_users = User.allowed_users()
    if current_user in allowed_users:
        return 'Open Sesame'
    else:
        return 'You cannot park inside today', 403


@app.route('/users', methods=['PUT'])
@login_required
def update_user():
    print(current_user)
    current_user.order = request.form.get('order', current_user.order)
    d = request.form.get('absent_on', current_user.absent_on)
    if d:
        current_user.absent_on = datetime.datetime.strptime(d, '%Y-%m-%d')
    db_session.commit()
    return 'User updated'

@app.route('/users', methods=['POST'])
@login_required
def update_users():
    arr = request.form.get('ids').split(',')
    for id, index in enumerate(arr, start = 1):
        user = User.query.get(id)
        user.order = index
    db_session.commit()
    return 'Users updated'
