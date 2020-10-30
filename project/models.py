from datetime import datetime
from sqlalchemy import and_
from project import db


class User(db.Model):
	Uid=db.Column(db.Integer, primary_key=True)
	UfirstName=db.Column(db.String(30), nullable=False)
	UlastName=db.Column(db.String(30), nullable=True)
	Uusername=db.Column(db.String(20),unique=True,nullable=False)
	Uemail=db.Column(db.String(80), nullable=True)
	UDescription=db.Column(db.String(300), nullable=True)
	Upassword=db.Column(db.String(40),nullable=False)
	Udob=db.Column(db.Date,nullable=True)
	UprofilePic=db.Column(db.String(80),default="temp_pic.jpg",nullable=False)
	UstudyYear=db.Column(db.Integer, nullable=False)
	URole=db.Column(db.Integer, db.ForeignKey('role.RoleId', ondelete="set null"))
	UBranch=db.Column(db.Integer, db.ForeignKey('branch.BranchId', ondelete="set null"))

	def user_tags(self):
		tags_dict=db.session.query(Tags).join(TagsFollowing, Tags.Tagid==TagsFollowing.TFtagId).filter(self.Uid==TagsFollowing.TFuserId).all()
		return tags_dict

	def questions_asked(self):
		ques_dict=db.session.query(QuestionThreads).filter(QuestionThreads.Qauthor==self.Uid).all()
		return ques_dict

	 


class Role(db.Model):
	RoleId=db.Column(db.Integer, primary_key=True)
	RoleName=db.Column(db.String(30),  nullable=False)

class Branch(db.Model):
	BranchId=db.Column(db.Integer, primary_key=True)
	BrancName=db.Column(db.String(30), nullable=False)



class QuestionThreads(db.Model):
	Qid=db.Column(db.Integer,primary_key=True)
	QAnonymous=db.Column(db.Integer, nullable=False, default=0)
	Qauthor=db.Column(db.Integer,db.ForeignKey('user.Uid',ondelete="cascade"),nullable=False)
	Qtitle=db.Column(db.String(20),nullable=False)
	QDescription=db.Column(db.String(1000),nullable=False)
	Qdate=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)


class QFollowing(db.Model):
	Question=db.Column(db.Integer,db.ForeignKey('question_threads.Qid',ondelete="cascade"),primary_key=True)
	user_id=db.Column(db.Integer,db.ForeignKey('user.Uid',ondelete="cascade"),primary_key=True)
	

class Answers(db.Model):
	Aid=db.Column(db.Integer,primary_key=True)
	AQid=db.Column(db.Integer,db.ForeignKey('question_threads.Qid',ondelete="cascade"),nullable=False)
	AAnonymous=db.Column(db.Integer, nullable=False, default=0)
	Aauthor=db.Column(db.Integer, db.ForeignKey("user.Uid", ondelete="cascade"), nullable=True)
	Atitle=db.Column(db.String(100),nullable=False)
	Aans=db.Column(db.String(2000),nullable=False)
	Adate=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	AreplyingTo=db.Column(db.Integer, db.ForeignKey('answers.Aid',ondelete="cascade"), nullable=True)
	
class AnswerVotes(db.Model):
	user=db.Column(db.Integer, db.ForeignKey("user.Uid",ondelete="cascade"), primary_key=True )
	answer=db.Column(db.Integer,db.ForeignKey("answers.Aid", ondelete="cascade"),primary_key=True)
	vote=db.Column(db.Integer, nullable=False)
	#1 for like 0 for dislike...
	


class Tags(db.Model):
	Tagid=db.Column(db.Integer, primary_key=True)
	Tagtitle=db.Column(db.String(30), nullable=False)

class TagsFollowing(db.Model):
	TFuserId=db.Column(db.Integer, db.ForeignKey('user.Uid'),primary_key=True)
	TFtagId=db.Column(db.Integer, db.ForeignKey('tags.Tagid'),primary_key=True)

class DTags(db.Model):
	Tag=db.Column(db.Integer,db.ForeignKey('tags.Tagid'),primary_key=True)
	Discussion=db.Column(db.Integer,db.ForeignKey('question_threads.Qid',ondelete="cascade"),primary_key=True)


class Reports(db.Model):
	Rep_id=db.Column(db.Integer, primary_key=True)
	Rep_title=db.Column(db.String(100), nullable=False )


class DQuestionReport(db.Model):
	DQreport=db.Column(db.Integer, db.ForeignKey('question_threads.Qid',ondelete="cascade"), primary_key=True )
	DQcomplaintId=db.Column(db.Integer, db.ForeignKey('reports.Rep_id',ondelete="cascade"), primary_key=True)
	DQreportedBy=db.Column(db.Integer, db.ForeignKey('user.Uid',ondelete='cascade'),nullable=False)
	DQmessage=db.Column(db.String(200), nullable=True)

class DAnswerReport(db.Model):
	DAreport=db.Column(db.Integer, db.ForeignKey('answers.Aid',ondelete="cascade"), primary_key=True )
	DAcomplaintId=db.Column(db.Integer, db.ForeignKey('reports.Rep_id',ondelete="cascade"), primary_key=True)
	DAreportedBy=db.Column(db.Integer, db.ForeignKey('user.Uid',ondelete='cascade'),nullable=False)
	DAmessage=db.Column(db.String(200), nullable=True)



class Notifications(db.Model):
	Nid=db.Column(db.Integer, primary_key=True)
	NUserId=db.Column(db.Integer, db.ForeignKey("user.Uid", ondelete="cascade"))
	Nmessage=db.Column(db.String(100), nullable=False)
	NLink=db.Column(db.String(150))
	Ndatetime=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
