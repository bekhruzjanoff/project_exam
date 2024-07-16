# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# import re
#
# from config import db, app
# from datetime import datetime
#
# from config import db, app
#
#
# class User_Details(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), unique=True, nullable=False)
#     email = db.Column(db.String(128), unique=True, nullable=False)
#     phone = db.Column(db.String(512), unique=True, nullable=False)
#     password = db.Column(db.String(512), nullable=False)
#     confirm_password = db.Column(db.String(512), nullable=False)
#     create_at = db.Column(db.Date, default=datetime.now())
#
#
# class User_Database(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), unique=True, nullable=False)
#     balance = db.Column(db.Float, nullable=False)
#     create_at = db.Column(db.Date, default=datetime.now())
#
#
# with app.app_context():
#     db.create_all()
#
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     return render_template("home.html")
#
#
# @app.route("/login", methods=["GET", "POST"])
# def detail():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         user = User_Details.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             return render_template("user_menu.html")
#         else:
#             return "Invalid Username or Password", 401
#     return render_template("login.html")
#
#
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")
#     else:
#         hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256')
#         hashed_confing_password = generate_password_hash(request.form.get("confing_passwird"), method='pbkdf2:sha256')
#         u1 = User_Details(username=request.form.get("username"), email=request.form.get("email"),
#                           phone=request.form.get("phone"), password=hashed_password,
#                           confing_passwird=hashed_confing_password)
#         db.session.add(u1)
#         db.session.commit()
#         message = "Blog successfully created"
#         return render_template("register.html", message=message)
#
#
# @app.route("/show_balance", methods=["GET", "POST"])
# def show_balance():
#     if request.method == "POST":
#         username = request.form.get("username")
#         user = User_Database.query.filter_by(username=username).first()
#         if user:
#             return render_template("show_balance.html", balance=user.balance, username=user.username)
#         else:
#             message = ("User not found")
#             return render_template("show_balance.html", message=message)
#     return render_template("show_balance.html")
#
#
# @app.route("/add_balance", methods=["GET", "POST"])
# def add_balance():
#     if request.method == "GET":
#         return render_template("add_balance.html")
#     else:
#         u1 = User_Database(username=request.form.get("username"), balance=request.form.get("balance"))
#         db.session.add(u1)
#         db.session.commit()
#         message = "Balance successfully added"
#         return render_template("add_balance.html", message=message)
#
#
# @app.route("/transfer_money", methods=["GET", "POST"])
# def transfer_money():
#     message = None
#     if request.method == "POST":
#         from_username = request.form.get("from_username")
#         to_username = request.form.get("to_username")
#         amount = request.form.get("balance")
#
#         user1 = User_Database.query.filter_by(username=from_username).first()
#         user2 = User_Database.query.filter_by(username=to_username).first()
#
#         if user1 and user2:
#             if user1.balance >= float(amount):
#                 user1.balance -= float(amount)
#                 user2.balance += float(amount)
#                 db.session.commit()
#                 message = "Transfer successful."
#             else:
#                 message = "Not enough money."
#         else:
#             message = "Not found user."
#
#     return render_template("transfer_money.html", message=message)
#
#
# @app.route("/transfer_history", methods=["GET"])
# def transfer_history():
#     return render_template("transfer_history.html")
#
#
# @app.route("/delete_account", methods=["GET", "POST"])
# def delete_account():
#     if request.method == "POST":
#         username = request.form.get("username")
#         user = User_Database.query.filter_by(username=username).first()
#         if user:
#             db.session.delete(user)
#             db.session.commit()
#             message = "User successfully deleted"
#         else:
#             message = "User not found"
#         return render_template("delete_account.html", message=message)
#     else:
#         return render_template("delete_account.html")
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
