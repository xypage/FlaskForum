import os

from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskforum.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    # Register other components
    # db management
    from . import db
    db.init_app(app)
    # login/new user management (includes @login_required)
    from . import login
    app.register_blueprint(login.bp)
    # post management (includes comments)
    from . import post
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')


    # Finally just return the app itself
    return app