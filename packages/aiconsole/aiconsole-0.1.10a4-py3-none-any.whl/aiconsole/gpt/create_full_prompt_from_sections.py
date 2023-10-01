import re
from typing import List

from aiconsole.aic_types import StaticManual


def create_full_prompt_from_sections(
    intro: str, sections: List[StaticManual], outro: str = "", section_marker="===="
):
    # Remove all section markers in intro, sections, and outro
    intro = re.sub(section_marker, "", intro)
    outro = re.sub(section_marker, "", outro)

    section_strs = []
    for static_manual in sections:
        name = f"{static_manual.id} ({static_manual.usage})"
        section = re.sub(section_marker, "", static_manual.content)
        section_strs.append(f"{section_marker} {name} {section_marker}\n{section}")

    # Construct the full prompt
    sub_str = "\n\n"
    full_prompt = f"{intro}\n\n" f"{sub_str.join(section_strs)}\n\n" f"{outro}".strip()

    return full_prompt
