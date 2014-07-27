ROLE_USER = 0
ROLE_ADMIN = 1


class User:
    def __init__(self, user_id, password):
        self.id = user_id
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_password(self):
        return unicode(self.password)