from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():

    return render_template('homepage.html')


@app.route('/clothes')
def all_clothes():

    clothes = crud.get_clothes()

    return render_template("all_clothes.html", clothes=clothes)


@app.route('/clothes/<clothes_id>')
def show_clothes(clothes_id):

    clothes = crud.get_clothes_by_id(clothes_id)

    return render_template("clothes_details.html", clothes=clothes)


@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again please.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def process_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/logout", methods=["POST"])
def process_logout():
    """Process user logout."""

    logged_in_to_email = session.get("user_email")
    if logged_in_to_email is None:
        flash("You were already logged out!")
    else:
        del session["user_email"]
        flash("You're logged out!")

    return redirect("/")


@app.route("/cart")
def cart():
    get_user = crud.get_user_by_email(session.get("user_email"))

    cart_items = crud.get_cart_items_by_user_id(get_user.user_id)

    return render_template("cart.html", cart_items=cart_items)


@app.route("/clothes/<clothes_id>/carts", methods=["GET", "POST"])
def create_cart_item(clothes_id):

    logged_in = session.get("user_email")

    if logged_in is None:
        flash("Please log in to continue")
    else:
        user = crud.get_user_by_email(logged_in)
        item = crud.get_clothes_by_id(clothes_id)

        cart_item = crud.create_cart_clothes(user.user_id, item.clothes_id)

        db.session.add(cart_item)
        db.session.commit()

        flash(f" {item.name} has been added to your cart")

    return redirect(f"/clothes")


@app.post("/carts/<clothes_id>/delete")
def delete_cart(clothes_id):
    crud.delete_cart_clothes(clothes_id)
    return redirect("/cart")


@app.route("/carts/subtotal")
def subtotal(clothes_id):
    total = crud.cart_total(clothes_id)

    return render_template("cart.html", total=total)


@app.route("/likes")
def like():
    get_user = crud.get_user_by_email(session.get("user_email"))

    liked_items = crud.get_liked_clothes_by_user_id(get_user.user_id)

    return render_template("likes.html", liked_items=liked_items)


@app.route("/clothes/<clothes_id>/likes", methods=["GET", "POST"])
def create_liked_item(clothes_id):

    logged_in = session.get("user_email")

    if logged_in is None:
        flash("Please log in to continue")
    else:
        user = crud.get_user_by_email(logged_in)
        item = crud.get_clothes_by_id(clothes_id)

        liked_item = crud.create_liked_clothes(user.user_id, item.clothes_id)

        db.session.add(liked_item)
        db.session.commit()

        flash(f" {item.name} has been added to your likes!")

    return redirect(f"/clothes")


@app.post("/likes/<clothes_id>/delete")
def delete_likes(clothes_id):
    crud.delete_liked_clothes(clothes_id)
    return redirect("/likes")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
