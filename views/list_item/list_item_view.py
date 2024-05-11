import flask
import flask_login
import sirope

from model.ListDTO import ListDTO
from model.ListItemDTO import ListItemDTO
from model.UserDTO import UserDTO


def get_blprint():
    list_item_view = flask.blueprints.Blueprint(
        "listt",
        __name__,
        url_prefix="/list_item",
        template_folder="templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return list_item_view, syrp


list_item_blueprint, srp = get_blprint()


@flask_login.login_required
@list_item_blueprint.route("/add/", methods=["POST"])
def create_item():
    usr = UserDTO.current_user()
    content = flask.request.form.get("content")
    checked = flask.request.form.get("checked")
    parent_list_oid = flask.request.form.get("parent_list")

    if not content:
        flask.flash("The item may not be empty.")
        return flask.redirect("/list/" + parent_list_oid, code=400)

    parent_list = ListDTO.find(srp, int(parent_list_oid))

    new_item = ListItemDTO(
        content=content, checked=checked, parent_oid=int(parent_list_oid)
    )

    if not parent_list or usr.oid not in parent_list.users_with_access:
        flask.flash("Invalid parent or access denied.")
        return flask.redirect("/home/")
    else:
        srp.save(new_item)
        return flask.redirect("/list/" + parent_list_oid, code=201)
