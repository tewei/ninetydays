from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt
from app import app
from app import login

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user_basic.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user_basic.id'))
)

mission_association = db.Table('mission_association',
    db.Column('user_basic_id', db.Integer, db.ForeignKey('user_basic.id')),
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'))
)

class UserBasic(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    physiologs = db.relationship('PhysioLog', backref='user', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))
    mission = db.relationship('Mission')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'UserBasic', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    # def followed_posts(self):
    #     return Post.query.join(
    #         followers, (followers.c.followed_id == Post.user_id)).filter(
    #             followers.c.follower_id == self.id).order_by(
    #                 Post.timestamp.desc())

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return UserBasic.query.get(id)

    def __repr__(self):
        return '<UserBasic {}>'.format(self.username)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    category = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_type = db.Column(db.String(140))
    level = db.Column(db.String(140))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    prize = db.Column(db.Float)
    active = db.Column(db.String(140))
    # body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))
    physiologs = db.relationship('PhysioLog', backref='mission', lazy='dynamic')
    users = db.relationship("UserBasic", back_populates="mission")

    def __repr__(self):
        return '<Mission {}>'.format(self.body)

class PhysioLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    physio_type = db.Column(db.String(140))
    physio_subtype = db.Column(db.String(140))
    physio_verify = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))

    def __repr__(self):
        return '<PhysioLog {}>'.format(self.body)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    transaction_type = db.Column(db.String(140))
    transaction_comment = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.id'))

    def __repr__(self):
        return '<Transaction {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return UserBasic.query.get(int(id))

