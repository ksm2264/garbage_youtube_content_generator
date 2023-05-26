from langchain.prompts import PromptTemplate

template = '''
Profile picture of a {race} named {name}.

Looking straight at the camera.
'''

prompt = PromptTemplate(
    template=template,
    input_variables=['race', 'name']
)