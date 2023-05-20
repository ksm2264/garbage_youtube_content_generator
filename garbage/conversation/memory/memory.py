from langchain.prompts import PromptTemplate

from garbage.conversation.memory.summarizer import Summarizer

class ConversationMemory:

    def __init__(self, name_a: str, name_b: str):

        self.A: str = name_a
        self.B: str = name_b

        self.history: list[str] = []

        self.summarizer: Summarizer = Summarizer(name_a, name_b)

        self.summary: str = ''

    def add(self, name: str, message: str):

        speaker_and_message = f'{name} : {message}'

        # update history and summary
        self.history.append(speaker_and_message)
        self.update_summary(speaker_and_message)
        

    def update_summary(self, speaker_and_message: str):

        self.summary = self.summarizer.update_summary(self.summary, speaker_and_message)

    def get_instructions(self, k: int=3) -> str:

        last_few_messages = self.history[-k:]

        template = '''
        This is a summary of the conversation so far:
        {summary}

        These are the last few exchanges:
        {last_few_messages}
        '''
        
        prompt = PromptTemplate(
            template = template,
            input_variables=['summary','last_few_messages']
        )

        formatted = prompt.format(
            summary = self.summary,
            last_few_messages = last_few_messages
        )

        return formatted

    