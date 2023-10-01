class AuthError(BaseException):
    def __init__(self, message):
        self.message = message

    def text(self):
        return self.message


class TTTorrent(BaseException):
    def __init__(self, message):
        self.message = message

    def text(self):
        return self.message
