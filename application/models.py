from .database import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(), unique=True, nullable=False)
  email = db.Column(db.String(),unique = True, nullable=False)
  password = db.Column(db.String(), nullable=False)
  type = db.Column(db.String(), default='general')
  ebooks = db.relationship('Ebook', backref='bearer')

class Ebook(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  author = db.Column(db.String(), nullable=False)
  url = db.Column(db.String(), nullable=False)
  status = db.Column(db.String(), default='available')
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)