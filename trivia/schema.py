from ninja import Schema
from uuid import UUID

from user.schema import UserOutSchema


class TriviaCategoryOutSchema(Schema):
    uid: UUID
    name: str
    description: str

class TriviaCategoryInSchema(Schema):
    name: str
    description: str


class AllTriviaSchema(Schema):
    uid: UUID
    category: TriviaCategoryOutSchema
    question: str
    option_1: str
    option_2: str
    option_3: str
    correct_option: str


class TriviaLogOutSchema(Schema):
    session_id: UUID
    user: UserOutSchema
    total_correct_answers: int
    total_wrong_answers: int
    total_time_spent_in_seconds: int
    trivia_category: TriviaCategoryOutSchema
