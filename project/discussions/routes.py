from flask import  render_template, url_for, Blueprint, session, request, escape, redirect, flash
from project.models import db,User, QuestionThreads, Tags, DTags, Answers, AnswerVotes, TagsFollowing, QFollowing
from project.discussions.forms import QuestionForm, AnswerForm
from sqlalchemy import and_

discussions=Blueprint('discussions',__name__)

@discussions.route('/hello/')
def temp():
	return render_template('FormLayout.html')

@discussions.route('/QuestionsPage/')
def QuesPage():
	if "user_id" in session.keys():
		present_user=db.session.query(User).get(session['user_id'])
		Tags=present_user.user_tags()
		return render_template("QuesPage.html",Tags=Tags)
	else:
		return "ACCESS DENIED"


@discussions.route('/questions',methods=['POST'])
def questions():
	if request.method=="POST":
		if 'option' in request.form.keys():
			option=int(request.form['option'])
			if option==1:
				curr_user=db.session.query(User).get(int(session['user_id']))
				user_questions=curr_user.questions_asked()
				if user_questions==None:
					user_questions=[]
				return render_template("questions.html",questions=user_questions,OnlyOne=False,tag_limit=None,len=len,str=str)
			elif option==2:
				curr_user=db.session.query(User).get(int(session['user_id']))
				user_tags=curr_user.user_tags()
				questions=curr_user.user_follows()
				if questions==None:
					questions=[]
				return render_template("questions.html",questions=questions,OnlyOne=False,tag_limit=None)
			elif option==3:
				tag_id=int(escape(request.form['tag_id']))
				if tag_id!=None:
					tag=db.session.query(Tags).get(int(tag_id))
					questions=tag.get_questions()
				else:
					questions=[]
				return render_template("questions.html",questions=questions,OnlyOne=False,tag_limit=None)
			
			elif option==4:
				allQuestions=db.session.query(QuestionThreads).order_by(QuestionThreads.Qdate.desc()).all()
				return render_template("questions.html",questions=allQuestions,OnlyOne=False,tag_limit=None)
			else:
				return "Explore..."


@discussions.route('/AnswersPage')
def answerPage():
	if "user_id" in session.keys():
		present_user=db.session.query(User).get(session['user_id'])
		Tags=present_user.user_tags()
		Qid=request.args.get('Qid')
		question=db.session.query(QuestionThreads).get(int(Qid))
		present_user_following=False
		if int(Qid) in [x.Qid for x in present_user.user_follows()]:
			present_user_following=True
		answers=question.get_answers()
		return render_template("AnswersPage.html",Tags=Tags,question=question, answers=answers,len=len, present_user_following=present_user_following)
	else:
		return "ACCESS DENIED"



@discussions.route('/AskQuestion/',methods=['POST','GET'])
def askQuestion():
	if ('username' in session.keys()) and ('user_id' in session.keys()):
		if (request.method=='POST') and ('QSubmit' in request.form.keys()):
			Qauthor=int(session['user_id'])
			Qtitle=escape(request.form['Qtitle'])
			QDescription=escape(request.form['Qdescription'])
			QAnonymous=int(request.form['QAnonymous'])
			new_question=QuestionThreads(Qauthor=Qauthor,Qtitle=Qtitle,QDescription=QDescription, QAnonymous=QAnonymous )

			db.session.add(new_question)
			db.session.commit()

			Qtags=list(escape(request.form['QTags']).split())
			
			for tag in Qtags:
				if tag[0]=='#':
					tag_id=db.session.query(Tags.Tagid).filter(Tags.Tagtitle==tag).first()
					if tag_id ==None:
						new_tag=Tags(Tagtitle=tag)
						db.session.add(new_tag)
						db.session.commit()
						tag_id=new_tag

					new_QuesTag=DTags(Tag=tag_id.Tagid,Discussion=new_question.Qid)
					db.session.add(new_QuesTag)
					db.session.commit()
			
			return redirect(url_for('users.homepage'))

		elif request.method=='GET':
			form=QuestionForm()
			return render_template('questionForm.html',form=form)
	else:
		return 'ACCESS DENIED'



@discussions.route('/answerQuestion', methods=['POST','GET'])
def answerQ():
	if "user_id" in session.keys():
		if request.method=="POST":
			Aauthor=int(session['user_id'])
			Atitle=escape(request.form['Atitle'])
			Aans=escape(request.form['AContent'])
			AQid=escape(request.form['answeringTo'])
			new_answer=Answers(Aauthor=Aauthor,Atitle=Atitle,Aans=Aans, AQid=AQid)
			db.session.add(new_answer)
			db.session.commit()
			return redirect(url_for('users.homepage'))
		else:
			form=AnswerForm()
			Qid=int(escape(request.args.get('Qid')))
			if Qid==None:
				return "Not Permitted"
			return render_template("AnswerForm.html", form=form, Qid=Qid)
	else:
		"ACCESS DENIED"



@discussions.route('/reactBlog/',methods=['POST'])
def reactToPost():
	if request.method=="POST":
		if ('Aid' in request.form.keys()):
			previous=db.session.query(AnswerVotes).filter(and_(AnswerVotes.user==int(session['user_id']),AnswerVotes.answer==int(request.form['Aid']) )).first()
			if previous!=None: 
				db.session.delete(previous)
				db.session.commit()
			else:
				post_vote=AnswerVotes(user=int(session['user_id']),vote=1,answer=int(request.form['Aid']))
				db.session.add(post_vote)
				db.session.commit()
			answer=db.session.query(Answers).get(int(request.form['Aid']))
		votes=list(answer.get_upvoters())
		return str(len(votes))
	else:
		pass


@discussions.route('/TagPage')
def TagInfo():
	if "user_id" in session.keys():
		tag_id=escape(request.args.get('tag_id'))
		if tag_id.isdigit():
			TAG=db.session.query(Tags).get(int(tag_id))
			present_user_following=False
			if "user_id" in session.keys():
				if session['user_id'] in [x.TFuserId for x in TAG.getFollowedBy()]:
					present_user_following=True
			return render_template("TagInfo.html", TAG=TAG, present_user_following=present_user_following )
		else:
			return "ACCESS DENIED"
	else:
		return "ACCESS DENIED"

@discussions.route('/tagFollowToggle',methods=['POST','GET'])
def tagFollowToggle():
	tagId=escape(request.args.get('tagId'))
	if ('user_id' in session.keys()) and ('username' in session.keys()):
		if request.method=='POST':
			tag_id=request.form['tagId']
			tag_id=escape(tag_id)
			TagF=db.session.query(TagsFollowing).filter(and_(TagsFollowing.TFuserId==session['user_id'], TagsFollowing.TFtagId==tag_id)).first()
			if TagF==None:
				TagF=TagsFollowing(TFuserId=session['user_id'], TFtagId=tag_id)
				db.session.add(TagF)
				db.session.commit()
			else:
				db.session.delete(TagF)
				db.session.commit()
			return redirect(url_for('discussions.tagFollowToggle', tagId=tag_id))
		else:
			tag_id=escape(tagId)
			TagF=db.session.query(TagsFollowing).filter(and_(TagsFollowing.TFuserId==session['user_id'], TagsFollowing.TFtagId==tag_id)).first()
			if TagF==None:
				return "FOLLOW"
			else:
				return "UNFOLLOW"


@discussions.route('/followDiscussion',methods=['POST','GET'])
def followDiscussion():
	Qid=escape(request.args.get('Qid'))
	if ('user_id' in session.keys()) and ('username' in session.keys()):
		if request.method=='POST':
			Qid=request.form['Qid']
			Qid=escape(Qid)
			DF=db.session.query(QFollowing).filter(and_(QFollowing.user_id==session['user_id'], QFollowing.Question==Qid)).first()
			if DF==None:
				DF=QFollowing(user_id=session['user_id'], Question=Qid)
				db.session.add(DF)
				db.session.commit()
			else:
				db.session.delete(DF)
				db.session.commit()
			return redirect(url_for('discussions.followDiscussion', Qid=Qid))
		else:
			Qid=escape(Qid)
			DF=db.session.query(QFollowing).filter(and_(QFollowing.user_id==session['user_id'], QFollowing.Question==Qid)).first()
			if DF==None:
				return "FOLLOW"
			else:
				return "UNFOLLOW"

@discussions.route('/fetchTags',methods=['POST'])
def fetchTags():
	if ('user_id' in session.keys()) and ('username' in session.keys()):
	
		if request.method=="POST":
			tagTitle=escape(request.form['tagname'])
			if tagTitle=="":
				flash("Tag Not Found...")
				return redirect(url_for('users.homepage'))
			tag=db.session.query(Tags).filter(Tags.Tagtitle==tagTitle).first()
			if tag==None:
				flash("Tag Not Found...")
				return redirect(url_for('users.homepage'))

			return redirect(url_for('discussions.TagInfo', tag_id=tag.Tagid))


@discussions.route("/allQuestions")
def AllQuestions():
	if "user_id" in session.keys():
		present_user=db.session.query(User).get(session['user_id'])
		Tags=present_user.user_tags()
		return render_template("AllQuestions.html",Tags=Tags)
	else:
		return "ACCESS DENIED"