from pydantic import BaseModel


class Artist(BaseModel):
    external_urls: dict[str, str]
    href: str
    id: str
    name: str
    type: str
    uri: str
