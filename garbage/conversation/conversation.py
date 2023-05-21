from pydantic import BaseModel

class Character(BaseModel):

    name: str
    race: str

class Message(BaseModel):

    source: str
    content: str

class Conversation(BaseModel):

    character_a: Character
    character_b: Character

    messages: list[Message]

