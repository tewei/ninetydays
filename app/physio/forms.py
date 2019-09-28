from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired
from app.models import UserBasic, Mission

class NewPhysioLogForm(FlaskForm):
    physio_type = SelectField('Physiology data type', choices=[('weight', '體重 (kg)'), ('blood_pressure', '血壓 (mmHg)'), ('blood_glucose', '血糖 (mg/dL)')], validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(NewPhysioLogForm, self).__init__(*args, **kwargs)
        

    # def validate_username(self, username):
    #     user = UserBasic.query.filter_by(username=self.username.data).first()
    #     if user is None:
    #         raise ValidationError('User not found!')
    #     else:
    #         mission = Mission.query.filter_by(user_id=user.id).first()
    #         if mission is not None:
    #             raise ValidationError('User is currently on a mission!')