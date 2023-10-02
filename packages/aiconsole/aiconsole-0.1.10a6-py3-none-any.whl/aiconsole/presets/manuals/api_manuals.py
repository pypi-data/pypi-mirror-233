# Manual

from aiconsole.manuals import manuals

def content(context):
    newline = "\n"
    return f'''
# Manuals

Available manuals: {newline.join(f'{f"* {manual.id} - {manual.usage}"}' for manual in manuals.all_manuals())}
'''

manual = {
    "usage": "Contains all the manuals available to agents.",
    "content": content,
}
