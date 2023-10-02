# SPDX-FileCopyrightText: 2023-present herbert <dataengineer42@gmail.com>
#
# SPDX-License-Identifier: MIT

from requests_rest_api.auth import basic_auth, digest_auth
from requests_rest_api.errors import RequestError
from requests_rest_api.rest_api import get_request, post_request, put_request, patch_request, delete_request

__all__ = [
    "get_request",
    "post_request",
    "put_request",
    "patch_request",
    "delete_request",
    "basic_auth",
    "digest_auth",
    "RequestError",
]
