import pytest
from requests import Session

from requests_rest_api import delete_request, get_request, patch_request, post_request, put_request


# ------------------------------------------------------------------------
# Tests for get_request()
# ------------------------------------------------------------------------
@pytest.mark.parametrize(
    "url, params",
    [
        ("https://reqres.in/api/users?page=2", None),
        ("https://reqres.in/api/users", {"page": 2}),
    ],
)
def test_get_request(url, params):
    with Session() as session:
        result = get_request(url, session=session, params=params)
    assert result


# ------------------------------------------------------------------------
def test_get_request_without_session():
    result = get_request("https://reqres.in/api/users/2", status_codes=[200])
    assert result


# ------------------------------------------------------------------------
# Tests for post_request()
# ------------------------------------------------------------------------
def test_post_request():
    data = {"email": "eve.holt@reqres.in", "password": "pistol"}
    result = post_request("https://reqres.in/api/register", data=data)
    assert result


# ------------------------------------------------------------------------
# Tests for put_request()
# ------------------------------------------------------------------------
def test_put_request():
    data = {"name": "morpheus", "job": "zion resident"}
    result = put_request("https://reqres.in/api/users/2", data=data)
    assert result


# ------------------------------------------------------------------------
# Tests for patch_request()
# ------------------------------------------------------------------------
def test_patch_request():
    data = {"name": "morpheus", "job": "zion resident"}
    result = patch_request("https://reqres.in/api/users/2", data=data)
    assert result


# ------------------------------------------------------------------------
# Tests for delete_request()
# ------------------------------------------------------------------------
def test_delete_request():
    result = delete_request("https://reqres.in/api/users/2")
    assert result
