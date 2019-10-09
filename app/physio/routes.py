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
import datetime as dt
from datetime import datetime
from datetime import timedelta

@bp.route('/my_physio', methods=['GET', 'POST'])
@login_required
def my_physio():
    form = NewPhysioLogForm()
    if form.validate_on_submit():
        log = PhysioLog(physio_type=form.physio_type.data, value=form.value.data, user=current_user)
        if (current_user.mission is not None):
            recent_log = PhysioLog.query.filter(PhysioLog.user_id == current_user.id, PhysioLog.physio_type == form.physio_type.data, PhysioLog.mission_id == current_user.mission.id, (PhysioLog.timestamp+timedelta(days=1))>datetime.now() ).first()
            #print(recent_log.timestamp)
            if (recent_log is None):
                log.mission = current_user.mission
        db.session.add(log)
        db.session.commit()
        flash('New physiological log added!')
        return redirect(url_for('physio.my_physio'))

    blood_pressure = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='blood_pressure').order_by(PhysioLog.timestamp.desc()).all()
    weight = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='weight').order_by(PhysioLog.timestamp.desc()).all()
    blood_glucose = PhysioLog.query.filter_by(user_id=current_user.id).filter_by(physio_type='blood_glucose').order_by(PhysioLog.timestamp.desc()).all()

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
