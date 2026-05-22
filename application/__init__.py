import os

from flask import Flask, render_template

from application.extension import db, migrate

from application.user.view import bp as user_bp
from application.post.view import bp as post_bp
from application.payroll.view import bp as payroll_bp

def create_app():

    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)
    database_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key'

    db.init_app(app)
    migrate.init_app(app, db)

    from application.user.models import User
    from application.post.models import Post


    @app.route('/')
    def home():
        return render_template('index.html')

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(payroll_bp)

    return app