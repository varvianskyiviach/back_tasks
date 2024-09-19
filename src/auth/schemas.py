from pydantic import BaseModel


# JSON payload containing access token
class TokenSchema(BaseModel):
    access_token: str
    type_token: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None
