from .extention import db


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    work = db.Column(db.String(100))
    age = db.Column(db.Integer)


db.create_all()
db.session.commit()
