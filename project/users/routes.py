from datetime import datetime, date
from flask import  render_template, url_for, Blueprint, request, session, redirect, escape, flash, abort
from sqlalchemy import and_
from project.users.forms import RegisterForm
from project.models import db,User

users=Blueprint('users',__name__)


@users.route('/')
def temp():
	return render_template('layout.html')

@users.route('/profile')
def profile():
	return render_template('profile.html')

@users.route('/questionAsked')
def questionAsked():
	return render_template('askedquestions.html')
	


@users.route('/register/',methods=['POST','GET'])
def register():
	if (request.method=="POST") and ( 'Submit' in request.form.keys()):
		FirstName=escape(request.form['FirstName'])
		LastName=escape(request.form['LastName'])
		if(LastName==''):
			LastName=None
		UserName=escape(request.form['UserName'])
		UserEmail=escape(request.form['UserEmail'])
		UserDob=(datetime.strptime(escape(request.form['UserDob']),"%Y-%m-%d")).date()
		Password=escape(request.form['Password'])
		UserDescritpion=escape(request.form['UserDescritpion'])
		UserBranch=int(escape(request.form['UserBranch']))
		UserAccountType=int(escape(request.form['UserAccountType']))
		UserYear=0
		if UserAccountType!=1:
			UserYear=int(escape(request.form["UserYear"]))

		new_user=User(UfirstName=FirstName, UlastName=LastName, Uusername=UserName,Uemail=UserEmail, Udob=UserDob, UDescription=UserDescritpion, UstudyYear=UserYear, URole=UserAccountType,Upassword=Password, UBranch=UserBranch)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('users.temp'))
	else:
		form=RegisterForm()
		return render_template("register.html",form=form)