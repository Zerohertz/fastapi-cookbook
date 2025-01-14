from pydantic import BaseModel


class Shields(BaseModel):
    schemaVersion: int
    label: str
    message: str
    color: str
    labelColor: str
    namedLogo: str
    style: str
