import flask_login
import sirope
import werkzeug.security as safe


class UserDTO(flask_login.UserMixin):
    def __init__(self, email, password, name):
        self._email = email
        self._password = safe.generate_password_hash(password)
        self._name = name

    @staticmethod
    def current_user() -> "UserDTO":
        usr = flask_login.current_user
        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        return usr

    @property
    def oid(self):
        return self.__oid__.num

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self):
        return self._email

    def get_id(self):
        return self.email

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    @staticmethod
    def find(sirope: sirope.Sirope, email: str) -> "UserDTO":
        return sirope.find_first(UserDTO, lambda u: u.email == email)
