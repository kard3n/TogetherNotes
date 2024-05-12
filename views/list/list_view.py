import flask
import flask_login
import sirope

from model.ListDTO import ListDTO
from model.ListItemDTO import ListItemDTO
from model.UserDTO import UserDTO


def get_blprint():
    list_view = flask.blueprints.Blueprint(
        "list",
        __name__,
        url_prefix="/list",
        template_folder="templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return list_view, syrp


list_blueprint, srp = get_blprint()


@flask_login.login_required
@list_blueprint.route("/create_list", methods=["GET", "POST"])
def create_list():
    usr = UserDTO.current_user()
    if flask.request.method == "GET":
        data = {"user": usr}
        return flask.render_template("create_list.html", **data)
    else:
        name = flask.request.form.get("name")
        description = flask.request.form.get("description")

        if not description:
            flask.flash("Please enter an email address.")
            return flask.redirect("/create_list")

        if not name:
            flask.flash("Please enter a name.")
            return flask.redirect("/create_list")

        new_list = ListDTO(name=name, description=description, owner_oid=usr.oid)
        srp.save(new_list)

        return flask.redirect(f"/list/{new_list.oid}", code=301)


@flask_login.login_required
@list_blueprint.route("/<list_id>", methods=["GET"])
def show_list(list_id):
    usr = UserDTO.current_user()
    current_list = ListDTO.find(srp, int(list_id))

    if (
        current_list is None
        or usr is None
        or usr.oid not in current_list.users_with_access
    ):
        flask.flash("List does not exist or you do not have access to it.")
        return flask.redirect("/home")

    item_list = ListItemDTO.find_for_list(srp, int(list_id))

    data = {"list": current_list, "items": item_list}
    return flask.render_template("show_list.html", **data)
