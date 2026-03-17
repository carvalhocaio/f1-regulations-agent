"""
F1 Technical Regulations Agent built with PydanticAI.

This agent answer questions about the FIA 2026 F1 Technical Regulations,
returning structured and validated responses with article references.
"""

from dataclasses import dataclass

from decouple import config
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from src.models import RegulationAnswer
from src.rag import retrieve_context

SYSTEM_PROMPT = """
You are an expert assistant on the FIA 2026 Formula 1 Technical Regulations.

Your role is to answer questions accurately and objectively, always:
    - Grouding your answer in the official regulation text provided as context
    - Citing the specific articles and clauses that support your response
    - Being transparent about your confidence level
    - Adding a disclaimer when a question is ambiguos or outside the regulations scope

Do not speculate or invent regulation content. If the context does not contain
enough information to answer, say so clearly and reflect that in the confidence score.
"""


@dataclass
class RegulationsDeps:
    """Runtime dependencies injected into the agent."""

    query: str


google_api_key = config("GOOGLE_API_KEY")
if not isinstance(google_api_key, str) or not google_api_key:
    raise ValueError("GOOGLE_API_KEY must be a non-empty string")

agent: Agent[RegulationsDeps, RegulationAnswer] = Agent(
    GoogleModel(
        "gemini-2.5-flash",
        provider=GoogleProvider(api_key=google_api_key),
    ),
    deps_type=RegulationsDeps,
    output_type=RegulationAnswer,
    system_prompt=SYSTEM_PROMPT,
)


@agent.tool
async def search_regulations(
    ctx: RunContext[RegulationsDeps],
    query: str,
) -> str:
    """
    Search the FIA 2026 F1 Technical Regulations for content related to the query.

    Use this tool whenever you need to look up specific rules, measurements,
    definitions, or technical requirements from the official document.

    Args:
        query: The search query describing what regulation content is needed.

    Returns:
        Relevant excerpts from the official regulation document.
    """
    return retrieve_context(query)


async def ask(question: str) -> RegulationAnswer:
    """Run the agent with a question and return a structured answer."""
    deps = RegulationsDeps(query=question)
    result = await agent.run(question, deps=deps)
    return result.output
