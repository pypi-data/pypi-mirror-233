<h1 align="center">AI Console</h1>

## Installing & Running

```shell
pip install --upgrade aiconsole --pre
cd your_project_dir
export OPENAI_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
aiconsole
```

aiconsole will create a bunch of working files like standard manuals and agents

## Running Your AI Console Dev Mode

In order to run your own AI Console:

1. CD into the project folder `/ai-console`
2. Install dependencies `poetry install` and `cd aiconsole/web && yarn`
3. In two distinct terminal windows run: `poetry run backend` and `cd aiconsole/web && yarn dev`

Optionally you can run `poetry run aiconsole` which will spawn two servers, but it's less ideal for development as it's often benefitial to restart just one.

Requires OPENAI_API_KEY env variable to be set.

### Running in another directory in dev mode

Often times you want to host aiconsole working files in another directory, even while developing. In order to do that you need to:

1. Discover the path to your env:
poetry env info

2. You will get something like: /Users/user/Library/Caches/pypoetry/virtualenvs/aiconsole-rmLpd4fO-py3.10

3. Execute in your directory of choice the following command:

```shell
vepath/bin/python -m aiconsole.init
```

so in our example that would be:

```shell
/Users/user/Library/Caches/pypoetry/virtualenvs/aiconsole-rmLpd4fO-py3.10bin/python -m aiconsole.init
```

## Publishing process

```shell
cd web && npm run build && cd .. && poetry build && poetry publish --username __token__ --password ...
```

## Manuals

Create .md files in ./manuals directory in the following format:


```md
<!---
Description of when this manual should be used?
-->

Actual content of a manual
```

Files are monitored and automatically loaded, then used as context. You can keep there API manuals, login information, prompts and other contextual information.

You can see examples of manuals i ./preset/manuals directory
