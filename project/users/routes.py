from datetime import datetime, date
from flask import  render_template, url_for, Blueprint, request, session, redirect, escape, flash, abort
from sqlalchemy import and_
from project.users.forms import RegisterForm, LoginForm, ChangePasswordForm, UpdateAccountForm
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



@users.route('/update-account/',methods=['POST','GET'])
def UpdateAccount():

	if 'username' in session.keys():

		if (request.method=='POST') and ('Submit' in request.form.keys()):

			current_user = User.query.filter_by(Uid=session['user_id']).first()
			current_user.UfirstName=escape(request.form['FirstName'])
			current_user.UlastName=escape(request.form['LastName'])
			if(current_user.UlastName==''):
				current_user.UlastName=None
			current_user.Uusername=escape(request.form['UserName'])
			current_user.Uemail=escape(request.form['UserEmail'])
			current_user.Udescription=escape(request.form['UserDescription'])
			db.session.commit()

			if(current_user.Uusername==session['username']):
				return redirect(url_for('users.mainpage'))
			else:
				return redirect(url_for('users.logout'))

		elif(request.method=='GET'):
			form=UpdateAccountForm()
			current_user=User.query.filter_by(Uid=session['user_id']).first()
			print(current_user)
			form.FirstName.data = current_user.UfirstName
			form.LastName.data = current_user.UlastName
			form.UserName.data = current_user.Uusername
			form.UserEmail.data = current_user.Uemail
			form.UserDescription.data = current_user.UDescription

			return render_template('UpdateAccount.html',user=current_user,form=form)
	else:
		return redirect(url_for('users.login'))




@users.route("/change-password/",methods=['POST','GET'])
def ChangePassword():
	
	if 'username' in session.keys():	
		if (request.method=="POST") and ( 'Submit' in request.form.keys()):

			currentPassword=escape(request.form['currentPassword'])
			newPassword=escape(request.form['newPassword'])
			newPassword1=escape(request.form['reEnterPassword'])
			user = User.query.filter_by(Uid = session['user_id']).first()

			if(newPassword==newPassword1 and currentPassword==user.Upassword):
				user.Upassword = newPassword
				db.session.commit()
				return redirect(url_for('users.homepage'))
			elif(currentPassword!=user.Upassword):
				flash("Current Password did not match")
				return redirect(url_for('users.ChangePassword'))
			else:
				flash("New passwords does not match. Please check again")
				return redirect(url_for('users.ChangePassword'))
		else:
			form=ChangePasswordForm()
			return render_template("ChangePassword.html",form=form)
	else:
		return redirect(url_for('users.login'))




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

@users.route('/DeleteUser/',methods=(['POST']))
def DeleteUser():

	if 'username' in session.keys():	
		if (request.method=="POST"):
			user =  db.session.query(User).get(session['user_id'])
			db.session.delete(user)
			db.session.commit()
			return redirect(url_for('users.logout'))
		else:
			pass
	else:
		abort(401)