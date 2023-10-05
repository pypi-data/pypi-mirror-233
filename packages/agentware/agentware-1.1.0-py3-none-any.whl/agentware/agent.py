from agentware.agent_logger import Logger
from agentware.memory import Memory
from agentware.core_engines import OpenAICoreEngine
from agentware.utils.json_fixes.parsing import fix_and_parse_json
from agentware.utils.json_validation.validate_json import validate_json

import openai
import json
import copy
from functools import reduce
import traceback
import agentware
import pystache


logger = Logger()


class PromptProcessor:
    def __init__(self, conversation_setup: str, template: str, output_schema=None) -> None:
        self._template = template
        self._conversation_setup = conversation_setup
        self._output_schema = output_schema

    @classmethod
    def from_config(cls, cfg: dict):
        return cls(cfg["conversation_setup"], cfg["template"], cfg["output_schema"])

    def get_conversation_setup(self):
        return self._conversation_setup

    def get_template(self):
        return self._template

    def to_config(self):
        return {
            "conversation_setup": self._conversation_setup,
            "template": self._template,
            "output_schema": self._output_schema
        }

    def format(self, *args, **kwargs):
        if not self._template:
            if not len(args) == 1:
                raise ValueError(
                    "One and only one arg is required to format for empty template")
            return args[0]
        return pystache.render(self._template, kwargs)

    def parse_output(self, raw_output):
        if self._output_schema:
            logger.debug(f'parsing {raw_output}')
            parsed_output = fix_and_parse_json(raw_output)
            validated_output = validate_json(
                parsed_output, self._output_schema)
            return validated_output["output"]
        else:
            return raw_output

class Agent():
    DEFAULT_MAX_RETRIES = 3
    def __init__(self, prompt_processor=None, core_engine=None):
        self._memory = Memory(self)
        if not core_engine:
            core_engine = OpenAICoreEngine()
        if not prompt_processor:
            prompt_processor = PromptProcessor("", "", "")
        self._core_engine = core_engine
        self._prompt_processor = prompt_processor
        self._max_num_retries = self.DEFAULT_MAX_RETRIES
        self._conversation_setup = prompt_processor.get_conversation_setup()

    def get_conversation_setup(self):
        return self._conversation_setup

    def set_num_max_retries(self, num_retries):
        self._max_num_retries = num_retries
 
    def run(self, *args, **kwargs):
        output_valid = False
        num_retries = 0
        raw_output = ""
        prompt = self._prompt_processor.format(*args, **kwargs)
        self._memory.add_memory({
            "role": "user",
            "content": prompt
        })
        memory_with_error = copy.deepcopy(self._memory)
        while True:
            if num_retries > 0:
                logger.debug(f"Retrying for the {num_retries} time")
            try:
                messages = memory_with_error.to_messages()
                raw_output = self._core_engine.chat(messages)
                try:
                    output = self._prompt_processor.parse_output(raw_output)
                    self._memory.add_memory({
                        "role": "assistant",
                        "content": output
                    })
                    output_valid = True
                    return output
                except Exception as err:
                    logger.warning(f"Error parsing with exception {err}")

                    traceback.print_exc()
                    if num_retries >= 1:
                        # Delete the previous wrong output, and the prompt
                        memory_with_error.delete_memory(-1)
                        memory_with_error.delete_memory(-1)
                    # Add the current wrong output, and requests to correct
                    memory_with_error.add_memory({
                        "role": "assistant",
                        "content": raw_output
                    })
                    memory_with_error.add_memory({
                        "role": "user",
                        "content": "Failed to parse output. Your content is great, regenerate with the same content in a format that aligns with the requirements and example schema."
                    })
            except Exception as e:
                logger.warning(f"Error getting agent output with error {e}")
            if output_valid or num_retries >= self._max_num_retries:
                break
            num_retries += 1

    def clear_memory(self):
        self._memory.clear()

        