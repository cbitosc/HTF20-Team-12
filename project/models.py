from datetime import datetime
from sqlalchemy import and_
from project import db


class User(db.Model):
	Uid=db.Column(db.Integer, primary_key=True)
	UfirstName=db.Column(db.String(30), nullable=False)
	UlastName=db.Column(db.String(30), nullable=True)
	Uusername=db.Column(db.String(20),unique=True,nullable=False)
	Uemail=db.Column(db.String(80), nullable=True)
	Upassword=db.Column(db.String(40),nullable=False)
	Udob=db.Column(db.Date,nullable=True)
	UprofilePic=db.Column(db.String(80),default="temp_pic.jpg",nullable=False)

class QuestionThreads(db.Models):
	pass

class Answers(db.Model):
	pass

class Tags(db.Models):
	pass

class TagsFollowing(db.Models):
	pass

class DTags(db.Model):
	pass

class ComplaintForReports(db.Model):
	pass

class DQuestionReport(db.Model):
	pass

class DAnswerReport(db.Model):
	pass



