from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired
from app.models import UserBasic, Mission

class NewMissionForm(FlaskForm):
    start_date = DateField('Start date', id='pickStartDate', validators=[DataRequired()])
    end_date = DateField('End date', id='pickEndDate', validators=[DataRequired()])
    mission_type = SelectField('Mission type', choices=[('pk', '雙人PK'), ('team', '組隊競賽'), ('gift', '好友送禮')])
    level = SelectField('Mission level', choices=[('easy', '佛系減重'), ('advanced', '精實減脂'), ('combined', '三高掰掰')])
    
    prize = FloatField('Value', validators=[DataRequired()])
    participant = StringField('Participant', validators=[DataRequired()])
    
    #to do: add survey questions for regression
    #
    #
    #
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewMissionForm, self).__init__(*args, **kwargs)

    def validate_participant(self, participant):
        user = UserBasic.query.filter_by(username=self.participant.data).first()
        if user is None:
            raise ValidationError('User not found!')
        else:
            mission = user.mission
            if mission is not None:
                raise ValidationError('User is currently on a mission!')

    # def validate_username(self, username):
    #     user = UserBasic.query.filter_by(username=self.username.data).first()
    #     if user is None:
    #         raise ValidationError('User not found!')
    #     else:
    #         mission = Mission.query.filter_by(user_id=user.id).first()
    #         if mission is not None:
    #             raise ValidationError('User is currently on a mission!')