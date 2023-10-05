import openai
import agentware

from langchain.chains import LLMChain
from langchain.agents.agent import AgentExecutor
from typing import Union, Dict, List

OPENAI = "OPENAI"

class CoreEngineBase():
    def run(self, messages: List[Dict[str, str]]):
        raise BaseException("Not implemented")


class OpenAICoreEngine(CoreEngineBase):
    DEFAULT_MODEL="gpt-3.5-turbo"
    def __init__(self, model=None):
        super().__init__()
        if (not agentware.openai_api_key) and (not openai.api_key):
            raise ValueError("You must first set openai api key with agentware.openai_api_key = <Your api key>")
        elif agentware.openai_api_key:
            openai.api_key = agentware.openai_api_key
        if not model:
            model=self.DEFAULT_MODEL
        self._model = model
    def set_model(self, model):
        self._model = model
    def chat(self, messages: List[Dict[str, str]]):
        completion = openai.ChatCompletion.create(
            model=self._model, messages=messages)
        return completion.choices[0].message.content


class LangchainCoreEngine(CoreEngineBase):
    def __init__(self, chain: Union[LLMChain, AgentExecutor]):
        super().__init__()
        self._chain = chain

    def run(self, messages: List[Dict[str, str]]):
        return self._chain.run(messages)
