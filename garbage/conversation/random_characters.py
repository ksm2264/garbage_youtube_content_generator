from dotenv import load_dotenv
load_dotenv()

from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from garbage.conversation.models import Characters

llm = ChatOpenAI(model_name = 'gpt-4')

template = '''
You generate two random characters ({optional_steering})

{format_instructions}
'''

parser = PydanticOutputParser(pydantic_object=Characters)

prompt = PromptTemplate(
    input_variables=['optional_steering'],
    template=template,
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

fixer = OutputFixingParser.from_llm(
    llm = llm,
    parser = parser
)

chain = LLMChain(
    llm = llm,
    prompt = prompt,
    verbose=True
)

def new_characters(optional_steering = ''):
    raw = chain.predict(optional_steering = optional_steering)

    characters = fixer.parse(raw)

    return characters.character_a, characters.character_b

if __name__ == '__main__':
  
    characters = new_characters()

    print(characters)