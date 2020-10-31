from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


def AgetChoices(n):
	if n==1:
		return [(0,'NO'),(1,'YES')]
	else:
		pass


class AnswerForm(FlaskForm):
	Atitle=StringField("Title:", validators=[DataRequired()])
	AContent=TextAreaField("Body:", validators=[DataRequired()])
	ATags=StringField("Answer Tags:")
	ASubmit=SubmitField('Submit')

class QuestionForm(FlaskForm):
	Qtitle=StringField("Question:", validators=[DataRequired()])
	Qdescription=TextAreaField("Description:", validators=[DataRequired()])
	QTags=StringField("Question Tags:")
	QAnonymous=SelectField('Ask as Anonymous:',choices=AgetChoices(1),  validators=[DataRequired()])
	QSubmit=SubmitField('Submit')
