from pydantic import BaseModel


class Answer(BaseModel):
    task: str
    audio: str
    user: str
    questionOffsets: list[float]
    content: str | None
