from application.extension import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    basic_salary = db.Column(
        db.Float,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    payrolls = db.relationship(
        'Payroll',
        backref='user',
        lazy=True,
        passive_deletes=True
    )

    def __repr__(self):
        return f'<User {self.username}>'