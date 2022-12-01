from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, email, password, username):

        return cls(email=email, password=password, username=username)


class Clothing(db.Model):

    __tablename__ = "clothes"

    clothes_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.String)
    size = db.Column(db.String)
    image_path = db.Column(db.String)

    def __repr__(self):
        return f"<Clothes clothes_id={self.clothes_id} name={self.name}>"


class Cart(db.Model):

    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    clothes_id = db.Column(db.Integer, db.ForeignKey("clothes.clothes_id"))

    user = db.relationship("User", backref="clothes")
    clothes = db.relationship("Clothing", backref="clothes")

    def __repr__(self):
        return f"<Cart cart_id={self.cart_id} user_id={self.user_id} clothes_id={self.clothes_id}>"


class Like(db.Model):

    __tablename__ = "likes"

    likes_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    clothes_id = db.Column(db.Integer, db.ForeignKey("clothes.clothes_id"))

    user = db.relationship("User", backref="likes")
    clothes = db.relationship("Clothing", backref="likes")

    def __repr__(self):
        return f"<Likes likes_id={self.likes_id} user_id={self.user_id} clothes_id={self.clothes_id}>"


class Review(db.Model):

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    review_desc = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    clothes_id = db.Column(db.Integer, db.ForeignKey("clothes.clothes_id"))

    user = db.relationship("User", backref="reviews")
    clothing = db.relationship("Clothing", backref="reviews")

    def __repr__(self):
        return f"<Review review_id={self.likes_id} user_id={self.user_id} clothes_id={self.clothes_id} review_desc={self.review_desc}>"


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo=False)
