import flask
import flask_login
import sirope
from flask import Response

from model.ListDTO import ListDTO
from model.ListItemDTO import ListItemDTO
from model.ListItemEditDTO import ListItemEditDTO
from model.UserDTO import UserDTO


def get_blprint():
    list_item_view = flask.blueprints.Blueprint(
        "list_item",
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
        content=content,
        checked=True if checked and checked == "on" else False,
        parent_oid=int(parent_list_oid),
    )

    if not parent_list or usr.oid not in parent_list.users_with_access:
        flask.flash("Invalid parent or access denied.")
        return flask.redirect("/home/")
    else:
        srp.save(new_item)
        edit = ListItemEditDTO(parent_oid=new_item.oid, user_oid=usr.oid, action="add")
        srp.save(edit)
        return flask.redirect("/list/" + parent_list_oid, code=301)


@flask_login.login_required
@list_item_blueprint.route("/disable/", methods=["POST"])
def disable_item():
    usr = UserDTO.current_user()
    item_oid = flask.request.form.get("oid")

    item = ListItemDTO.find(srp, int(item_oid))

    if item:
        parent_list = ListDTO.find(srp, item.parent_oid)
        if usr.oid in parent_list.users_with_access:
            edit = ListItemEditDTO(
                parent_oid=item.oid, user_oid=usr.oid, action="disable"
            )
            item.disabled = True
            srp.save(item)
            srp.save(edit)
        else:
            flask.flash("Access to item denied.")
        return flask.Response(status=201)
    else:
        flask.flash("Item not found")
        return flask.Response(status=401)


@flask_login.login_required
@list_item_blueprint.route("/check/", methods=["POST"])
def check_item():
    usr = UserDTO.current_user()
    oid = flask.request.form.get("oid")
    checked = flask.request.form.get("checked")

    current_item = ListItemDTO.find(srp, int(oid))
    if (
        current_item
        and usr.oid in ListDTO.find(srp, int(current_item.parent_oid)).users_with_access
    ):
        current_item.checked = True if checked == "true" else False
        edit = ListItemEditDTO(
            parent_oid=current_item.oid,
            user_oid=usr.oid,
            action="check" if current_item.checked else "uncheck",
        )

        srp.save(current_item)
        srp.save(edit)
        return Response(status=201)
    else:
        flask.flash("Invalid parent or access denied.")
        return flask.redirect("/home/")


@flask_login.login_required
@list_item_blueprint.route("/<item_oid>", methods=["GET"])
def show_item(item_oid):
    usr = UserDTO.current_user()

    item = ListItemDTO.find(srp, int(item_oid))

    if not item or usr.oid not in ListDTO.find(srp, item.parent_oid).users_with_access:
        flask.flash("Invalid item or access denied.")
        return flask.redirect("/home/")
    else:
        data = {
            "user": usr,
            "item": item,
            "edits_list": ListItemEditDTO.find_for_item(srp, item.oid),
        }
        return flask.render_template("show_item.html", **data)
