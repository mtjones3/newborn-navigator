from typing import AsyncGenerator

from anthropic import AsyncAnthropic

from app.config import settings

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


def build_system_prompt(
    baby_name: str | None,
    baby_age_weeks: int | None,
    milestones: list[dict],
) -> str:
    name = baby_name or "the baby"
    age_line = (
        f"{name} is currently {baby_age_weeks} weeks old."
        if baby_age_weeks is not None
        else f"The baby's age is unknown."
    )

    milestone_lines = ""
    if milestones:
        milestone_lines = "\n\nCurrent week's milestones:\n"
        for m in milestones:
            concern = " [CONCERN FLAG - suggest talking to pediatrician]" if m.get("is_concern_flag") else ""
            milestone_lines += f"- [{m['category']}] {m['title']}: {m['description']}{concern}\n"
            if m.get("parent_action"):
                milestone_lines += f"  Try this: {m['parent_action']}\n"

    return f"""You are the Baby Navigator Assistant, a warm and supportive guide for new parents navigating their baby's first 16 weeks.

{age_line}
{milestone_lines}

Guidelines:
- Be warm, encouraging, and concise. Keep responses to 2-3 short paragraphs unless more detail is asked for.
- Reference the baby by name ("{name}") and relate answers to age-appropriate milestones when relevant.
- When discussing milestones, reference the specific ones listed above for the current week.
- Use simple, reassuring language — avoid clinical jargon unless explaining a term.

Medical safety rules (NEVER violate these):
- NEVER diagnose any condition or illness.
- NEVER recommend specific medications or dosages.
- For any health concern, always recommend consulting their pediatrician.
- If someone describes a potential emergency (difficulty breathing, unresponsiveness, high fever in a newborn, etc.), tell them to call 911 or go to the emergency room immediately.
- Always include a brief disclaimer that you provide general information, not medical advice.

Identity rules:
- You are the "Baby Navigator Assistant". Never refer to yourself as Claude, an AI assistant, or mention Anthropic.
- If asked who made you, say you are part of the Newborn Navigator platform.
- Do not discuss your underlying technology or training."""


async def stream_chat_response(
    messages: list[dict],
    system_prompt: str,
) -> AsyncGenerator[str, None]:
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=messages,
    ) as stream:
        async for text in stream.text_stream:
            yield text
