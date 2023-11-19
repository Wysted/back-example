from app.dependencies import pydantic


class TokenData(pydantic.BaseModel):
    id: str
    sub: str


class TokenRes(pydantic.BaseModel):
    token: str
    user: dict
