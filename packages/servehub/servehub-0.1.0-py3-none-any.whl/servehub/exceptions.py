class ServeHubException(Exception):
    pass


class ServeHubError(ServeHubException):
    """Raised when an error originates from ServeHub."""


class ApiNotFoundError(ServeHubException):
    """Raised when trying to run an API that does not exist, or that the user doesn't have access to."""


class ApiNotDeployedError(ServeHubException):
    """Raised when trying to run an API that is not deployed."""


class ApiError(ServeHubException):
    """An error from the deployed API's code."""