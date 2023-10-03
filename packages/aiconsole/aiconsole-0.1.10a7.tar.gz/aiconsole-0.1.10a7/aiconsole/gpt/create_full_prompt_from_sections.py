import re
from typing import List

from aiconsole.aic_types import StaticManual


def create_full_prompt_from_sections(
    intro: str, sections: List[StaticManual], outro: str = ""
):
    section_strs = []
    for static_manual in sections:
        section_strs.append(f"\n\n{static_manual.content}")

    # Construct the full prompt
    sub_str = "\n\n"
    full_prompt = f"{intro}\n\n" f"{sub_str.join(section_strs)}\n\n" f"{outro}".strip()

    return full_prompt
