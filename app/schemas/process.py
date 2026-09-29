from pydantic import BaseModel, Field


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ProcessResponse(BaseModel):
    result: str
