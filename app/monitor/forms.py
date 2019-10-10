from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired
from app.models import UserBasic, Mission, Transaction

class NewPhysioLogForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    physio_type = SelectField('Physiology data type', choices=[('weight', '體重 (kg)'), ('blood_pressure', '血壓 (mmHg)'), ('blood_glucose', '血糖 (mg/dL)'), ('body_fat', '體脂 (%)'), ('exercise', '運動 (分鐘)'), ('calorie', '攝食 (kcal)')], validators=[DataRequired()])
    physio_subtype = SelectField('Physiology data subtype', choices=[('none', '無'), ('systolic', '收縮壓'), ('diastolic', '舒張壓'), ('swimming', '游泳'), ('running', '慢跑')], validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(NewPhysioLogForm, self).__init__(*args, **kwargs)
        
    def validate_username(self, username):
        user = UserBasic.query.filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError('User not found!')
    # def validate_username(self, username):
    #     user = UserBasic.query.filter_by(username=self.username.data).first()
    #     if user is None:
    #         raise ValidationError('User not found!')
    #     else:
    #         mission = Mission.query.filter_by(user_id=user.id).first()
    #         if mission is not None:
    #             raise ValidationError('User is currently on a mission!')

class NewTransactionForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    transaction_type = SelectField('Transaction type', choices=[('add', '儲值'), ('gift', '送禮'), ('new_mission', '加入新任務')], validators=[DataRequired()])
    value = FloatField('Value', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(NewTransactionForm, self).__init__(*args, **kwargs)

    def validate_username(self, username):
        user = UserBasic.query.filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError('User not found!')