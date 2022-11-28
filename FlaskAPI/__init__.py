from flask import Flask


def Build_App():
    app = Flask(__name__)
    app.jinja_env.filters['zip'] = zip
    app.config['SECRET_KEY'] = 'cefd0cdafc081c7fdde5caf6f96edf6e'
    

    from .routes import routes # Define Page routing
    from .analysis import analysis
    

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(analysis, url_prefix='/')
    

    return app