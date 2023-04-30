from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime


class JobsForm(FlaskForm):
    job = StringField("Работа", validators=[DataRequired()])
    work_size = IntegerField("Размер работы", validators=[NumberRange(0, 1000000, "Недопустимый возраст")])
    collaborators = StringField("Сотрудники", validators=[DataRequired()])
    start_date = DateTimeField("Дата начала", default=datetime.now())
    end_date = DateTimeField("Дата окончания", default=datetime.now())
    is_finished = BooleanField("Закончена")
    submit = SubmitField('Подтвердить')
