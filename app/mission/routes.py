from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user
from app.models import UserBasic
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.mission import bp
from app import db
from app.mission.forms import NewMissionForm
from app.models import Mission, PhysioLog
import datetime as dt
from datetime import datetime
from datetime import timedelta

@bp.route('/my_mission', methods=['GET', 'POST'])
@login_required
def my_mission():
    mission = current_user.mission
    if mission is not None:
        log_today = PhysioLog.query.filter(PhysioLog.user_id == current_user.id, PhysioLog.physio_type == 'weight', PhysioLog.mission_id == current_user.mission.id, (PhysioLog.timestamp+timedelta(days=1))>datetime.now() ).first()
        date_today = dt.date.today()
        diff1 = date_today  - mission.start_date
        diff2 = mission.end_date - mission.start_date
        progress = "%.2f" % (float(diff1.days)/float(diff2.days)*100.0)
        return render_template("mission/my_mission.html", mission=mission, log_today=log_today, progress=progress)
    else:
        return render_template("mission/my_mission.html", mission=mission)

@bp.route('/new_mission', methods=['GET', 'POST'])
@login_required
def new_mission():
    form = NewMissionForm()
    if form.validate_on_submit():
        the_other_user = UserBasic.query.filter_by(username=form.participant.data).first()
        mission = Mission(mission_type=form.mission_type.data, level=form.level.data, start_date=form.start_date.data, end_date=form.end_date.data, users=[current_user, the_other_user])
        db.session.add(mission)
        db.session.commit()
        flash('New mission added!')
        return redirect(url_for('mission.my_mission'))
    return render_template("mission/new_mission.html", form=form)

@bp.route('/end_mission/<id>')
@login_required
def end_mission(id):
    mission = Mission.query.filter_by(id=id).first_or_404()
    if (current_user.mission.id == mission.id):
        db.session.delete(mission)
        db.session.commit()
        flash('Mission ended~')
        return redirect(url_for('mission.my_mission'))
    return redirect(url_for('mission.my_mission'))
