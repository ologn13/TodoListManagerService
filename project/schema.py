from project import db
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='owner')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def update_user(cls, username, email):
        user = cls.query.filter_by(username=username).first()
        user.email = email
        db.session.commit()

    @classmethod
    def delete_user(cls, username):
        user = cls.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    heading = db.Column(db.String(360))
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_task_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def update_task(cls, id, heading, description, is_completed):
        task = cls.query.filter_by(id=id).first()
        task.heading = heading
        task.description = description
        task.is_completed = is_completed
        db.session.commit()

    @classmethod
    def delete_task(cls, id):
        task = cls.query.filter_by(id=id).first()
        db.session.delete(task)
        db.session.commit()


class RevokedTokens(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_token_revoked(cls, token):
        query = cls.query.filter_by(token=token).first()
        return bool(query)
