from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=10)

# Define tuition fees and optional fees
tuition_fees = {
    'Nursery': 6500,
    'Grade 1-3': 8500,
    'Grade 4-6': 9000,
    'Grade 7-9': 12000
}

optional_fees = {
    'Food': 2000,
    'Transport': 1500,
    'Admission Fee': 1000,
    'Interview Fee': 500,
    'Diary': 300,
    'Activity Fee': 700,
    'School Supplies': 800,
    'Assessment Tools': 600,
    'Uniform': 1000
}

# User database (in-memory for demonstration purposes)
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash("Username already exists!")
        else:
            users[username] = password
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['username'] = username
            flash("Login successful!")
            return redirect(url_for('fee_calculator'))
        else:
            flash("Invalid username or password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!")
    return redirect(url_for('login'))

@app.route('/fee_calculator', methods=['GET', 'POST'])
def fee_calculator():
    if 'username' not in session:
        flash("Please log in to access this page.")
        return redirect(url_for('login'))

    total_fee = 0
    selected_optional_fees = {}

    if request.method == 'POST':
        grade = request.form['grade']
        term = request.form['term']
        student_name = session['username']
        tuition_fee = tuition_fees.get(grade, 0)
        
        # Calculate optional fees
        for item, price in optional_fees.items():
            if request.form.get(item):
                selected_optional_fees[item] = price
                total_fee += price
        total_fee += tuition_fee
        
        return render_template(
            'invoice.html',
            student_name=student_name,
            grade=grade,
            term=term,
            tuition_fee=tuition_fee,
            optional_fees=selected_optional_fees,
            total_fee=total_fee
        )
    
    return render_template('fee_calculator.html', tuition_fees=tuition_fees, optional_fees=optional_fees)

if __name__ == '__main__':
    app.run(debug=True)
