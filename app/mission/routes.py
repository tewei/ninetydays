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
from app.models import Mission, PhysioLog, Transaction
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
        ended = False
        diff = mission.end_date - date_today
        if(diff.days < 0):
            ended = True
        return render_template("mission/my_mission.html", mission=mission, log_today=log_today, progress=progress, ended=ended)
    else:
        return render_template("mission/my_mission.html", mission=mission)

@bp.route('/new_mission', methods=['GET', 'POST'])
@login_required
def new_mission():
    form = NewMissionForm()
    if form.validate_on_submit():
        the_other_user = UserBasic.query.filter_by(username=form.participant.data).first()
        if(form.mission_type.data == 'pk'):
            mission = Mission(mission_type=form.mission_type.data, level=form.level.data, start_date=form.start_date.data, prize=form.prize.data, end_date=form.end_date.data, users=[current_user, the_other_user])
        elif(form.mission_type.data == 'gift'):
            mission = Mission(mission_type=form.mission_type.data, level=form.level.data, start_date=form.start_date.data, prize=form.prize.data, end_date=form.end_date.data, users=[the_other_user])
        

        if form.mission_type.data == 'pk':
            t = Transaction(transaction_type='new_mission', value=-form.prize.data, user=current_user, transaction_comment='PK with '+the_other_user.username)
            db.session.add(t)
            db.session.commit()
            flash('New transaction updated!')

            t = Transaction(transaction_type='new_mission', value=-form.prize.data, user=the_other_user, transaction_comment='PK with '+current_user.username)
            db.session.add(t)
            db.session.commit()
            flash('New transaction updated!')

        elif form.mission_type.data == 'gift':
            t = Transaction(transaction_type='gift', value=-form.prize.data, user=current_user, transaction_comment='Gift to '+the_other_user.username)
            db.session.add(t)
            db.session.commit()
            flash('New transaction updated!')
            
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
        date_today = dt.date.today()
        diff = mission.end_date - date_today
        winner = None
        max_score = -1
        if(diff.days < 0):
            for user in current_user.mission.users:

                num_user_logs = PhysioLog.query.filter(PhysioLog.user_id == user.id, PhysioLog.physio_verify == 'user', PhysioLog.mission_id == id).count()
                num_physician_logs = PhysioLog.query.filter(PhysioLog.user_id == user.id, PhysioLog.physio_verify == 'user', PhysioLog.mission_id == id).count()
                
                #change here for scoring formula
                score = num_user_logs + 30*num_physician_logs
                if(score > max_score):
                    winner = user
                    max_score = score

            if(mission.prize is not None):
                if(mission.mission_type == 'pk'):
                    t = Transaction(transaction_type='add', value=mission.prize*2, user=winner, transaction_comment='Winner of PK')
                    db.session.add(t)
                    db.session.commit()
                    flash('Prize distributed!')

                elif(mission.mission_type == 'gift'):
                    t = Transaction(transaction_type='add', value=mission.prize, user=winner, transaction_comment='Received a gift')
                    db.session.add(t)
                    db.session.commit()
                    flash('Gift sent!')

        db.session.delete(mission)
        db.session.commit()
        flash('Mission ended~')
        return redirect(url_for('mission.my_mission'))
    return redirect(url_for('mission.my_mission'))
