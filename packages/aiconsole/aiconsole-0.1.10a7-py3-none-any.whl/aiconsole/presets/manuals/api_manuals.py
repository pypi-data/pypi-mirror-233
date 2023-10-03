# Manual

from aiconsole.manuals import manuals

def content(context):
    newline = "\n"
    return f'''
# Manuals

Available manuals: {newline.join(f'{f"* {manual.id} - {manual.usage}"}' for manual in manuals.all_manuals())}

## Location

Manuals are stored in the `./manuals` directory. Each manual is a .md file with following structure:

```md
<!---
Description of when this manual should be used?
-->

Actual content of a manual
```

Note that <!--- ... --> is required for the description to be parsed correctly.

it can also be a .py file with following structure:

```py
# Manual

def content(context):
    return f"""
# Manual

Manual content
```

When asked to save a manual, write a file with the same name as the manual id in the `./manuals` directory. use lower case letters and underscores for spaces. For example, if you want to save a manual with id `My Manual`, save it as `my_manual.md` in the `./manuals` directory.

## Writing Manuals
When you need to write a manual based on a conversation so far, extract key information from this conversation in very consise form, use only one main header (#). The goal is for you to read those instructions later, and be able to do this faster next time.


"""

manual = {{
    "usage": "Description of when this manual should be used?",
    "content": content,
}}
'''.strip()

manual = {
    "usage": "Contains an index of manuals for manipulating them (saving, editing etc). Do not use if not tasked to directly manipulate manuals or learning about capabilities of this AIConsole instance.",
    "content": content,
}
