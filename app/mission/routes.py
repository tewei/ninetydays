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
from app.models import Mission
from datetime import datetime

@bp.route('/my_mission', methods=['GET', 'POST'])
@login_required
def my_mission():
    mission = Mission.query.filter_by(user_id=current_user.id).first()
    return render_template("mission/my_mission.html", mission=mission)

@bp.route('/new_mission', methods=['GET', 'POST'])
@login_required
def new_mission():
    form = NewMissionForm()
    if form.validate_on_submit():
        mission = Mission(mission_type=form.mission_type.data, start_date=form.start_date.data, end_date=form.end_date.data, creator=current_user)
        db.session.add(mission)
        db.session.commit()
        flash('New mission added!')
        return redirect(url_for('mission.my_mission'))
    return render_template("mission/new_mission.html", form=form)

@bp.route('/end_mission/<id>')
@login_required
def end_mission(id):
    mission = Mission.query.filter_by(id=id).first_or_404()
    db.session.delete(mission)
    db.session.commit()
    flash('Mission ended~')
    return render_template('mission/my_mission.html')
