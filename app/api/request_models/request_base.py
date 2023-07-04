from pydantic import BaseModel, Extra


class RequestBaseModel(BaseModel):
    """
    Base class for requests bodies.

    Forbidden extra fields.
    """

    class Config:
        extra = Extra.forbid
