import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
import os

load_dotenv()  # Memuat variabel dari file .env

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Konfigurasi logging
logging.basicConfig(filename='app.log', level=logging.INFO)

class ContactForm(FlaskForm):
    name = StringField('Nama', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Alamat email tidak valid')])
    message = TextAreaField('Pesan', validators=[DataRequired()])
    submit = SubmitField('Kirim')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Proses pengiriman pesan (misalnya, simpan ke database atau kirim email)
        flash('Terima kasih atas pesan Anda! Saya akan segera menghubungi Anda.', 'success')
        return redirect(url_for('home'))  # Mengarahkan ke halaman home setelah pengiriman
    return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"500 error: {str(e)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
