from dotenv import load_dotenv
load_dotenv()

from garbage.conversation.models import Character
from garbage.conversation.memory.memory import ConversationMemory
from garbage.conversation.character.character import CharacterLLM
from garbage.conversation.random_character import new_character


class ConversationGenerator:

    def __init__(self, character_a: Character, character_b: Character):

        self.A = CharacterLLM(character_a)
        self.B = CharacterLLM(character_b)

        self.active = self.A

        self.memory = ConversationMemory(character_a.name, character_b.name)

    def next(self):
        
        instructions = self.memory.get_instructions()

        response = self.active.respond(
            instructions = instructions
        )

        name = self.active.character.name

        self.memory.add(self.active.character.name, response)

        self.swap()

        return response, name

    def swap(self):

        if self.active == self.A:
            self.active = self.B
        else:
            self.active = self.A

if __name__ == '__main__':

    character_a = new_character()
    character_b = new_character()

    generator = ConversationGenerator(character_a, character_b)

    for idx in range(5):

        message, name = generator.next()

        print(f'{name} : {message}')
