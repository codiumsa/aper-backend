from aper import app
from flask_login import login_required, current_user
from flask import jsonify, request
from .models import User
from .db import db_session
import datetime
from gpiozero import LED
from time import sleep


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
        controller=LED(17)
        controller.on()
        sleep(2)
        controller.off()
        sleep(2)
        return 'Open Sesame'
    else:
        return 'You cannot park inside today', 403


@app.route('/users', methods=['PUT'])
@login_required
def update_user():
    current_user.order = request.form.get('order', current_user.order)

    d = request.form.get('absent_on', current_user.absent_on)
    if d:
        current_user.absent_on = datetime.datetime.strptime(d, '%Y-%m-%d')
    db_session.commit()
    return 'User updated'
