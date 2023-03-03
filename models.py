from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    product = db.relationship('Product', backref='user')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    dis_price = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(255),nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey(
        'subcategory.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.relationship('Comments', backref='product')

    def __init__(self, name, dis_price, price, image_url, description,size_id, color_id, category_id, subcategory_id, user_id):
        self.name = name
        self.dis_price = dis_price
        self.price = price
        self.image_url = image_url
        self.description=description
        self.size_id = size_id
        self.color_id = color_id
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.user_id = user_id

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product = db.relationship('Product', backref='size')

    @classmethod
    def count_size(cls):
        return cls.query.count()

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product = db.relationship('Product', backref='color')

    @classmethod
    def count_color(cls):
        return cls.query.count()

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    product = db.relationship('Product', backref='category')

    @classmethod
    def count_cat(cls):
        return cls.query.count()

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(30), nullable=True)
    messages = db.Column(db.Text, nullable=True)

    def __init__(self, name, email, subject, messages):
        self.name = name
        self.email = email
        self.subject = subject
        self.messages = messages

    def __repr__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comments = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __init__(self, comments, product_id, user_id):
        self.comments = comments
        self.product_id = product_id
        self.user_id = user_id

    @property
    def formatted_time(self):
        return self.time.strftime('%d %B %Y')

    def __repr__(self):
        return self.comments

    def save(self):
        db.session.add(self)
        db.session.commit()


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product = db.relationship(
        'Product', backref=db.backref('favorites', lazy=True))
    __table_args__ = (UniqueConstraint(user_id, product_id), )

    @classmethod
    def count_fav(cls):
        return cls.query.count()

    def __init__(self, product_id, user_id):
        self.product_id = product_id,
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()
