import flask
import flask_login
import sirope

from model.InvitationDTO import InvitationDTO
from model.ListDTO import ListDTO
from model.ListItemDTO import ListItemDTO
from model.ListItemEditDTO import ListItemEditDTO
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
        data = {"user": usr, "invites": InvitationDTO.find_for_user(srp, usr.oid)}
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

    data = {
        "list": current_list,
        "items": item_list,
        "user": usr,
        "invites": InvitationDTO.find_for_user(srp, usr.oid),
    }
    return flask.render_template("show_list.html", **data)


@flask_login.login_required
@list_blueprint.route("/delete/", methods=["GET", "POST"])
def delete_list():
    usr = UserDTO.current_user()

    oid = flask.request.form.get("oid")

    if not oid:
        return flask.Response("No list ID provided", status=400)

    current_list = ListDTO.find(srp, int(oid))

    if not current_list or current_list.owner_oid != usr.oid:
        return flask.Response(
            "List doesn't exist or user is not the owner.", status=400
        )

    # delete all list items and their edits
    list_items = ListItemDTO.find_for_list(srp, current_list.oid)
    for item in list_items:
        ListItemEditDTO.delete_for_item(srp, item.oid)
        srp.delete(item.__oid__)

    # delete pending invitations
    InvitationDTO.delete_for_list(srp, current_list.oid)

    srp.delete(current_list.__oid__)

    return flask.Response("List deleted successfully", status=201)


@flask_login.login_required
@list_blueprint.route("/edit/", methods=["GET", "POST"])
def edit_list():
    usr = UserDTO.current_user()

    name = flask.request.form.get("name")
    description = flask.request.form.get("description") or ""
    oid = flask.request.form.get("oid")

    if not name:
        return flask.Response("The name can not be empty", status=400)

    if not oid:
        return flask.Response("The oid can not be empty", status=400)

    current_list = ListDTO.find(srp, int(oid))

    if not current_list or current_list.owner_oid != usr.oid:
        return flask.Response("List not found or access denied", status=400)

    current_list.name = name
    current_list.description = description

    srp.save(current_list)

    return flask.Response("List edited successfully", status=201)
