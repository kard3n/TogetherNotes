import flask
import flask_login
import sirope

from model.UserDTO import UserDTO


def get_blprint():
    login = flask.blueprints.Blueprint(
        "login",
        __name__,
        url_prefix="/login",
        template_folder="views/login_register/templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return login, syrp


login_blprint, srp = get_blprint()


@login_blprint.route("/", methods=["GET", "POST"])
def login():
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    else:
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        if not email:
            flask.flash("Please enter an email address")
            return flask.redirect("/login")

        if not password:
            flask.flash("Please enter a password")
            return flask.redirect("/login")

        usr = UserDTO.find(srp, email)
        if not usr or not usr.chk_password(password):
            print(usr)
            flask.flash("Username and or email invalid. Please try again.")
            return flask.redirect("/login")

        flask_login.login_user(usr)

        return flask.redirect("/my_lists", code=200)
