import typing

from gh_issue_validator import ValidationCheck, ValidationIssue, ValidationReport, validate
from gh_issue_validator.checks.headings import CheckMissingHeadings, HeadingRequirement
from gh_issue_validator.types import SegmentsMap


# Optional: Create your own validator based on the ValidationCheck ABC.
class ProblemStatementQualityCheck(ValidationCheck):
    """Reject problem statements that are just a URL."""

    @typing.override
    def check(self, *, segments: SegmentsMap, report: ValidationReport) -> None:
        heading_to_check = "Problem statement"
        content = segments.get(heading_to_check, [])
        if not content:
            return  # Empty content is handled by first-party CheckWordCount check.

        text = str(content).strip()
        if text.startswith("http") and " " not in text:
            # Our custom "issue" to report:
            report.add_issue(ValidationIssue(
                code="problem-statement-is-url",
                message="Problem statement should be a description, not just a URL.",
                heading=heading_to_check,
            ))

HEADING_REQUIREMENTS =[
        {"heading": "Problem Statement", "min_words": 10},
        {"heading": "Proposed Solution", "min_words": 10, "max_words": 500},
        {"heading": "Proposed Implementation", "min_words": 10, "max_words": 500},
        {
            "heading": "How will this fit in the ecosystem?",
            "min_words": 10,
        },
        {"heading": "Endorsements", "min_words": 0},
]

validate(checks=[
    CheckMissingHeadings(requirements=HEADING_REQUIREMENTS),
    CheckWordCount(requirements=HEADING_REQUIREMENTS)
    ProblemStatementQualityCheck(),
])
