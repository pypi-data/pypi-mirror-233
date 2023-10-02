from requests.auth import HTTPBasicAuth, HTTPDigestAuth


def basic_auth(username: str, password: str) -> HTTPBasicAuth:
    """
    Creates a ``HTTPBasicAuth`` object to provide the ``.RequestsAPI`` object for authentication.

    :param username: The username to authenticate as.
    :param password: The password of the user to authenticate with.
    :return: ``HTTPBasicAuth`` object.
    """
    return HTTPBasicAuth(username, password)


def digest_auth(username: str, password: str) -> HTTPDigestAuth:
    """
    Creates a ``HTTPDigestAuth`` object to provide the ``.RequestsAPI`` object for authentication.

    :param username: The username to authenticate as.
    :param password: The password of the user to authenticate with.
    :return: ``HTTPDigestAuth`` object.
    """
    return HTTPDigestAuth(username, password)
