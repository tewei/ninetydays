from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user
from app.models import UserBasic
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.physio import bp
from app import db
from app.physio.forms import NewPhysioLogForm
from app.models import Mission, PhysioLog
from datetime import datetime

@bp.route('/my_physio', methods=['GET', 'POST'])
@login_required
def my_physio():
    form = NewPhysioLogForm()
    if form.validate_on_submit():
        log = PhysioLog(physio_type=form.physio_type.data, value=form.value.data, user=current_user)
        db.session.add(log)
        db.session.commit()
        flash('New physiological log added!')
        return redirect(url_for('physio.my_physio'))

    blood_pressure = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='blood_pressure').all()
    weight = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='weight').all()
    blood_glucose = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='blood_glucose').all()

    return render_template("physio/my_physio.html", form=form, weight=weight, blood_pressure=blood_pressure, blood_glucose=blood_glucose)

@bp.route('/del_physio/<id>')
@login_required
def del_physio(id):
    physiolog = PhysioLog.query.filter_by(id=id).first_or_404()
    if (physiolog.user.id == current_user.id):
        db.session.delete(physiolog)
        db.session.commit()
        flash('Log deleted~')
        return redirect(url_for('physio.my_physio'))
    return redirect(url_for('physio.my_physio'))
