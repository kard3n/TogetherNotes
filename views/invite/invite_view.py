import flask
import flask_login
import sirope
from flask import Response

from model.InviteDTO import InviteDTO
from model.ListDTO import ListDTO
from model.UserDTO import UserDTO


def get_blprint():
    invite_view = flask.blueprints.Blueprint(
        "invite",
        __name__,
        url_prefix="/invite",
        template_folder="templates",
        static_folder="static",
    )
    syrp = sirope.Sirope()
    return invite_view, syrp


invite_blueprint, srp = get_blprint()


@flask_login.login_required
@invite_blueprint.route("/create", methods=["POST"])
def create_invite():
    usr = UserDTO.current_user()

    invitee_name = flask.request.form.get("invitee_name")
    message = flask.request.form.get("message")

    current_list_id = flask.request.form.get("list_oid")
    current_list = ListDTO.find(srp, int(current_list_id))

    if not current_list or usr.oid != current_list.owner_oid:
        flask.flash("List does not exist or you are not its owner.")
        return flask.redirect("/home")

    invitee: UserDTO = UserDTO.find_by_name(srp, invitee_name)

    if (
        not invitee
        or invitee.oid in current_list.users_with_access
        or InviteDTO.find_by_invitee_list(srp, invitee.oid, current_list.oid)
    ):
        if not invitee:
            flask.flash("Invitee not found.")
        elif invitee.oid in current_list.users_with_access:
            flask.flash("Invite already sent.")
        else:
            flask.flash("User already invited.")

        data = {
            "user": usr,
            "list": current_list,
            "invitee_name": invitee_name,
            "message": f'Come join my to-do list "{current_list.name}"',
            "invites": InviteDTO.find_for_user(srp, usr.oid),
        }
        return flask.render_template("create_invite.html", **data)

    new_invite = InviteDTO(
        inviter_oid=usr.oid,
        invitee_oid=invitee.oid,
        message=(
            message if message else f'Come join my to-do list, "{current_list.name}"'
        ),
        list_oid=current_list.oid,
    )

    srp.save(new_invite)
    flask.flash(f"Invite created for {invitee.name}")
    return flask.redirect(f"/list/{current_list.oid}", code=301)


@flask_login.login_required
@invite_blueprint.route("/new/<list_id>", methods=["GET"])
def get_invite_page(list_id):
    usr = UserDTO.current_user()
    current_list = ListDTO.find(srp, int(list_id))

    if current_list is None or usr is None or usr.oid != current_list.owner_oid:
        flask.flash("List does not exist or you are not its owner.")
        return flask.redirect("/home")

    data = {
        "user": usr,
        "list": current_list,
        "invitee_name": "",
        "message": f'Come join my to-do list, "{current_list.name}"',
        "invites": InviteDTO.find_for_user(srp, usr.oid),
    }
    return flask.render_template("create_invite.html", **data)


@flask_login.login_required
@invite_blueprint.route("/reject", methods=["POST"])
def reject_invite():
    usr = UserDTO.current_user()

    invite_oid = flask.request.form.get("oid")
    invite = InviteDTO.find(srp, int(invite_oid))

    if invite and invite.invitee_oid == usr.oid:
        srp.delete(invite.__oid__)
        return Response(status=201)
    else:
        return Response(status=400)


@flask_login.login_required
@invite_blueprint.route("/accept", methods=["POST"])
def accept_invite():
    usr = UserDTO.current_user()

    invite_oid = flask.request.form.get("oid")
    invite = InviteDTO.find(srp, int(invite_oid))

    if invite and invite.invitee_oid == usr.oid:
        current_list = ListDTO.find(srp, invite.list_oid)
        current_list.add_user_by_oid(usr.oid)
        print(current_list.__dict__)
        srp.save(current_list)
        srp.delete(invite.__oid__)
        return Response(status=201)
    else:
        return Response(status=400)
