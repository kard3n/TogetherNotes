import flask
import flask_login
import sirope

from model.UserDTO import UserDTO


def get_blprint():
    register = flask.blueprints.Blueprint(
        "register",
        __name__,
        url_prefix="/register",
        template_folder="templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return register, syrp


register_blprint, srp = get_blprint()


@register_blprint.route("/", methods=["GET", "POST"])
def register():
    if flask.request.method == "GET":
        return flask.send_from_directory(
            register_blprint.static_folder, "register.html"
        )
    else:
        name = flask.request.form.get("name")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")

        if not email:
            flask.flash("Please enter an email address.")
            return flask.redirect("/")

        if not password:
            flask.flash("Please enter a password.")
            return flask.redirect("/")

        if not name:
            flask.flash("Please enter a name.")
            return flask.redirect("/")

        usr = UserDTO.find(srp, email)
        if usr:
            flask.flash("Email address already in use. Please try with another.")
            return flask.redirect("/")

        usr = UserDTO(email=email, password=password, name=name)
        flask_login.login_user(usr)

        return flask.redirect("/my_lists", code=200)
