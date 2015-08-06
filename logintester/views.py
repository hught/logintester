from logintester import app, db
from flask import make_response, \
        render_template, request, \
        session, redirect, url_for, g
from werkzeug import generate_password_hash, check_password_hash
from functools import wraps

users = db.users

def login_required(f):
    @wraps(f)
    def inner_func(*args, **kwargs):
        if g.user['name'] is None:
            return redirect(url_for('login', next=request.url))# can do a next=request.url here if you'd like
        return f(*args, **kwargs)
    return inner_func

@app.before_request
def load_user():
    if session.get('user_id', None):
        user = db.users.find_one({'name': session['user_id']})
    else:
        user = {'name': None}
    g.user = user

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


@app.route('/home')
def home():
    is_logged_in = session.get('logged_in', None)
    user = g.get('user', None)
    return render_template('home.html', is_logged_in=is_logged_in)

@app.route('/create_user', methods=['GET'])
def create_user():
    pwdhash = generate_password_hash('test')
    users.insert([{'name': 'huw', 'pwdhash': pwdhash}])
    return render_template('test.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/login')
def login():
    user = request.args.get('id', None) 
    if not user:
        return 'No request.args.get("id") supplied'
    user = db.users.find_one({'name': user})
    if not user:
        return 'User does not exist'

    password = request.args.get('pwd', None)
    if not password:
        return 'No request.args.get("pwd") supplied'
    is_pwd = check_password_hash(user['pwdhash'], password)
    if is_pwd:
        # password correct, do session stuff
        session['logged_in'] = True
        session['user_id'] = user['name']
        if request.args.get('next'):
            next = request.args.get('next')
            return redirect(next)
        return redirect(url_for('home'))

    return 'Incorrect password'
    
