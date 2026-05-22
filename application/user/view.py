from flask import Blueprint, render_template, request, redirect, url_for

from application.extension import db
from application.user.models import User

bp = Blueprint(
    'user',
    __name__,
    url_prefix='/user',
    template_folder="pages"
)


@bp.route('/')
def index():

    users = User.query.all()

    return render_template(
        'user/index.html',
        users=users
    )


@bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        basic_salary = request.form['basic_salary']

        new_user = User(
            username=username,
            email=email,
            basic_salary=basic_salary
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('user.index'))

    return render_template('user/create.html')


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    user = User.query.get_or_404(id)

    if request.method == 'POST':

        user.username = request.form['username']
        user.email = request.form['email']
        user.basic_salary = request.form['basic_salary']

        db.session.commit()

        return redirect(url_for('user.index'))

    return render_template(
        'user/update.html',
        user=user
    )


@bp.route('/delete/<int:id>')
def delete(id):

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('user.index'))