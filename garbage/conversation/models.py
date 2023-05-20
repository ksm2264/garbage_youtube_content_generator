from pydantic import BaseModel
from typing import Optional, List

class Character(BaseModel):
    name: str
    race: str
    occupation: str
    emotional_state: str
    obssessed_with: list[str]
    has_distate_for: list[str]


    @staticmethod
    def mocks():
        character1 = Character(
            name="Gandalf",
            race="Maia",
            age=2019,
            occupation="Wizard",
            speaking_style="Formal and archaic",
            backstory="A Maia spirit sent by the Valar to assist the peoples of Middle-earth in their struggle against Sauron.",
            secret_goals=["Defeat Sauron", "Unite the peoples of Middle-earth"],
            personality_disorders=[],
            insecurities=["Fear of losing to Sauron", "Fear of corruption by the One Ring"]
        )

        character2 = Character(
            name="Harry Potter",
            race="Wizard",
            age=11,
            occupation="Student",
            speaking_style="Informal",
            backstory="The Boy Who Lived, who survived a killing curse as an infant",
            secret_goals=["Defeat Voldemort", "Protect his friends"],
            personality_disorders=[],
            insecurities=["Fear of being an inadequate wizard", "Fear of losing loved ones"]
        )

        return character1, character2

class Characters(BaseModel):

    character_a: Character
    character_b: Character


class VoiceName(BaseModel):
    name: str