import os
from datetime import date
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 1. LOGIN REQUIRED DECORATOR
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_6782341")

# 2. DATABASE CONFIGURATION
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'birthdays.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. MODELS
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    birthdays = db.relationship('Birthday', backref='owner', lazy=True)

class Birthday(db.Model):
    __tablename__ = 'birthdays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 4. HELPER: COUNTDOWN CALCULATION
def get_days_until(month, day):
    today = date.today()
    try:
        bday = date(today.year, month, day)
        if bday < today:
            bday = bday.replace(year=today.year + 1)
        return (bday - today).days
    except ValueError:
        return 999

# 5. ROUTES
@app.route("/")
@login_required
def index():
    user_id = session.get("user_id")
    selected_month = request.args.get("month")
    
    query = Birthday.query.filter_by(user_id=user_id)
    if selected_month and selected_month.isdigit():
        query = query.filter_by(month=int(selected_month))

    birthdays = query.all()
    for b in birthdays:
        b.days_until = get_days_until(b.month, b.day)

    birthdays.sort(key=lambda x: x.days_until)
    return render_template("index.html", birthdays=birthdays)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Normalize username to lowercase and remove spaces
        username = request.form.get("username", "").lower().strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        if not username or not password or password != confirmation:
            flash("Registration failed: Missing fields or passwords do not match.")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Registration failed: Username already exists.")
            return redirect(url_for("register"))

        new_user = User(username=username, hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        # Normalize input to match database storage
        username = request.form.get("username", "").lower().strip()
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.hash, request.form.get("password")):
            session["user_id"] = user.id
            flash("Login successful: Welcome back!")
            return redirect(url_for("index"))
        
        flash("Login failed: Invalid username or password.")
    return render_template("login.html")

@app.route("/add", methods=["POST"])
@login_required
def add_birthday():
    name = request.form.get("name", "").strip()
    try:
        m = int(request.form.get("month"))
        d = int(request.form.get("day"))
        date(2024, m, d)
        
        if not name:
            raise ValueError
            
        db.session.add(Birthday(name=name, month=m, day=d, user_id=session["user_id"]))
        db.session.commit()
        flash("Birthday added successfully!")
    except (ValueError, TypeError):
        flash("Action failed: Invalid name or date.")
        
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    b = Birthday.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        try:
            m = int(request.form.get("month"))
            d = int(request.form.get("day"))
            date(2024, m, d)
            
            if not name:
                raise ValueError
            
            b.name = name
            b.month = m
            b.day = d
            db.session.commit()
            flash("Update successful!")
            return redirect(url_for("index"))
        except (ValueError, TypeError):
            flash("Update failed: Invalid name or date.")

    return render_template("update.html", birthday=b)

@app.route("/delete", methods=["POST"])
@login_required
def delete():
    b = Birthday.query.filter_by(id=request.form.get("id"), user_id=session["user_id"]).first()
    if b:
        db.session.delete(b)
        db.session.commit()
        flash("Birthday deleted successfully.")
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logout successful: See you soon!")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)