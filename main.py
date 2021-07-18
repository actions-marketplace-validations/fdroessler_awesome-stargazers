import os
import re
from pathlib import Path
from github import Github

# Use the github_token from actions
g = Github(os.environ.get("GITHUB_TOKEN"))


def repl_starcount(match: re.Match) -> str:
    """Add stargazer count to a github link or update the count if it already exists.
    
    Arguments:
        match: github link match with keys: company, repo, star, link and
            description text
    """
    repo = g.get_repo(f"{match.group('company')}/{match.group('repo')}")
    count = repo.stargazers_count
    # if the link already contains a stargazer count we only want to update that one
    if len(match.group("star")) > 0:
        return re.sub(f":star:{match.group('star')}", f":star:{count}", match.group(0))
    return f"[{match.group('text')} :star:{count}]({match.group('link')})"


def main():
    # This regular expression matches links like the following:
    # [some text](https://github.com/company/repo)
    # also
    # [some text :star:133](http(s)://github.com/company/repo)
    # explanation here: https://regex101.com/r/DzHIb5/1
    full_match = re.compile(
        r"\[(?P<text>.*?(:star:)?(?P<star>\d*))]\((?P<link>https?://github.com/(?P<company>[^/\n]*)/(?P<repo>[^/\n)]*).*)\)"
    )
    readme = Path(os.environ.get("myReadme", "readme.md"))
    text = readme.read_text()
    text2 = full_match.sub(
        repl_starcount, text, count=int(os.environ.get("NUM_REPLACEMENTS", 0))
    )
    readme.write_text(text2)


if __name__ == "__main__":
    main()
