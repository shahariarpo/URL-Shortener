from pydantic import BaseModel

class UrlBody(BaseModel):
    url: str