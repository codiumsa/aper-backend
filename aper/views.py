from aper import app
from flask_login import login_required, current_user
from flask import jsonify, request
from .models import User
from .db import db_session
from datetime import date
import datetime
from gpiozero import LED
from time import sleep


@app.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(current_user.serialize())


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
        # controller=LED(17)
        # controller.on()
        # sleep(2)
        # controller.off()
        # sleep(2)
        return 'Abriendo portón...'
    else:
        return 'No podés estacionar adentro hoy :(', 403


@app.route('/not_using', methods=['POST'])
@login_required
def not_using():
    print(current_user)
    if current_user.absent_on != datetime.date.today():
        current_user.absent_on = date.today()
        db_session.commit()
        return 'Registramos que no vas a usar tu lugar hoy'
    else:
        current_user.absent_on = None
        db_session.commit()
        return 'Vas a usar tu lugar hoy'

@app.route('/users', methods=['POST'])
@login_required
def update_users():
    arr = request.form.get('ids').split(',')
    for id, index in enumerate(arr, start = 1):
        user = User.query.get(id)
        user.order = index
    db_session.commit()
    return 'Users updated'
