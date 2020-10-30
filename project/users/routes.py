from datetime import datetime, date
from flask import  render_template, url_for, Blueprint, request, session, redirect, escape, flash, abort
from sqlalchemy import and_
from project.users.forms import RegisterForm, LoginForm
from project.models import db,User

users=Blueprint('users',__name__)


branches={1:"CSE",2:"ECE",3:"IT",4:"MECH",5:"CIVIL",6:"CHEM",7:"BIO-TECH",8:"PROD",9:"MCA",10:"MBA"}

@users.route('/profile')
def profile():
	if('username' in  session.keys()) and ('user_id' in session.keys()):
		present_user=db.session.query(User).get(session['user_id'])
		return render_template('profile.html',current_user=present_user,branches=branches) 	

	return redirect(url_for('users.login'))

@users.route('/questionAsked')
def questionAsked():
	return render_template('askedquestions.html')
	


@users.route("/login/",methods=['POST','GET'])
def login():
	if request.method=="POST":
		username=escape(request.form['Username'])
		password=escape(request.form['Password'])
		row=db.session.query(User).filter(and_(User.Uusername==username, User.Upassword==password)).first()
		if row!=None:
			session['username']=str(username)
			session['user_id']=int(row.Uid)
			return redirect(url_for('users.mainpage'))
		else:
			flash("Username or Password incorrect...")
			return redirect(url_for('users.login'))
	else:
		form=LoginForm()
		return render_template("Login.html",form=form)

@users.route('/logout/')
def logout():
	if 'username' in session.keys():
		session.pop('username')
		session.pop('user_id')
		return redirect(url_for('users.mainpage'))
	else:
		abort(401)

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
		return redirect(url_for('users.login'))
	else:
		form=RegisterForm()
		return render_template("register.html",form=form)


@users.route("/")
def mainpage():
	if ('username' in session.keys()) and ('user_id' in session.keys()):
		return redirect(url_for('users.homepage'))

	return render_template("GreetPage.html")


@users.route('/home/')
def homepage():
	if ('username' in session.keys()) and ('user_id' in session.keys()):
		present_user=db.session.query(User).get(session['user_id'])
		Tags=present_user.user_tags()
		return render_template("homepage.html",Tags=Tags)
		
	return render_template("GreetPage.html")

@users.route('/AccountDetails')
def AccountDetails():
	if('username' in  session.keys()) and ('user_id' in session.keys()):
		present_user=db.session.query(User).get(session['user_id'])
		return render_template('userAccount.html',current_user=present_user,branches=branches) 	

	return redirect(url_for('users.login'))