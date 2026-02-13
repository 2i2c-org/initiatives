from argparse import ArgumentParser
import os
import sys
import nltk
from typing import Iterable
from mistletoe import Document
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.block_token import Heading
from mistletoe.token import Token
from github import Github, Auth
from yarl import URL

REQUIRED_HEADINGS = {
    "Level 1": [
        {"heading": "Problem Statement", "min_words": 50},
        {"heading": "Proposed Solution", "min_words": 50, "max_words": 500},
        {"heading": "Proposed Implementation", "min_words": 50, "max_words": 500},
        {
            "heading": "How will this fit in the ecosystem?",
            "min_words": 25,
        },
        {"heading": "Endorsements", "min_words": 0},
    ]
}


def validate_segment(heading: str, level: str, content: str) -> bool:
    # Find segment config
    heading_config = None
    for h in REQUIRED_HEADINGS[level]:
        if h["heading"] == heading:
            heading_config = h
            break
    else:
        # Heading config not found, this shouldn't be here at this level
        print(f"Found heading {heading}, not expected at level {level}")
        return False

    words = nltk.word_tokenize(content.lower())
    word_count = len(words)

    min_words = heading_config.get("min_words", 0)
    if word_count < min_words:
        print(
            f"Heading {heading} requires at least {min_words} words, found {word_count} words only"
        )
        return False

    if "max_words" in heading_config:
        max_words = heading_config["max_words"]
        if word_count > max_words:
            print(
                f"Heading {heading} requires at most {max_words} words, found {word_count} words"
            )
            return False

    return True


def render_tokens_md(renderer: MarkdownRenderer, tokens: Iterable[Token]) -> str:
    """
    Render tokens passed in as markdown

    Convenience function to convert AST to markdown
    """
    return "".join([renderer.render(c) for c in tokens])


def parse_segments(markdown: str) -> dict[str, list[Token]]:
    """
    Parse given markdown into 'segments' separated by 2nd level headings

    Returns a dictionary where the key are the 2nd level headings and values are the contents
    of those headings.
    """
    with MarkdownRenderer() as renderer:
        doc = Document(markdown)
        if not doc.children:
            return {}

        document_segments = {}

        current_segment_header = None
        current_segment_content = []
        for c in doc.children:
            if isinstance(c, Heading) and c.level == 3:
                if current_segment_header is not None:
                    document_segments[current_segment_header] = current_segment_content
                current_segment_header = render_tokens_md(renderer, c.children).strip()
                current_segment_content = []
            else:
                current_segment_content.append(c)

        # Add the last segment
        document_segments[current_segment_header] = current_segment_content

        return document_segments


def validate(markdown: str) -> bool:
    """
    Validate that a passed in markdown is a valid level 1
    """

    segments = parse_segments(markdown)

    # Make sure that all the level headings are present
    missing_headers = set(h["heading"] for h in REQUIRED_HEADINGS["Level 1"]) - set(
        segments.keys()
    )
    if missing_headers:
        print(f"Missing headers: {missing_headers}")
        return False

    # Make sure that none of the content is practically empty
    with MarkdownRenderer() as renderer:
        for header, content in segments.items():
            md_content = render_tokens_md(renderer, content).strip()
            if not validate_segment(header, "Level 1", md_content):
                return False

    return True


def validate_issue(github: Github, account: str, repo: str, issue_id: int):
    issue = github.get_repo(f"{account}/{repo}").get_issue(issue_id)

    # Only act on open issues
    if issue.state != 'open':
        return
    if validate(issue.body):
        print(f"{issue.html_url} is valid")
        if "content-error" in issue.labels:
            issue.remove_from_labels("content-error")
    else:
        print(f"{issue.url} has content errors")
        issue.add_to_labels("content-error")


def main():
    # Download nltk data for tokenization if needed
    nltk.download("punkt_tab", quiet=True)

    argparser = ArgumentParser()
    argparser.add_argument(
        "issue", help="Issue to validate (Full URL or id on 2i2c-org/initiatives)"
    )
    args = argparser.parse_args()

    if args.issue.isdigit():
        account = "2i2c-org"
        repo = "initiatives"
        issue_id = int(args.issue)
    else:
        # Assume it's a full URL
        issue_url = URL(args.issue)
        parts = issue_url.path.split("/")
        if (
            issue_url.host != "github.com"
            or len(parts) != 5
            or parts[3] != "issues"
            or not parts[4].isdigit()
        ):
            print(f"Expected a GitHub issue URL, found {issue_url}", file=sys.stderr)
            sys.exit(1)

        account = parts[1]
        repo = parts[2]
        issue_id = int(parts[4])

    github = Github(auth=Auth.Token(os.environ["GITHUB_TOKEN"]))
    validate_issue(github, account, repo, issue_id)


if __name__ == "__main__":
    main()
