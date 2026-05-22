from application.extension import db
from datetime import datetime


class Payroll(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    allowance = db.Column(
        db.Float,
        default=0,
        nullable=False
    )

    deduction = db.Column(
        db.Float,
        default=0,
        nullable=False
    )

    overtime = db.Column(
        db.Float,
        default=0,
        nullable=False
    )

    salary_snapshot = db.Column(
        db.Float,
        nullable=False
    )

    employee_name = db.Column(
        db.String(100),
        nullable=False
    )

    net_pay = db.Column(
        db.Float,
        nullable=False
    )

    payroll_date = db.Column(
        db.String(100),
        nullable=False
    )

    payroll_period = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
        'user.id',
        ondelete='SET NULL'
    ),
    nullable=True
)