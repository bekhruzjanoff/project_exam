from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re, os

# from flask_migrate import Migrate

app = Flask(__name__)

app.config['DATABASE_URL'] = 'db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User_details.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# Create a 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(512), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    confirm_password = db.Column(db.String(512), nullable=False)
    create_at = db.Column(db.Date, default=datetime.now())


class User_Database(db.Model):
    tablename = 'User_Database'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.Date, default=datetime.now())


# Transfer History Table
class TransferHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_username = db.Column(db.String(128), nullable=False)
    to_username = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Record the time of the transfer


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def detail():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User_Details.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return render_template("user_menu.html")
        else:
            return "Invalid Username or Password", 401
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Basic validation
        if not all([username, email, phone, password, confirm_password]):
            message = "Please fill out all fields."
            return render_template("register.html", message=message)

        # Check if passwords match
        if password != confirm_password:
            message = "Passwords do not match."
            return render_template("register.html", message=message)

        # Generate password hashes
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        hashed_confirm_password = generate_password_hash(confirm_password, method='pbkdf2:sha256')

        # Create new user
        u1 = User_Details(username=username, email=email,
                          phone=phone, password=hashed_password,
                          confirm_password=hashed_confirm_password)

        # Add to database
        db.session.add(u1)
        db.session.commit()

        # Success message
        message = "Registration successful!"
        return render_template("register.html", message=message)


@app.route("/show_balance", methods=["GET", "POST"])
def show_balance():
    if request.method == "POST":
        username = request.form.get("username")
        user = User_Database.query.filter_by(username=username).first()
        if user:
            return render_template("show_balance.html", balance=user.balance, username=user.username)
        else:
            message = ("User not found")
            return render_template("show_balance.html", message=message)
    return render_template("show_balance.html")


@app.route("/add_balance", methods=["GET", "POST"])
def add_balance():
    if request.method == "GET":
        return render_template("add_balance.html")
    else:
        username = request.form.get("username")
        balance = request.form.get("balance")

        
        if not all([username, balance]):
            message = "Пожалуйста, заполните все поля."
            return render_template("add_balance.html", message=message)

        
        try:
            balance = float(balance)
        except ValueError:
            message = "Неверный формат суммы баланса."
            return render_template("add_balance.html", message=message)

       
        existing_user = User_Database.query.filter_by(username=username).first()
       
        if existing_user:
            
            existing_user.balance += float(balance)  
            db.session.commit()
            message = "Баланс успешно обновлен!"
            return render_template("add_balance.html", message=message)

        
        u1 = User_Database(username=username, balance=balance)
        db.session.add(u1)
        db.session.commit()

       
        message = "Баланс успешно добавлен"
        return render_template("add_balance.html", message=message)

@app.route("/transfer_money", methods=["GET", "POST"])
def transfer_money():
    message = None
    if request.method == "POST":
        from_username = request.form.get("from_username")
        to_username = request.form.get("to_username")
        amount = request.form.get("balance")

        user1 = User_Database.query.filter_by(username=from_username).first()
        user2 = User_Database.query.filter_by(username=to_username).first()

        if user1 and user2:
            if user1.balance >= float(amount):
                user1.balance -= float(amount)
                user2.balance += float(amount)
                db.session.commit()

                # Record transfer history
                transfer = TransferHistory(from_username=from_username,
                                           to_username=to_username,
                                           amount=float(amount))
                db.session.add(transfer)
                db.session.commit()

                message = "Transfer successful."
            else:
                message = "Not enough money."
        else:
            message = "Not found user."

    return render_template("transfer_money.html", message=message)

@app.route('/user_menu')
def user_menu():
    # Logic to render user menu page (user_menu.html)
    return render_template('user_menu.html')


@app.route("/transfer_history")
def transfer_history():
    transfers = TransferHistory.query.order_by(TransferHistory.timestamp.desc()).all()
    return render_template("transfer_history.html", transfers=transfers)


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        username = request.form.get("username")
        user = User_Database.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            message = "User successfully deleted"
        else:
            message = "User not found"
        return render_template("delete_account.html", message=message)
    else:
        return render_template("delete_account.html")


if __name__ == "__main__":
    app.run(debug=True)
