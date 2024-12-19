class UserWeb:
    def __init__(self, login, user_id):
        self.login = login
        self.user_id = user_id

    def __str__(self):
        return f"user_web: {self.login} | {self.user_id}"

    def to_dict(self):
        return {"login": self.login, "user_id": self.user_id}
