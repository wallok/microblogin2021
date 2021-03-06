from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm,RegistrationForm 
from flask_login import current_user, login_user, logout_user
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    user={'username': 'miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author':{'username':'Francisco'},
            'body':'(͡• ͜ʖ ͡•)'
        }
    ]
    return render_template('index.html', title='Home page', posts=posts)

@app.route("/login",methods=["GET", "POST"])
@app.route("/index/login",methods=["GET", "POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        flash("login reuested for user {},remeber_me={}".format(form.username.data, form.remeber_me.data))
        return redirect(url_for("index"))
    return render_template("login.html",title="Iniciar Sesion",form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)