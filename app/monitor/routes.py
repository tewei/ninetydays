from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user
from app.models import UserBasic
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.monitor import bp
from app import db
from app.monitor.forms import NewPhysioLogForm, NewTransactionForm
from app.models import Mission, PhysioLog, Transaction
import datetime as dt
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func

@bp.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    form = NewPhysioLogForm()
    form_bank = NewTransactionForm()
    if form.validate_on_submit():
        user_to_add = UserBasic.query.filter_by(username=form.username.data).first()
        log = PhysioLog(physio_type=form.physio_type.data, value=form.value.data, user=user_to_add, physio_verify='physician')
        if (current_user.mission is not None):
                log.mission = current_user.mission
        db.session.add(log)
        db.session.commit()
        flash('New physiological log added!')
        return redirect(url_for('monitor.monitor'))

    if form.validate_on_submit():
        user_to_add = UserBasic.query.filter_by(username=form.username.data).first()
        t = Transaction(transaction_type=form.transaction_type.data, value=form.value.data, user=current_user)
        db.session.add(t)
        db.session.commit()
        flash('New transaction updated!')
        return redirect(url_for('monitor.monitor'))

    user_monitor = UserBasic.query.filter(UserBasic.mission != None).all()

    return render_template('monitor/monitor.html', form=form, form_bank=form_bank, user_monitor=user_monitor)

@bp.route('/monitor/user/<username>/del_physio/<id>')
@login_required
def del_physio(username, id):
    physiolog = PhysioLog.query.filter_by(id=id).first_or_404()
    if (physiolog.user.username == username):
        db.session.delete(physiolog)
        db.session.commit()
        flash('Log deleted~')
        return redirect(url_for('monitor.user_monitor', username=username))
    
    return redirect(url_for('monitor.monitor'))

@bp.route('/monitor/user/<username>')
@login_required
def user_monitor(username):
    user = UserBasic.query.filter_by(username=username).first_or_404()
    current_sum = db.session.query(func.sum(Transaction.value)).filter_by(user_id=user.id).scalar()
    weight = PhysioLog.query.filter_by(user_id=user.id).filter_by(physio_type='weight').order_by(PhysioLog.timestamp.desc()).all()
    exercise = PhysioLog.query.filter_by(user_id=user.id).filter_by(physio_type='exercise').order_by(PhysioLog.timestamp.desc()).all()
    calorie = PhysioLog.query.filter_by(user_id=user.id).filter_by(physio_type='calorie').order_by(PhysioLog.timestamp.desc()).all()

    return render_template('monitor/user_monitor.html', user=user, current_sum=current_sum, weight=weight, exercise=exercise, calorie=calorie)

