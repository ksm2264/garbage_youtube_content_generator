from dotenv import load_dotenv
load_dotenv()

from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

from garbage.conversation.models import Character

llm = ChatOpenAI(model_name = 'gpt-3.5-turbo')

template = '''
You generate random characters

{format_instructions}
'''

parser = PydanticOutputParser(pydantic_object=Character)

prompt = PromptTemplate(
    input_variables=[],
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

def new_character():
    raw = chain.predict()

    character = fixer.parse(raw)

    return character

if __name__ == '__main__':
  
    character = new_character()

    print(character)