import typing

from gh_issue_validator import validate
from gh_issue_validator.checks.headings import CheckMissingHeadings, HeadingRequirement, CheckWordCount
from gh_issue_validator.types import SegmentsMap


HEADING_REQUIREMENTS =[
        {"heading": "Problem Statement", "min_words": 10},
        {"heading": "Proposed Solution", "min_words": 10, "max_words": 500},
        {"heading": "Proposed Implementation", "min_words": 10, "max_words": 500},
        {
            "heading": "How will this fit in the ecosystem?",
            "min_words": 10,
        },
        {"heading": "Endorsements", "min_words": 0}
]

validate(checks=[
    CheckMissingHeadings(requirements=HEADING_REQUIREMENTS),
    CheckWordCount(requirements=HEADING_REQUIREMENTS),
])
