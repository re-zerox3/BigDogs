from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__, static_url_path='/static/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'dogTracker'
login_manager = LoginManager(app)
login_manager.init_app(app)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    print("he1")
    return User.query.get(uid)

@app.route('/')
def start():
    print("hi")
    isLoggedIn = current_user.is_authenticated
    return render_template('index.html', isLoggedIn=isLoggedIn)

@app.route('/create', methods=['GET', 'POST'])
def create():
    print("hello World1")
    if request.method == 'POST':
        print("hellosssss")
        name = request.form['name']
        print(name)
        age = int(request.form['age'])
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        print("hello World2")
        if user is not None:
            print("hello World3")
            return render_template('create.html', alert="User Already Exists", isLoggedIn = False)
        else:
            print("hell woer4")
            newUser = User(name=name, age=age, username=username, password=password)
            print("vacaa")
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser)
            print("1232")
            return redirect("/")
    print("final go")
    return render_template('create.html')
    

@app.route('/login',  methods=['GET', 'POST'])
def login():
    print("log5")
    if request.method == 'GET':
        print("log6")
        return render_template('login.html', alert="", isLoggedIn = False)
    print("log7")
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    print("log8")
    user = User.query.filter_by(username=username).first()
    print("log88")
    if user is None or user.password != password:
        print("log9")
        return render_template('login.html', alert="INNCORRECT LOGIN", isLoggedIn = False)
    if user.password == password:
        print("log10")
        login_user(user)
        return redirect('/')
    
@app.route('/view_all')
@login_required
def view_all():
    resultList = User.query.all()
    return render_template('view_all.html', resultList=resultList, isLoggedIn=True)

@app.route('/dog_map')
@login_required
def dog_map():
    
    return render_template('dog_map.html', isLoggedIn=True)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        if current_user.password == oldPassword:
            current_user.password = newPassword
            db.session.commit()
            return redirect("/") 
        else:
            return render_template('update.html', alert="MISMATCHED PASSWORD", isLoggedIn=True)
    else:
        return render_template('update.html', alert="", isLoggedIn=True)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
    
@app.errorhandler(404)
def err404(err):
    return render_template('404.html', err=err)

@app.errorhandler(401)
def err401(err):
    return render_template('401.html', err=err)

if __name__ == '__main__':
    app.run()