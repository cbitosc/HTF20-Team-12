from datetime import datetime, date
from flask import  render_template, url_for, Blueprint, request, session, redirect, escape, flash, abort
from sqlalchemy import and_


users=Blueprint('users',__name__)


@users.route('/')
def temp():
	return render_template('layout.html')