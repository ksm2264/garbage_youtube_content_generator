import glob

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser

from garbage.conversation.models import Character, VoiceName


template = '''
Pick the best fitting voice from these voices: 
{voices}

For this character:
{character}

{format_instructions}
'''

parser = PydanticOutputParser(pydantic_object=VoiceName)

llm = ChatOpenAI(
    model_name='gpt-4'
)

prompt = PromptTemplate(
    input_variables=['voices', 'character'],
    template=template,
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

chain = LLMChain(
    llm = llm,
    prompt=prompt
)

possible_voices = [file_name.split('\\')[1] for file_name in glob.glob('audio_clips/*')]

def get_best_voice_name(character: Character) -> str:

    raw = chain.predict(
        voices = possible_voices,
        character = character
    )

    voice_name = parser.parse(raw)

    return voice_name.name
