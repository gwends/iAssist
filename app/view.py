from app import app, Register
from flask import render_template


@app.route('/register', methods = ['GET', 'POST']) 
def register():
	form = Register()
	return render_template('register.html', form = form)