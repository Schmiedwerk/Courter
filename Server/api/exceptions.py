from fastapi import HTTPException, status
from typing import Optional


def not_found(detail: Optional[str] = None) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, detail)


def bad_request(detail: Optional[str] = None) -> HTTPException:
    return HTTPException(status.HTTP_400_BAD_REQUEST, detail)


def conflict(detail: Optional[str] = None) -> HTTPException:
    return HTTPException(status.HTTP_409_CONFLICT, detail)


# TODO: consider returning a 200 OK with an appropriate message instead
# see https://stackoverflow.com/questions/9269040/which-http-response-code-for-this-email-is-already-registered
USERNAME_UNAVAILABLE_EXCEPTION = conflict('username unavailable')

ACCESS_DENIED_EXCEPTION = HTTPException(status.HTTP_403_FORBIDDEN, 'access to the requested resource denied')
