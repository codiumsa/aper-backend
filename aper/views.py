from aper import app
from flask_login import login_required, current_user
from flask import jsonify, request
from .models import User
from .db import db_session
from datetime import date, datetime
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
    if current_user.role != 'ADMIN':
        return 'FORBIDDEN', 403
    else:
        users = [u.serialize() for u in User.query.all()]
        return jsonify(users)


@app.route('/open_gate', methods=['GET'])
@login_required
def open_gate():
    if (current_user.role != 'ADMIN' and current_user.role != 'USER'):
        return 'FORBIDDEN', 403
    else:
        allowed_users = User.allowed_users()
        if current_user in allowed_users:
            controller = LED(17)
            controller.on()
            sleep(2)
            controller.off()
            sleep(2)
            current_user.last_use = datetime.datetime.now()
            db_session.commit()
            return 'Abriendo portón...'
        else:
            return 'No podés estacionar adentro hoy :(', 403


@app.route('/not_using', methods=['POST'])
@login_required
def not_using():
    if (current_user.role != 'ADMIN' and current_user.role != 'USER'):
        return 'FORBIDDEN', 403
    else:
        if current_user.absent_on != datetime.date.today():
            current_user.absent_on = date.today()
            db_session.commit()
            return 'Registramos que no vas a usar tu lugar hoy', 201
        else:
            current_user.absent_on = None
            db_session.commit()
            return 'Vas a usar tu lugar hoy', 202


@app.route('/users_order', methods=['POST'])
@login_required
def change_order():
    if current_user.role != 'ADMIN':
        return 'FORBIDDEN', 403
    else:
        for id, order in request.form.items():
                user = User.query.get(id)
                if order == 'null':
                    user.order = ''
                else:
                    user.order = order
        db_session.commit()
        return 'Users updated'

@app.route('/users_roles', methods=['POST'])
@login_required
def change_roles():
    if current_user.role != 'ADMIN':
        return 'FORBIDDEN', 403
    else:
        for id, role in request.form.items():
                user = User.query.get(id)
                user.role = role
        db_session.commit()
        return 'Users updated'

@app.route('/absent', methods=['GET'])
@login_required
def isabsent():
    if (current_user.role != 'ADMIN' and current_user.role != 'USER'):
        return 'FORBIDDEN', 403
    else:
        if current_user.absent_on == datetime.date.today():
            return 'yes'
        else:
            return 'no'


@app.route('/last_use', methods=['GET'])
@login_required
def getlastuse():
    if (current_user.role != 'ADMIN' and current_user.role != 'USER'):
        return 'FORBIDDEN', 403
    else:
        user = User.query.order_by(User.last_use.desc()).first()
        return user.serialize()


@app.route('/delete', methods=['POST'])
@login_required
def delete():
    if current_user.role != 'ADMIN':
        return 'FORBIDDEN', 403
    else:
        for id, state in request.form.items():
            if state == 'true':
                user = User.query.get(id)
                db_session.delete(user)
        db_session.commit()
        return 'ok', 200

