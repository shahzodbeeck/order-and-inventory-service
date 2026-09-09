class AuthUser:
    def __init__(self, id, email):
        self.id = id
        self.pk = id
        self.email = email
        self.is_authenticated = True
        self.is_anonymous = False
