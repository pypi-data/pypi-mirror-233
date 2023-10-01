# Manual

from aiconsole.agents import agents

def content(context):
    newline = "\n"
    return f'''Available agents: {newline.join(f'{f"* {agent.id} - {agent.usage}"}' for agent in agents.all_agents())}'''

manual = {
    "usage": "Contains info about all the agents in AI Console.",
    "content": content,
}
