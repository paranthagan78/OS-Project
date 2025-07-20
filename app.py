from flask import Flask, render_template, request, redirect, url_for
import restore, backup
import smtplib
import random
from datetime import datetime
from cryptography.fernet import Fernet

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forgetpassword')
def forget_password():
    return render_template('forget_password.html')

@app.route('/feature')
def features():
    return render_template('feature.html')

@app.route('/logout')
def logout():
    return redirect(url_for('welcome'))

users = {'paran': '1234', 'siddarth': '5678'}
user_emails = {'paran': 'paranthagan2311@gmail.com', 'siddarth': 'paranthagan2004@gmail.com'}

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_datetime = datetime.now()
    indian_date_format = current_datetime.strftime("%d/%m/%Y")
    current_time = datetime.now().strftime('%H:%M:%S')

    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        if entered_username in users:
            if entered_password == users[entered_username]:
                return redirect(url_for('home'))

        return render_template('login.html', current_datetime=indian_date_format, current_time=current_time, error='Invalid UserName or Password')
    return render_template('login.html', current_datetime=indian_date_format, current_time=current_time)

email_sender = 'paranthagan2311@gmail.com'
email_password = '' #Enter your Password
session = {}

def send_otp_to_email(email, otp):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, email_password)

    msg = f"Your New OTP is {otp}. Please Don't share this to anyone..."
    server.sendmail(email_sender, email, msg)

    server.quit()

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = request.form['username']

        user_email = user_emails[username]
        otp = ''.join([str(random.randint(0, 9)) for i in range(6)])

        session['otp'] = otp
        session['username'] = username

        send_otp_to_email(user_email, otp)

        return render_template('verify_otp.html', username=username)

    return render_template  ('forget_password.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']

        stored_otp = session.get('otp')
        username = session.get('username')

        if entered_otp == stored_otp and username:
            return redirect(url_for('reset_password'))
        else:
            return render_template('verify_otp.html', error='Invalid OTP. Please try again.')

    return render_template('verify_otp.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if new_password == confirm_new_password:
            username = session.get('username')
            users[username] = new_password

            session.clear()

            return redirect(url_for('login'))
        else:
            return render_template('reset_password.html', error='Passwords do not match.')

    return render_template('reset_password.html')

@app.route('/backup', methods=['GET', 'POST'])
def backup_route():
    encryption_key = None
    
    if request.method == 'POST':
        source = request.form['source'].strip().strip('"')
        destination = request.form['destination'].strip().strip('"')
        compress = 'compress' in request.form
        encrypt = 'encrypt' in request.form
        password = request.form['password'] if encrypt else None
        
        # Debugging output
        print(f"Received source: {source}")
        print(f"Received destination: {destination}")

        try:
            encryption_key = backup.perform_backup(source, destination, compress, encrypt, password)
            session['encryption_key'] = encryption_key  # Store the key in session
        except Exception as e:
            print(f"Error during backup: {e}")
            return f"Error: {e}", 500
        
        return redirect(url_for('home'))
    return render_template('backup.html', encryption_key=encryption_key)


@app.route('/restore', methods=['GET', 'POST'])
def restore_route():
    encryption_key = session.get('encryption_key', None)

    if request.method == 'POST':
        backup_file = request.form['backup_file'].strip().strip('"')
        restore_location = request.form['restore_location'].strip().strip('"')
        decrypt = 'decrypt' in request.form
        password = request.form['password'] if decrypt else None
        
        try:
            restore.perform_restore(backup_file, restore_location, decrypt, password)
            return redirect(url_for('home'))
        except FileNotFoundError as e:
            return str(e), 400  # or render a template with the error message
        except Exception as e:
            return str(e), 500  # or render a template with the error message

    return render_template('restore.html', encryption_key=encryption_key)

if __name__ == '__main__':
    app.run(debug=True)
