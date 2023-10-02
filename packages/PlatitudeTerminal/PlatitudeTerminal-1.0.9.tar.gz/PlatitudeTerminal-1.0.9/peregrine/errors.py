class PeregrineVersionOutOfDateError(Exception):
    pass

class PeregrineServerError(Exception):
    pass

class PeregrineConnectionError(Exception):
    pass

class PeregrineExpiredLoginError(Exception):
    pass

class PeregrineInsufficientTokensError(Exception):
    pass