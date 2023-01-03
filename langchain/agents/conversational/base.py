"""An agent designed to hold a conversation in addition to using tools."""
from __future__ import annotations

import re
from typing import Any, List, Optional, Tuple

from langchain.agents.agent import Agent
from langchain.agents.conversational.prompt import FORMAT_INSTRUCTIONS, PREFIX, SUFFIX
from langchain.agents.tools import Tool
from langchain.prompts import PromptTemplate


class ConversationalAgent(Agent):
    """An agent designed to hold a conversation in addition to using tools."""
    own_name: str = "AI"

    @property
    def observation_prefix(self) -> str:
        """Prefix to append the observation with."""
        return "Observation: "

    @property
    def llm_prefix(self) -> str:
        """Prefix to append the llm call with."""
        return "Thought:"

    @classmethod
    def create_prompt(
        cls,
        tools: List[Tool],
        prefix: str = PREFIX,
        suffix: str = SUFFIX,
        input_variables: Optional[List[str]] = None,
        **kwargs: Any
    ) -> PromptTemplate:
        """Create prompt in the style of the zero shot agent.

        Args:
            tools: List of tools the agent will have access to, used to format the
                prompt.
            prefix: String to put before the list of tools.
            suffix: String to put after the list of tools.
            input_variables: List of input variables the final prompt will expect.

        Returns:
            A PromptTemplate with the template assembled from the pieces here.
        """
        tool_strings = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])
        tool_names = ", ".join([tool.name for tool in tools])

        own_name = kwargs.get("own_name", "AI")

        format_instructions = FORMAT_INSTRUCTIONS.format(
            tool_names=tool_names, own_name=own_name)

        prefix = prefix.format(own_name=own_name)

        suffix = suffix.format(own_name=own_name)

        template = "\n\n".join([prefix, tool_strings, format_instructions, suffix])
        if input_variables is None:
            input_variables = ["input", "chat_history", "agent_scratchpad"]
        return PromptTemplate(template=template, input_variables=input_variables)

    @property
    def finish_tool_name(self) -> str:
        """Name of the tool to use to finish the chain."""
        return self.own_name

    def _extract_tool_and_input(self, llm_output: str) -> Optional[Tuple[str, str]]:
        finish_prefix = f"{self.finish_tool_name}: "
        if finish_prefix in llm_output:
            return self.finish_tool_name, llm_output.split(finish_prefix)[-1]
        regex = r"Action: (.*?)\nAction Input: (.*)"
        match = re.search(regex, llm_output)

        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1)
        action_input = match.group(2)
        return action, action_input.strip(" ").strip('"')
