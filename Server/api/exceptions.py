from fastapi import HTTPException, status
from typing import Optional


def _make_exception(status_code: status, detail: Optional[str] = None):
    return HTTPException(
        status_code=status_code,
        detail=detail
    )


# TODO: consider returning a 200 OK with an appropriate message instead
# see https://stackoverflow.com/questions/9269040/which-http-response-code-for-this-email-is-already-registered
USERNAME_UNAVAILABLE_EXCEPTION = _make_exception(status.HTTP_409_CONFLICT, 'username unavailable')


def not_found(detail: Optional[str] = None):
    return _make_exception(status.HTTP_404_NOT_FOUND, detail)


def bad_request(detail: Optional[str] = None):
    return _make_exception(status.HTTP_400_BAD_REQUEST, detail)
