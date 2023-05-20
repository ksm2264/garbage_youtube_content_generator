from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


template = '''
You maintain an ongoing summary of a conversation between {entity_a} and {entity_b}

Current summary:
{summary}

New message:
{new_message}
'''

llm = ChatOpenAI(model_name='gpt-4')

class Summarizer:
    
    def __init__(self, entity_a: str, entity_b: str):

        prompt = PromptTemplate(
            input_variables=['summary','new_message'],
            template=template,
            partial_variables={'entity_a':entity_a,
                               'entity_b':entity_b}
        )

        self.chain = LLMChain(
            llm = llm,
            prompt=prompt
        )

    def update_summary(self, summary: str, new_message: str):

        new_summary = self.chain.predict(
            summary = summary,
            new_message = new_message
        )

        return new_summary