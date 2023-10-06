# Manual
"""

# Top Trending repos on Github

```python
import trending_on_github
trending_repos = trending_on_github.get_top_trending_repos_information()
```

function declaration:
async   def get_top_trending_repos_information() -> dict

"""

import requests
from bs4 import BeautifulSoup

def get_top_trending_repos_information():
    """
    ****
    """
    url = "https://github.com/trending"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup = soup.find_all("div", attrs={"data-hpc": ""})[0]

    if not soup:
        return []

    repos = []

    for repo in soup.find_all("article", class_="Box-row"):
        try:
            repo_description = repo.find("p").text.strip()
            repo_url = repo.h2.a['href'].strip('/')
            repos.append({
                "name": repo_url,
                "description": repo_description,
            })
        except:
            pass

    return repos


manual = {
    "usage": "When you need to know what are the top trending repos on github",
}

