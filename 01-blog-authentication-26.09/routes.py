from datetime import date

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from extensions import app, db
from models import BlogPost, User, Comment
from forms import CreatePostForm, RegistrationForm, LoginForm, CommentForm
from security import admin_only


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            User.add_user_to_db(form.email.data, form.password.data, form.name.data)
        except IntegrityError:
            flash("You have already registered. Please login like normal people.", category="info")
            return redirect(url_for("login"))
        else:
            user = User.fetch_from_database(form.email.data)
            login_user(user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are already logged in!", category="success")
    if form.validate_on_submit():
        input_email = form.email.data
        input_password = form.password.data
        user = User.fetch_from_database(input_email)
        if user is not None and check_password_hash(user.password, input_password):  # type: ignore
            login_user(user)
            return redirect(url_for("get_all_posts"))
        else:
            flash("Incorrect credentials.", category="danger")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = db.get_or_404(BlogPost, post_id)
    if not current_user.is_authenticated:
        flash("Log in to comment.", category="info")
    if form.validate_on_submit():
        new_comment = Comment(
            author=current_user,
            post_id=post_id,
            text=form.body.data
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template(
        template_name_or_list="post.html",
        post=requested_post,
        form=form,
        post_id=post_id
    )


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, post_id=post_id)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")
