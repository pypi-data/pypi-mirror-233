# Manual

from aiconsole.agents import agents

def content(context):
    newline = "\n"
    return f'''
# Agents

Available agents: {newline.join(f'{f"* {agent.id} - {agent.usage}"}' for agent in agents.all_agents())}
'''

manual = {
    "usage": "Contains info about all the agents in AIConsole, useful when you want to know what agents are available and what they can do.",
    "content": content,
}
