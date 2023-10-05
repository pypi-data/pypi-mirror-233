from typing import Dict, List, Tuple
from agentware.agent_logger import Logger

import copy
import time
import json
import os

logger = Logger()

class MemoryUnit:
    def __init__(self, role, content) -> None:
        assert role == "user" or role == "system" or role == "assistant"
        self.role = role
        self.content = content

    @classmethod
    def from_json(cls, data: Dict[str, str]):
        return cls(data["role"], data["content"])

    def to_json(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content
        }

    def __repr__(self) -> str:
        return f"<{self.role}>: {self.content}[{self.num_tokens} tokens]"

    def __str__(self) -> str:
        return f"<{self.role}>: {self.content}[{self.num_tokens} tokens]"

class Memory():
    def __init__(self, agent):
        self._memory = []
        self._agent = agent

    def add_memory(self, memory: Dict[str, str]):
        new_memory = MemoryUnit(memory["role"], memory["content"])
        self._memory.append(new_memory)

    def delete_memory(self, memory_index: int):
        if memory_index >= len(self._memory):
            logger.debug(
                f"Deleting index {memory_index} out of range of 0-{len(self._memory)-1}")
            return
        if memory_index < 0:
            if memory_index + len(self._memory) - 1 < 0:
                logger.debug(
                    f"Deleting index {memory_index} out of range of 0-{len(self._memory)-1}")
                return
        del self._memory[memory_index]

    def to_messages(self):
        messages = []
        conversation_setup = self._agent.get_conversation_setup()
        print("conversation setup is", conversation_setup)
        if conversation_setup:
            messages.append({
                "role": "system",
                "content": conversation_setup
            })
        messages += [
            {
                "role": memory_unit.role,
                "content": memory_unit.content
            }
            for memory_unit in self._memory
        ]
        return messages