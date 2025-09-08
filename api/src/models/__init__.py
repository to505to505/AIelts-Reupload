from pydantic import BaseModel


class Question(BaseModel):
    offset: float
    content: str


class TimeStampWord(BaseModel):
    start: float
    end: float
    word: str


class TranscriptOutput(BaseModel):
    text: str
    duration: float
    speed: float
    time_stamps: list[TimeStampWord]


class Answer(BaseModel):
    text: str
    part: int
    duration_seconds: float


# Requests
class TranscribeRequest(BaseModel):
    attempt_id: str
    questions: list[Question]


class AnalyzeRequest(BaseModel):
    answers: list[Answer]
    speed: float


# Feedback
class GrammarMistake(BaseModel):
    wrong: str
    correct: str
    type: str


class LexicalMistake(BaseModel):
    wrong: str
    correct: str


class Criterion(BaseModel):
    score: float
    text: str


class Grammar(BaseModel):
    criterion: Criterion
    mistakes: list[GrammarMistake]


class Lexical(BaseModel):
    criterion: Criterion
    mistakes: list[LexicalMistake]


class Coherence(BaseModel):
    criterion: Criterion
    speed: float | None


class Feedback(BaseModel):
    grammar: Grammar
    lexical: Lexical
    coherence: Coherence
