from ninja import Schema


class TriviaCategorySchema(Schema):
    uid: str
    name: str
    description: str
