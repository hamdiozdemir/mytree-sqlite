from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.sql import func
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, PasswordField, validators, SelectField, FileField, EmailField, TextAreaField
from wtforms.validators import InputRequired, ValidationError
from datetime import datetime
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = "somesecretkeyaboutlinktree"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\hamdiozdemir\\Desktop\\Flask\\linktree\\link.db"
UPLOAD_FOLDER = 'static/uploads/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGHT"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


# ------- DATABASE Installations --------
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    bg_choice = db.Column(db.String, default="basic")
    visitors = db.Column(db.Integer, default=0)
    image = db.Column(db.String, default="default.png")


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    about = db.Column(db.String, nullable=True)
    facebook = db.Column(db.String, nullable=True)
    instagram = db.Column(db.String, nullable=True)
    twitter = db.Column(db.String, nullable=True)
    linkedin = db.Column(db.String, nullable=True)
    github = db.Column(db.String, nullable=True)
    youtube = db.Column(db.String, nullable=True)
    spotify = db.Column(db.String, nullable=True)
    tiktok = db.Column(db.String, nullable=True)

    website1_icon = db.Column(db.String, nullable=True)
    website1_name = db.Column(db.String, nullable=True)
    website1_link = db.Column(db.String, nullable=True)

    website2_icon = db.Column(db.String, nullable=True)
    website2_name = db.Column(db.String, nullable=True)
    website2_link = db.Column(db.String, nullable=True)

    website3_icon = db.Column(db.String, nullable=True)
    website3_name = db.Column(db.String, nullable=True)
    website3_link = db.Column(db.String, nullable=True)

    website4_icon = db.Column(db.String, nullable=True)
    website4_name = db.Column(db.String, nullable=True)
    website4_link = db.Column(db.String, nullable=True)

    website5_icon = db.Column(db.String, nullable=True)
    website5_name = db.Column(db.String, nullable=True)
    website5_link = db.Column(db.String, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    link = db.Column(db.String)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    visit = db.Column(db.Boolean, default=True)


class ProfileCounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    visit = db.Column(db.Boolean, default=True)



# ------ FORMS --------

class RegisterForm(Form):
    username = StringField("Username", validators=[validators.Length(min=4), InputRequired(message="You should input a username")])
    name = StringField("First Name", validators=[validators.Length(min=1), InputRequired(message="You should input a name")])
    surname = StringField("Last Name", validators=[validators.Length(min=1), InputRequired(message="You should input a surname")])
    email = EmailField("E-Mail", [InputRequired("Please enter your email.")])
    password = PasswordField("Password", validators=[validators.Length(min=6), InputRequired(message="You should input a password")])
    bg_choice = SelectField(u"Your Background Choice", choices=["basic","simple", "dark", "circles", "stripes", "newyear"])


class LoginForm(Form):
    username = StringField("Username", validators=[validators.Length(min=4)])
    password = PasswordField("Password", validators=[validators.Length(min=6)])


class LinksForm(Form):
    about = TextAreaField("About -Max 140 Character-")
    facebook = StringField("Your Facebook Link")
    instagram = StringField("Your Instagram Link")
    twitter = StringField("Your Twitter Link")
    linkedin = StringField("Your LinkedIn Link")
    github = StringField("Your GitHub Link")
    youtube = StringField("Your Youtube Link")
    spotify = StringField("Your Spotify Link")
    tiktok = StringField("Your TikTok Link")

    website1_icon = SelectField(u"Your Background Choice", choices=["link.png", "profile.png", "dress.png", "shop.png", "light.png", "music.png", "video.png", "blog.png", "chat.png", "book.png", "coffee.png", "important.png", "sun.png", "pet.png", "None"])
    website1_name = StringField("Name")
    website1_link = StringField("Link")

    website2_icon = SelectField(u"Your Background Choice", choices=["link.png", "profile.png", "dress.png", "shop.png", "light.png", "music.png", "video.png", "blog.png", "chat.png", "book.png", "coffee.png", "important.png", "sun.png", "pet.png", "None"])
    website2_name = StringField("Name")
    website2_link = StringField("Link")

    website3_icon = SelectField(u"Your Background Choice", choices=["link.png", "profile.png", "dress.png", "shop.png", "light.png", "music.png", "video.png", "blog.png", "chat.png", "book.png", "coffee.png", "important.png", "sun.png", "pet.png", "None"])
    website3_name = StringField("Name")
    website3_link = StringField("Link")

    website4_icon = SelectField(u"Your Background Choice", choices=["link.png", "profile.png", "dress.png", "shop.png", "light.png", "music.png", "video.png", "blog.png", "chat.png", "book.png", "coffee.png", "important.png", "sun.png", "pet.png", "None"])
    website4_name = StringField("Name")
    website4_link = StringField("Link")

    website5_icon = SelectField(u"Your Background Choice", choices=["link.png", "profile.png", "dress.png", "shop.png", "light.png", "music.png", "video.png", "blog.png", "chat.png", "book.png", "coffee.png", "important.png", "sun.png", "pet.png", "None"])
    website5_name = StringField("Name")
    website5_link = StringField("Link")

    def validate_about(form, field):
        if len(field.data) > 140:
            raise ValidationError("Max lenght is 140 Char.")

class BgForm(Form):
    bg_choice = SelectField(u"Your Background Choice", choices=["basic","simple", "dark", "circles", "stripes", "newyear"], validators=[InputRequired()])

#login required decorator
def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You must login to view this page", "danger")
            return redirect(url_for("login"))
    return decorated_func

def non_login(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not "logged_in" in session:
            return f(**args, **kwargs)
        else:
            flash("You already have a account.", "warning")
            return redirect(url_for("index"))
    return decorated_func



# ----- PAGE VIEWS ----------

@app.route("/")
@app.route("/app")
def index():
    users = db.session.query(Users, Links).join(Users).order_by(Users.visitors.desc()).limit(5)
    return render_template("index.html", users=users)


@app.route("/<username>")
def user(username):
    if  Users.query.filter_by(username=username).first() == None:
        flash("We could not find such a user. Link may not be lasts anymore.", "warning")
        return redirect(url_for("index"))
    else:
        user = Users.query.filter_by(username=username).first()
        user_links = Links.query.filter_by(user_id=user.id).first()
        if not 'logged_in' in session or user.id != session["id"]:
            user.visitors = user.visitors + 1
            visit = ProfileCounter(user_id=user.id)
            db.session.add(visit)
            db.session.commit()
        return render_template("user_page.html", user=user, user_links=user_links)
    

@app.route('/app/register', methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate:
        username = form.username.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        bg_choice = form.bg_choice.data
        if user_checker(username):
            new_user = Users(username=username, name=name, surname=surname, email=email, password=password, bg_choice=bg_choice)
            db.session.add(new_user)
            db.session.commit()
            user_link = Links(user_id=new_user.id)
            db.session.add(user_link)
            db.session.commit()
            flash(f"Welcome to MyTree {name} {surname}. Let's login to continue.")
            return redirect(url_for("login"))
        else:
            flash(f"This username is already in use - {username}, please choose something really cool.", "warning")
            return redirect(url_for("register"))
    else:
        return render_template("register.html", form=form)


@app.route("/app/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        username_entered = form.username.data
        password_entered = form.password.data
        user = Users.query.filter_by(username = username_entered).first()

        if user == None:
            flash("Username or/and Password is incorrect.", "danger")
            return redirect(url_for("login"))
        else:
            password = user.password
            if sha256_crypt.verify(password_entered, password):
                session["logged_in"] = True
                session["username"] = user.username
                session["id"] = user.id
                session["bg_choice"] = user.bg_choice
                session["visitors"] = user.visitors
                flash("You logged in successfully.", "success")
                return redirect(url_for("index"))
            else:
                flash("Username or/and Password is incorrect.", "danger")
                return redirect(url_for("login"))
    else:
        return render_template("login.html", form=form)


@app.route("/app/logout")
@login_required
def logout():
    session.clear()
    flash("You logged out succesfully", "success")
    return redirect(url_for("index"))



@app.route("/app/edit", methods=["GET","POST"])
@login_required
def profile():
    form = LinksForm(request.form)
    if request.method == "POST" and form.validate:
        about = form.about.data
        facebook = http_cleaner(form.facebook.data)
        instagram = http_cleaner(form.instagram.data)
        twitter = http_cleaner(form.twitter.data)
        linkedin = http_cleaner(form.linkedin.data)
        github = http_cleaner(form.github.data)
        youtube = http_cleaner(form.youtube.data)
        spotify = http_cleaner(form.spotify.data)
        tiktok = http_cleaner(form.tiktok.data)
        website1_icon = form.website1_icon.data
        website1_name = form.website1_name.data
        website1_link = http_cleaner(form.website1_link.data)
        website2_icon = form.website2_icon.data
        website2_name = form.website2_name.data
        website2_link = http_cleaner(form.website2_link.data)
        website3_icon = form.website3_icon.data
        website3_name = form.website3_name.data
        website3_link = http_cleaner(form.website3_link.data)
        website4_icon = form.website4_icon.data
        website4_name = form.website4_name.data
        website4_link = http_cleaner(form.website4_link.data)
        website5_icon = form.website5_icon.data
        website5_name = form.website5_name.data
        website5_link = http_cleaner(form.website5_link.data)


        links = Links.query.filter_by(user_id = session["id"]).first()
        links.about=about
        links.facebook=facebook
        links.instagram=instagram
        links.twitter=twitter
        links.linkedin=linkedin
        links.github=github
        links.youtube=youtube
        links.spotify=spotify
        links.tiktok=tiktok
        if website1_icon:
            links.website1_icon=website1_icon
        links.website1_name = website1_name
        links.website1_link=website1_link
        if website2_icon:
            links.website2_icon=website2_icon
        links.website2_name=website2_name
        links.website2_link=website2_link
        if website3_icon:
            links.website3_icon=website3_icon
        links.website3_name=website3_name
        links.website3_link=website3_link
        if website4_icon:
            links.website4_icon=website4_icon
        links.website4_name=website4_name
        links.website4_link=website4_link
        if website5_icon:
            links.website5_icon=website5_icon
        links.website5_name=website5_name
        links.website5_link=website5_link
        db.session.commit()
        flash("Your links have updated.", "success")
        return redirect(url_for("index"))
    else:
        links = Links.query.filter_by(user_id = session["id"]).first()
        if links != None:
            form.about.data=links.about
            form.facebook.data=links.facebook
            form.instagram.data=links.instagram
            form.twitter.data=links.twitter
            form.linkedin.data=links.linkedin
            form.github.data=links.github
            form.youtube.data=links.youtube
            form.spotify.data=links.spotify
            form.tiktok.data=links.tiktok
            # form.website1_icon.data=links.website1_icon
            form.website1_name.data=links.website1_name
            form.website1_link.data=links.website1_link
            # form.website2_icon.data=links.website2_icon
            form.website2_name.data=links.website2_name
            form.website2_link.data=links.website2_link
            # form.website3_icon.data=links.website3_icon
            form.website3_name.data=links.website3_name
            form.website3_link.data=links.website3_link
            # form.website4_icon.data=links.website4_icon
            form.website4_name.data=links.website4_name
            form.website4_link.data=links.website4_link
            # form.website5_icon.data=links.website5_icon
            form.website5_name.data=links.website5_name
            form.website5_link.data=links.website5_link
            return render_template("edit.html", form=form)
        else:
            return render_template("edit.html", form=form)



@app.route("/app/stats")
@login_required
def stats():
    query = sa.select([
        Counter.link,
        sa.func.count(Counter.link)]).filter_by(user_id=session["id"]).group_by(Counter.link)
    links_result = db.session.execute(query).fetchall()
    category = [x[0].upper() for x in links_result]
    category_visit = [x[1] for x in links_result]

    visit_result = db.session.query(func.strftime("%Y-%m-%d", ProfileCounter.timestamp),
    func.count(ProfileCounter.id)).\
    group_by(func.strftime("%Y-%m-%d",
        ProfileCounter.timestamp)).filter(ProfileCounter.user_id==session["id"]).order_by(ProfileCounter.timestamp.asc()).all()
    day = [x[0] for x in visit_result]
    day_visit = [x[1] for x in visit_result]
    return render_template("stats.html", category=category, category_visit=category_visit, day=day, day_visit=day_visit)


@app.route("/app/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/<int:userid>/<string:category>/<path:link_in>")
def linkage(userid, category,link_in):
    link = link_in
    count = Counter(user_id=userid, link=category, visit=True, timestamp=datetime.now())
    db.session.add(count)
    db.session.commit()
    return redirect(f"https://{link}")



@app.route("/app/imageupload", methods=["GET", "POST"])
@login_required
def imageupload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file", "warning")
            return render_template("imageupload.html")
        file = request.files['file']
        if file.filename == '':
            flash("No image selected for uploading", "warning")
            return render_template("imageupload.html")
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            user = Users.query.filter_by(id=session["id"]).first()
            user.image = filename
            session["image"] = user.image
            db.session.commit()
            flash("Image uploaded", "success")
            return redirect(url_for('index'))
        else:
            flash("Only -jpg, jpeg, png, gif- extensions are allowed. Max 16 MB.", "info")
            return redirect(request.url)
    else:
        return render_template("imageupload.html")



@app.route("/app/bg", methods=["GET", "POST"])
@login_required
def bg():
    form = BgForm(request.form)
    user = Users.query.filter_by(id=session["id"]).first()
    if request.method == "POST" and form.validate():
        bg_new = request.form["bg_choice"]
        user.bg_choice = bg_new
        db.session.commit()
        flash(f"You changed your profile background to {bg_new}", "success")
        return redirect(url_for("bg"))

    else:
        request.form.bg_choice = user.bg_choice
        return render_template("bg.html", form=form)



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# ------- UTILS ----------
def user_checker(username):
    if Users.query.filter_by(username=username).first() == None:
        return True
    else:
        return False


def http_cleaner(link):
    separator_index = link.find("//")
    if separator_index != -1:
        link = link[separator_index+2:]
    return link


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)