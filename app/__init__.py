from flask import Flask
from .auth.views import login_manager
from .utils import db
from .models.user import User
from .models.poll import Poll
from flask_migrate import Migrate
from .config.config import config_dict
from .auth.views import authblp
from .resources.views import voteblp

def create_app(config=config_dict["dev"]):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.login_view = "login"

    login_manager.init_app(app)

    app.register_blueprint(authblp)
    app.register_blueprint(voteblp)
   

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "user":User,
            "vote":Poll
        }

    return app
