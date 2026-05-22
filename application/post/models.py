from application.extension import db

class Post(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    body = db.Column(
        db.Text,
        nullable=False
    )