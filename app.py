from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_mail import Mail, Message
import time
import datetime
from PIL import Image, ExifTags
import sqlite3
import os
from settings import get_project_settings

app = Flask(__name__)

app.config.update(get_project_settings())

mail = Mail(app)


@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


def get_connection():
    return sqlite3.connect(app.config['DATABASE'])


def initialize_db():
    if not os.path.isfile(app.config['DATABASE']):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS story")
        cur.execute("CREATE TABLE story(id TEXT, name TEXT, date TEXT, message TEXT, approved TEXT)")
        conn.close()


def get_stories(show_approved):
    show_approved = int(show_approved)
    if show_approved:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('select * from story')
    else:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('select * from story where approved = "1"')

    ar = [[str(item) for item in results] for results in cur.fetchall()]
    return ar


def add_story(story):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('insert into story values(?,?,?,?,?)', (str(int(time.time() * 100)), story['name'], datetime.date.today().strftime('%d/%m/%y'), story['message'], "0"))
    conn.commit()
    conn.close()


def set_story_approved(story_id, approved):
    approved = str(int(approved))
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('update story set approved = ? where id = ?', (approved, story_id))
    conn.commit()
    conn.close()


def delete_story(story_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('delete from story where id = ?', (story_id,))
    conn.commit()
    conn.close()


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/manage_story", methods=['POST'])
def manage_story():
    stories = get_stories(True)
    if request.form['submit'] == 'public':
        for i in range (0, len(stories)):
            set_story_approved(stories[i][0], ("[" + str(i) + "]") in request.form.keys())
    else:
        for i in range (0, len(stories)):
            if ("[" + str(i) + "]") in request.form.keys():
                delete_story(stories[i][0])

    return redirect("/testimonials")


@app.route("/sendmessage", methods=['POST'])
def sendmessage():
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    message = request.form['message']
    msg = Message('Job Query', sender=app.config.get('MAIL_USERNAME'), recipients=app.config.get('MAIL_RECIPIENTS'))
    msg.body = name + " has sent you a message using the website.\n\n" + "Phone Number: " + number + "\nEmail: " + email + "\n\nMessage: \n\n" + message
    mail.send(msg)
    return redirect('/contact?message-sent=true')


@app.route("/submitstory", methods=['POST'])
def submit_story():
    name = request.form['name']
    story = request.form['story']
    add_story(dict(name=name, message=story))
    msg = Message('Story Submitted', sender=app.config.get('MAIL_USERNAME'), recipients=app.config.get('MAIL_RECIPIENTS'))
    msg.body = "Someone has submitted a testimonial to the website.\n\n" + "Name: " + name + "\n\nMessage: \n\n" + story + "\n\nLog in to the website to review this testimonial"
    mail.send(msg)
    return redirect('/testimonials?story-sent=true')


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    input = request.form['authcode']
    if input == app.config.get('AUTH_PASSWORD'):
        session['admin'] = "True"
        return redirect('/')
    else:
        return render_template('error.html', error=dict(title="Authorisation Code Invalid",
                                                        message="The authorisation code you entered was not valid. "
                                                                "Please return to the home screen where you can try to log in again."))


@app.route("/gallery")
def gallery():
    items_per_page = 16
    page = request.args.get('page')
    if page is None:
        page = 0
    else:
        page = int(page)
    files = []

    if os.path.exists("static/images/uploads"):
        for f in os.listdir("static/images/uploads"):
            if f.endswith(".jpg"):
                files.append(f)

    return render_template('gallery.html', admin=('admin' in session),
                           column_0=list(reversed(files[page*items_per_page:items_per_page*(page+1):4])), column_1=list(reversed(files[(page*items_per_page)+1:items_per_page*(page+1)+1:4])), column_2=list(reversed(files[(page*items_per_page)+2:items_per_page*(page+1)+2:4])),
                           column_3=list(reversed(files[(page*items_per_page)+3:items_per_page*(page+1)+3:4])), page=page,
                           prev_button=(page > 0), next_button=((page+1) * items_per_page < (len(files))))


@app.route("/delete")
def delete_image():
    file = request.args.get('file')
    page = request.args.get('page')
    os.remove(os.path.join('static/images/uploads', file))
    return redirect('/gallery?page=' + page)


@app.route("/testimonials")
def testimonials():
    return render_template('testimonials.html', admin=('admin' in session), stories=get_stories('admin' in session))


@app.route("/where")
def where():
    return render_template('where.html')


@app.route("/")
def main():
    return render_template('index.html', admin=('admin' in session))


@app.route('/upload', methods=['POST'])
def upload():
    date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    timestamp_id = -1
    for file in request.files.getlist('file[]'):
        timestamp_id += 1
        new_name = date_time + str(timestamp_id) + ".jpg"
        if not os.path.exists("static/images/uploads"):
            os.makedirs('static/images/uploads')
        image = Image.open(file)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)

        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        image.save(os.path.join('static/images/uploads', new_name))
        image.close()
    return redirect('/gallery')


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=dict(title="Something's Wrong!",
                                                    message="Fortunately, we are on the job and you can just return home")), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=dict(title="Page not found",
                                                    message="The page you were looking for is not here. Fortunately, you can just return home")), 404


if __name__ == "__main__":
    initialize_db()
    app.run(host='0.0.0.0')
