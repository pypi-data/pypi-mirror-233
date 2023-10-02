from enum import Enum
from http import HTTPStatus
from typing import Optional


# supported request methods
class RequestMethod(str, Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


# expected http status codes per method type
STATUS_CODES_PER_REQUEST_METHOD = {
    RequestMethod.GET: [HTTPStatus.OK],
    RequestMethod.HEAD: [HTTPStatus.OK],
    RequestMethod.POST: [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT],
    RequestMethod.PUT: [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT],
    RequestMethod.DELETE: [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT],
    RequestMethod.PATCH: [HTTPStatus.OK, HTTPStatus.NO_CONTENT],
}


def expected_status_codes(
    method: RequestMethod,
    status_codes: Optional[list] = None,
):
    return STATUS_CODES_PER_REQUEST_METHOD[method] if status_codes is None else status_codes
