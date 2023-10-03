import random


def get_analyse_system_content(system_description, available_agents, available_manuals):
    new_line = "\n"
    random_agents = new_line.join(
        [
            f"* {c.id} - {c.usage}"
            for c in random.sample(available_agents, len(available_agents))
        ]
    )
    random_manuals = (
        new_line.join(
            [
                f"* {c.id} - {c.usage}"
                for c in random.sample(available_manuals, len(available_manuals))
            ]
        )
        if available_manuals
        else ""
    )

    return (
        f"{system_description}\n\n"
        f"1. Establish the agent to handle the task, it can be one of the following ids:\n\n"
        f"{random_agents}\n\n"
        f"2. Figure out and provide a list of ids of manuals that are needed to execute the task, choose among the following ids:\n\n"
        f"{random_manuals}"
        "".strip()
    )
