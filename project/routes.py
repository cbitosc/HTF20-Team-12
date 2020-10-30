from project import app
from flask import  render_template, url_for, Blueprint, request, session, redirect, escape
from datetime import datetime

@app.route('/')
def home():
	return render_template('layout.html')

@app.route('')