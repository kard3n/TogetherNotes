import flask
import flask_login
import sirope

from model.InvitationDTO import InvitationDTO
from model.ListDTO import ListDTO
from model.UserDTO import UserDTO


def get_blprint():
    list_view = flask.blueprints.Blueprint(
        "home",
        __name__,
        url_prefix="/home",
        template_folder="templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return list_view, syrp


home_blueprint, srp = get_blprint()


@flask_login.login_required
@home_blueprint.route("/", methods=["GET"])
def home():
    usr = UserDTO.current_user()

    lists = ListDTO.find_for_user(srp, usr.oid)

    data = {
        "lists": lists,
        "user": usr,
        "invites": InvitationDTO.find_for_user(srp, usr.oid),
    }
    return flask.render_template("home.html", **data)
