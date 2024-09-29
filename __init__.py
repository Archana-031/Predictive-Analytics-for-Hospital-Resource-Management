import os
from flask import Flask, request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Omega_Beyond_Infinity'

    @app.route("/", methods=["GET"])
    def index():
        return redirect("/login")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if os.path.exists("user_details.csv"):
                with open("user_details.csv", "r") as f:
                    data = [line.strip().split(",") for line in f.readlines()]

                for user in data:
                    if user[1] == email and check_password_hash(user[2], password):
                        session['authenticated'] = True
                        session['user'] = user[0]  # Store full name in session
                        return redirect("/home")
                flash("Invalid email or password, please try again.", "error")
                return redirect("/login")
            
            flash("No users found. Please register first.", "error")
            return redirect("/register")

        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            full_name = request.form['full_name']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password == confirm_password:
                hashed_password = generate_password_hash(password)
                
                # Data: Full Name, Email, Password
                user_data = [full_name, email, hashed_password]

                with open("user_details.csv", "a") as f:
                    f.write(",".join(user_data))
                    f.write("\n")
                flash("Registration successful! Please log in.", "success")
                return redirect("/login")
            else:
                flash("Passwords do not match! Please try again.", "error")
                return redirect("/register")

        return render_template('signup.html')

    @app.route('/home', methods=['GET'])
    def home():
        if session.get('authenticated'):
            return render_template("home.html", user=session.get('user'))
        else:
            flash("Please log in to access this page.", "error")
            return redirect("/login")

    @app.route('/logout')
    def logout():
        session.clear()
        flash("Logged out successfully.", "success")
        return redirect("/login")

    return app