import json

import flask
import flask_login
import sirope
from flask_login import login_manager

from model.UserDTO import UserDTO
from views.home import home_view
from views.list import list_view
from views.list_item import list_item_view
from views.login_register import login_view, register_view


def create_app():
    lmanager = login_manager.LoginManager()
    fapp = flask.Flask(__name__)
    syrp = sirope.Sirope()
    fapp.config.from_file("config.json", load=json.load)

    # register blueprints
    fapp.register_blueprint(login_view.login_blprint)
    fapp.register_blueprint(register_view.register_blprint)
    fapp.register_blueprint(list_view.list_blueprint)
    fapp.register_blueprint(list_item_view.list_item_blueprint)
    fapp.register_blueprint(home_view.home_blueprint)

    lmanager.init_app(fapp)
    return fapp, lmanager, syrp


app, lm, srp = create_app()


@lm.user_loader
def user_loader(email):
    return UserDTO.find(srp, email)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    flask.flash("User logged out")
    return flask.redirect("/")


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")


@app.route("/")
def get_index():
    usr = UserDTO.current_user()
    # messages_list = list(sirope.Sirope().load_last(MessageDto, 5))
    data = {
        "usr": usr,
    }
    return flask.render_template("index.html", **data)


if __name__ == "__main__":
    app.run()
