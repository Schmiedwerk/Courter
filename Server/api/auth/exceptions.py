from fastapi import HTTPException, status


_AUTHENTICATE_HEADER = {'WWW-Authenticate': 'Bearer'}

INCOMPLETE_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='could not validate credentials',
    headers=_AUTHENTICATE_HEADER
)

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='incorrect username or password',
    headers=_AUTHENTICATE_HEADER
)

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='invalid access token',
    headers=_AUTHENTICATE_HEADER
)

ROLE_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='insufficient rights',
    headers=_AUTHENTICATE_HEADER
)
