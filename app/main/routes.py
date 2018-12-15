from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('users.home', username=current_user.username, post_page=1, hired_page=1, history_page=1))
    return render_template('land_page.html', title="Home")
