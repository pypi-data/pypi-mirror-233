import openai
from openai import Completion

class GPTWrapper:

    def __init__(self):
        self.model = "gpt-3.5-turbo-instruct"
        openai.api_key = "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"

    def complete(self, prompt
                 ):
        return Completion.create(
            model=self.model,
            prompt=prompt,
            stop = ["."]
        )