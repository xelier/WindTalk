class User(object):
    def __init__(self, user):
        self._id = user['ID']
        self._userName = user['USER_NAME']
        self._password = user['PASSWORD']
        self._nickname = user['NICKNAME']
        self._role = user['ROLE']
        self._email = user['EMAIL']

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @property
    def username(self):
        return self._userName

    @username.setter
    def username(self, new_username):
        self._userName = new_username

    @property
    def password(self):
        return self._id

    @password.setter
    def password(self, new_password):
        self._password = new_password

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, new_nickname):
        self._nickname = new_nickname

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, new_role):
        self._role = new_role

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        self._email = new_email
