import json

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from garbage.conversation.models import Character
from garbage.conversation.random_character import new_character


template = '''
You are roleplaying as this character:
{character}.

{instructions}

Respond to the ongoing discussion in a way that this character would.
Even though this is fantasy-esque, give the character a non fiction and mundane
kind of topic / way of speaking about thigns.
Base your response on their description.
Keep it short.

Use spoken words, no *laughs* or *winks* or things like that.

{name}:
'''

llm = ChatOpenAI(
     model_name = 'gpt-4'
)

class CharacterLLM:

    def __init__(self, character: Character):

        self.character: Character = character

        prompt = PromptTemplate(
            template=template,
            input_variables=['instructions', 'name'],
            partial_variables={'character': json.dumps(character.dict())}
        )

        self.chain = LLMChain(
             prompt = prompt,
             llm = llm,
             verbose = True
        )


    def respond(self, instructions: str) -> str:
        
        response = self.chain.predict(
             instructions = instructions,
             name = self.character.name
        )

        return response


if __name__ == '__main__':

    
      character = new_character()

      prompt = PromptTemplate(
            template=template,
            input_variables=['instructions','name'],
            partial_variables={'character': json.dumps(character.dict())}
        )
      
      print(prompt.format(
           instructions='foo'
      ))