import os
import re
from pathlib import Path
from github import Github

g = Github(os.environ.get("GITHUB_TOKEN"))


def repl_starcount(match):
    repo = g.get_repo(f"{match.group('company')}/{match.group('repo')}")
    count = repo.stargazers_count
    if len(match.group("star")) > 0:
        return re.sub(f":star:{match.group('star')}", f":star:{count}", match.group(0))
    return f"[{match.group('text')} :star:{count}]({match.group('link')})"


def main():
    full_match = re.compile(
        r"\[(?P<text>.*?(:star:)?(?P<star>\d*))]\((?P<link>https?://github.com/(?P<company>[^/\n]*)/(?P<repo>[^/\n)]*).*)\)"
    )
    readme = Path(os.environ.get("myReadme", "readme.md"))
    text = readme.read_text()
    text2 = full_match.sub(repl_starcount, text, count=5)
    readme.write_text(text2)


if __name__ == "__main__":
    main()
