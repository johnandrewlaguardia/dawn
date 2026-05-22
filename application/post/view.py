from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from application.extension import db
from application.post.models import Post

bp = Blueprint(
    'post',
    __name__,
    url_prefix='/post',
    template_folder="pages"
)


@bp.route('/')
def index():

    posts = Post.query.all()

    return render_template(
        'post/index.html',
        posts=posts
    )


@bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        title = request.form['title']
        body = request.form['body']

        new_post = Post(
            username=username,
            email=email,
            title=title,
            body=body
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('post.index'))

    return render_template('post/create.html')


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    post = Post.query.get_or_404(id)

    if request.method == 'POST':

        post.title = request.form['title']
        post.body = request.form['body']

        db.session.commit()

        return redirect(url_for('post.index'))

    return render_template(
        'post/update.html',
        post=post
    )


@bp.route('/delete/<int:id>')
def delete(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('post.index'))