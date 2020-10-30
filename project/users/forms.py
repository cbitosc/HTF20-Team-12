from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
	Username=StringField("Username",validators=[DataRequired()])
	Password=PasswordField("Password",validators=[DataRequired()])
	Submit=SubmitField("Login")


def getChoices(n):
	if n==1:
		return [1,2,3,4]
	elif n==2:
		return [(1,"CSE"),(2,"ECE"),(3,'IT'),(4,"MECH"),(5,"CIVIL"),(6,'CHEM'),(7,"BIO-TECH"),(8,"PROD"),(9,"MCA"),(10,"MBA")] 
	elif n==3:
		return [(1,'FACULTY ACCOUNT'),(2,'STUDENT ACCOUNT')]
	else:
		pass

class RegisterForm(FlaskForm):
	FirstName=StringField("First-Name:",validators=[DataRequired()])
	LastName=StringField("Last-Name:")
	UserName=StringField("Username:",validators=[DataRequired()])
	UserEmail=StringField("UserEmail:",validators=[DataRequired()])
	Password=PasswordField("Password:",validators=[DataRequired(),EqualTo('ConfirmPassword',message="Passwords must be equal...")])
	ConfirmPassword=PasswordField("Confirm Password:",validators=[DataRequired()])
	UserDob=DateField("DOB:",validators=[DataRequired()])
	UserDescritpion=TextAreaField("Description:", validators=[DataRequired()])
	UserYear=SelectField('Year (not necessary for Faculty Account):',choices=getChoices(1),validators=[DataRequired()])
	UserBranch=SelectField('Branch:',choices=getChoices(2), validators=[DataRequired()])
	UserAccountType=SelectField('Account Type:', choices=getChoices(3), validators=[DataRequired()])
	Submit=SubmitField("Register")




	
class UpdateAccountForm(FlaskForm):
	FirstName=StringField("First-Name:",validators=[DataRequired()])
	LastName=StringField("Last-Name:")
	UserName=StringField("Username:",validators=[DataRequired()])
	UserEmail=StringField("UserEmail:",validators=[DataRequired()])
	UserDescritpion=TextAreaField("Description:", validators=[DataRequired()])
	# profilepicture
	Submit=SubmitField("Save Changes")

