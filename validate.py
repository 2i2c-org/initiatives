import nltk
from typing import Iterable
from mistletoe import Document
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.block_token import Heading
from mistletoe.token import Token

REQUIRED_HEADINGS = {
    "Level 1":[
        {
            "heading": "Problem Statement",
            "min_words": 50
        },
        {
            "heading": "Proposed Solution",
            "min_words": 50,
            "max_words": 500
        },
        {
            "heading": "Proposed Implementation",
            "min_words": 50,
            "max_words": 500
        },
        {
            "heading": "Where will this solution fit?",
            "min_words": 25,
        },
        {
            "heading": "Endorsements",
            "min_words": 0
        }

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
        print(f"Heading {heading} requires at least {min_words} words, found {word_count} words only")
        return False

    if "max_words" in heading_config:
        max_words = heading_config["max_words"]
        if word_count > max_words:
            print(f"Heading {heading} requires at most {max_words} words, found {word_count} words")
            return False

    return True



def render_tokens_md(renderer: MarkdownRenderer, tokens: Iterable[Token]) -> str:
    """
    Render tokens passed in as markdown

    Convenience function to convert AST to markdown
    """
    return ''.join([renderer.render(c) for c in tokens])

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
    missing_headers = set(h["heading"] for h in REQUIRED_HEADINGS["Level 1"]) - set(segments.keys())
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


MD = """
### Problem Statement

As a user on the hub, I want to have someone else get into the exact same kind of server I am on (environment, resource allocation, content pulled, etc) so we can work together with less accidental complexity caused by underlying server differences. Currently to do so, I have to explicitly give them verbal instructions on what options to choose or type in their 'Start Server' page ('Select the JupyterLab instance, and pick the 14.1 GB resource allocation, then click start'), which is error prone. It is particularly error prone when those instructions use features such as 'Unlisted choice' ('Select Other..., and type in this exact image, and avoid spaces') or 'Build your own image'. I want an easier and more succint way to share this that doesn't involve verbal instructions.

### Proposed Solution

As you make selections in your own 'Start Server' page, we create a link that encodes the choices you make in a stable fashion that is persistent over time. You can copy this link and share it with others, that lets them get to the exact same set of options you picked. You can choose to have this link *automatically* start the server too, so whoever you share it with does not necessarily need to read and understand the 'start a server' page either. This also allows you to make complex 'galleries' that can contain clickable links that not only allow for specific content to be checked out (via nbgitpuller), but also specific environments and resource selections to be chosen.

### Proposed Implementation

To do this, we would need to:

1. Have a 'permalink' implementation in jupyterhub-fancy-profiles that allows automatically filling in info based on a link (mostly done)
2. Changing our Resource Allocation script to provide more stable ids for resources so we can make adjustments we need to without breaking existing links
3. Add an 'autostart' feature to the permalinks in jupyterhub-fancy-profiles so they can automatically start servers if enabled (in review)
4. Roll this out to all users with appropriate documentation

### Where will this solution fit?

This solution will

### Endorsements

- This was pithced to Brian Frietag as part of VEDA PI planning and he wants us to drive this as a way to enable MAAP to be useful to end users.

"""


def main():
    # Download nltk data for tokenization if needed
    nltk.download("punkt_tab", quiet=True)
    print(validate(MD))

if __name__ == '__main__':
    main()