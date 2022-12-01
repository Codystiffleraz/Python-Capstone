from model import db, User, Clothing, Like, Review, Cart, connect_to_db


def create_user(email, password):

    user = User(email=email, password=password)

    return user


def get_user():

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

# ---------------------------------------------------------


def create_clothes(name, description, price, size, image_path):

    clothing = Clothing(
        name=name,
        description=description,
        price=price,
        size=size,
        image_path=image_path
    )
    return clothing


def get_clothes():

    return Clothing.query.all()


def get_clothes_by_id(clothes_id):

    return Clothing.query.get(clothes_id)


def get_clothes_by_clothes_id(clothes_id):
    clothes = Clothing.query.get(clothes_id())
    return clothes


# ------------------------------------------------------------

def create_cart_clothes(user_id, clothes_id):
    cart = Cart(
        user_id=user_id,
        clothes_id=clothes_id,
    )
    return cart


def get_cart_items_by_user_id(user_id):
    return Cart.query.filter(Cart.user_id == user_id).all()


def get_cart_by_cart_id(cart_id):
    cart_session = Cart.query.get(cart_id)
    return cart_session


def delete_cart_clothes(clothes_id):
    cart_item = Cart.query.get(clothes_id)
    db.session.delete(cart_item)
    db.session.commit()


def create_liked_clothes(user_id, clothes_id):
    like = Like(
        user_id=user_id,
        clothes_id=clothes_id,
    )
    return like


def get_liked_clothes_by_user_id(user_id):
    return Like.query.filter(Like.user_id == user_id).all()


def get_likes_by_likes_id(likes_id):
    likes_session = Like.query.get(likes_id)
    return likes_session


def delete_liked_clothes(clothes_id):
    liked_clothes = Like.query.get(clothes_id)
    db.session.delete(liked_clothes)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)
