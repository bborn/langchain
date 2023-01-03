# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

_DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and {ai_prefix}. The {ai_prefix} is talkative and provides lots of specific details from its context. If {ai_prefix} does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
{ai_prefix}:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input", "ai_prefix"], template=_DEFAULT_TEMPLATE
)

_DEFAULT_SUMMARIZER_TEMPLATE = """Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary.

EXAMPLE
Current summary:
The human asks what {ai_prefix} thinks of artificial intelligence. {ai_prefix} thinks artificial intelligence is a force for good.

New lines of conversation:
Human: Why do you think artificial intelligence is a force for good?
{ai_prefix}: Because artificial intelligence will help humans reach their full potential.

New summary:
The human asks what {ai_prefix} thinks of artificial intelligence. {ai_prefix} thinks artificial intelligence is a force for good because it will help humans reach their full potential.
END OF EXAMPLE

Current summary:
{summary}

New lines of conversation:
{new_lines}

New summary:"""
SUMMARY_PROMPT = PromptTemplate(
    input_variables=["summary", "new_lines", "ai_prefix"], template=_DEFAULT_SUMMARIZER_TEMPLATE
)
