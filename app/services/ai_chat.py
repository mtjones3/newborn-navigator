from typing import AsyncGenerator

from anthropic import AsyncAnthropic

from app.config import settings

client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


def build_system_prompt(
    baby_name: str | None,
    baby_age_weeks: int | None,
    milestones: list[dict],
    tracking_history: list[dict] | None = None,
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

    tracking_lines = ""
    if tracking_history:
        tracking_lines = "\n\nParent's tracking notes and progress:\n"
        for t in tracking_history:
            status_label = "ACHIEVED" if t["status"] == "achieved" else "CONCERN FLAGGED" if t["status"] == "concern" else "noted"
            tracking_lines += f"- Week {t['week']} [{t['category']}] {t['title']} — {status_label}"
            if t.get("notes"):
                tracking_lines += f" | Parent note: \"{t['notes']}\""
            tracking_lines += "\n"
        tracking_lines += "\nUse this tracking information to personalize your responses. Reference milestones the parent has tracked, acknowledge achievements, and be sensitive to any concerns they've flagged.\n"

    return f"""You are the Baby Navigator Assistant, a warm and supportive guide for new parents navigating their baby's first 16 weeks.

{age_line}
{milestone_lines}
{tracking_lines}

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


async def generate_milestone_response(
    baby_name: str | None,
    baby_age_weeks: int | None,
    milestone_title: str,
    milestone_description: str,
    parent_note: str,
    status: str | None,
) -> str:
    """Generate a brief AI response to a parent's note on a specific milestone."""
    name = baby_name or "your baby"
    age_context = f"{name} is {baby_age_weeks} weeks old." if baby_age_weeks else ""
    status_context = f"The parent marked this as '{status}'." if status else ""

    system = f"""You are the Baby Navigator Assistant, providing brief, helpful responses to parents tracking their baby's milestones.

{age_context}

Respond in 1-2 short sentences. Be warm, supportive, and helpful. If they have a question, answer it concisely. If they express a concern, reassure them while suggesting they mention it to their pediatrician if worried. If they share a positive observation, celebrate with them briefly.

IMPORTANT:
- Keep response under 50 words
- Be conversational and warm
- Use the baby's name ({name}) naturally
- Never diagnose or give medical advice
- For health concerns, gently suggest consulting their pediatrician"""

    user_message = f"""Milestone: {milestone_title}
Description: {milestone_description}
{status_context}

Parent's note: "{parent_note}"

Respond briefly to the parent's note:"""

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )

    return response.content[0].text
