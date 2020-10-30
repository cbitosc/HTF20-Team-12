from flask import  render_template, url_for, Blueprint

discussions=Blueprint('discussions',__name__)

@discussions.route('/hello/')
def temp():
	return render_template('FormLayout.html')