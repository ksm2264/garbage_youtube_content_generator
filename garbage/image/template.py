from langchain.prompts import PromptTemplate

template = '''
Headshot with upper body of a {race} {occupation}.

Human-like face. 
'''

prompt = PromptTemplate(
    template=template,
    input_variables=['race','occupation']
)