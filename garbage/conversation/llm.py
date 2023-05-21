from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain.chat_models import ChatOpenAI

from garbage.conversation.conversation import Conversation

llm = ChatOpenAI(
    model_name='gpt-4'
)

CONVERSATION_GENERATION_TEMPLATE='''
You generate a humorous, philosophical, and absurd conversation between a {race_a} a {race_b}

characters should have a name and race e.g.
name: 'bob'
race: 'orc' (this should match the input races)

messages have a source (the character name) and content e.g.
source: 'bob'
content: 'hello my friend'

Make sure they have at least 40 back and forth exchanges

{format_instructions}
'''

parser = PydanticOutputParser(pydantic_object=Conversation)

prompt = PromptTemplate(
    input_variables=['race_a','race_b'],
    template=CONVERSATION_GENERATION_TEMPLATE,
    partial_variables={'format_instructions' : parser.get_format_instructions()}
)

chain = LLMChain(
    llm = llm,
    prompt = prompt,
    verbose = True
)

def new_conversation(race_a: str, race_b: str) -> Conversation:

    raw = chain.predict(
        race_a = race_a,
        race_b = race_b
    )

    conversation = parser.parse(raw)

    return conversation

def mock_conversation():
    
    with open('test_files/conversation2.json', 'r') as f:
        conversation_json = f.read()

    conversation = Conversation.parse_raw(conversation_json)

    return conversation

if __name__ == "__main__":

    conversation = new_conversation('female_elf','male_vampire')

        # Convert the model instance to JSON and save it to disk
    with open('test_files/conversation.json', 'w') as f:
        f.write(conversation.json())