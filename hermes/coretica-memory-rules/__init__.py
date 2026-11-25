"""Supply the canonical Coretica instructions through Hermes' public prompt API."""

from pathlib import Path


def register(ctx):
    skill = Path(__file__).resolve().parent / "skills/coretica-memory/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    _, separator, body = text.partition("\n---\n")
    if not text.startswith("---\n") or not separator:
        raise ValueError("Coretica's bundled skill has invalid frontmatter")
    body = body.strip()
    # Hermes skips oversized sections. Fail visibly instead of silently omitting
    # the save, privacy, or retry rules when the shared skill changes.
    if not body or len(body) > 4000:
        raise ValueError("Coretica's memory instructions must contain 1–4000 characters")
    ctx.register_system_prompt_section(
        "coretica.private-memory", body, position="after_memory", max_chars=4000
    )
