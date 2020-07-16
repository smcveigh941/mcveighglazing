from builtins import len

from flask import Flask, render_template, request, redirect, session, send_from_directory, url_for
from flask_mail import Mail, Message
from settings import get_project_settings
import os
import json

app = Flask(__name__)

app.config.update(get_project_settings())

mail = Mail(app)

SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True


@app.route('/sitemap.xml')
def sitemap_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/robots.txt')
def robots_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/sendmessage", methods=['POST'])
def sendmessage():
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    message = request.form['message']
    honeypot = request.form['address']

    if len(honeypot) > 0:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    blacklisted_words = [line.rstrip('\n') for line in os.open('blacklist.txt')]
    message_ok = True

    for word in blacklisted_words:
        if (" " + word + " ") in message.lower():
            message_ok = False
            break

    if message_ok:
        msg = Message('Job Query', sender=app.config.get('MAIL_USERNAME'), recipients=app.config.get('MAIL_RECIPIENTS'))
        msg.body = name + " has sent you a message using the website.\n\n" + "Phone Number: " + number + "\nEmail: " + email + "\n\nMessage: \n\n" + message
        mail.send(msg)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('main', _external=False, _scheme='https'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
