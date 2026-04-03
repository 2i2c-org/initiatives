# Initiatives

Experimental repository to contain 2i2c org-wide public initiatives
that are available for communities to fund together

## Why?

Our [public roadmap](https://2i2c.org/roadmap/index) is excellent, and needs a single source
of *structured* truth. When this repository was started, it's source of truth is initiatives
in:

1. Issues in the [2i2c-org/infrastructure](https://github.com/2i2c-org/infrastructure) repo
2. Specific words used in the title of the issues
3. Specific *labels* applied to the issue
4. Specific Project Fields set in the [Products & Services Board](https://github.com/orgs/2i2c-org/projects/57)

In addition, the issues in the infrastructure repository have a few problems:

1. They were originally written with an *internal* facing audience, to serve as parent
   issues for subtasks. They are not particularly friendly to external audiences, and are
   thus not easy to use as *sales assets*.
2. Some of them are stale or outdated, as our thinking has evolved over time.

This repository, along with [a corresponding new project board](https://github.com/orgs/2i2c-org/projects/67/views/1)
is an experiment to try the following:

1. Can we use GitHub project fields as a *dedicated* way to measure structured pieces of
   information (such as levels of detail, current funding situation, internal / external labels,
   etc) that are useful to publicly surface?
2. Can we use GitHub actions to automatically (and deterministically) *lint*
   these issues, to make sure that they *actually* follow the standard structure we
   are trying to follow with our levels of detail?
3. (not as important) can the code that maintains [our public roadmap](https://2i2c.org/roadmap/index) be simpler
   and more clearly maintainable if it pulls from a structured github project?
4. Can we rewrite some of the existing initiatives to have a more external facing focus?
   For example, compare [this](https://github.com/2i2c-org/infrastructure/issues/5381) (old) to
   [this](https://github.com/2i2c-org/initiatives/issues/5) new.
5. Can we have issue templates here that make it easier for folks to create structured content?

## Timeline

There is always risk of too much fiddling with a system as a way to procrastinate actually using
the system, so this should not take more than one week. Let's learn what we can at the one week mark
and move on.

## What is here?

1. This repository - particularly issues + labels
2. [This board](https://github.com/orgs/2i2c-org/projects/67/settings) primarily as a way to attach additional fields
   to issues. We may not use the Board UI at all
3. A `validator`, which is a linter for our structured issues.

## Issue Structure

All issues here **must** have the following headings, *and the following headings only*.

1. Problem Statement
2. Proposed Solution
3. Proposed Implementation
4. How will this fit in the ecosystem?
5. Endorsements
6. (Optional) Other Information

There is a [new initiative](https://github.com/2i2c-org/initiatives/issues/new?template=01_new-initiative.yaml)
template that will help you keep to this structure.

We have a GitHub action that will run on each edit to issues, and
apply error labels (`error:extra-heading`, `error:missing-heading`, `error:incomplete-info` or `error:too-much-info`)
based on what the error is. This lets us keep consistently high
quality in our content

## Data Model

An incomplete description of the data model, split between project board fields (for almost everything) and issue labels
(specifically for 'multi select' values, [until GitHub implements them in project fields](https://github.com/orgs/community/discussions/6580)).

1. "Level of Detail" represents how complete this initiative is. Only those with at least "Level 1" should be displayed in
   the public roadmap, as it ensures we have a basic minimum structure for the content of each publicly visible initiative.
2. "Status" represents the current status of actual work on the initiative, between "Not Started", "In Progress" and "Done".
3. "interested:<community-name>" labels (all colored the same) that indicate interest in this feature expressed by a specific
   community.
4. "co-funded:<community-name>" labels (all colored the same) that indicate we have a firm, signed commitment (either as a
   contract or via a different process) that indicate we can start work on this initiative.
5. "User visible" indicates if this initiative results in anything that is visible to end users or admins, or if it will
   be internal engineering improvements that strengthen foundations.
6. "Rough size" indicates a broad idea of how 'big' we think doing the implementation of this initiative is.
7. "Rough Hours Estimate Range" is provided in *some specific cases* as a lower and upper bound 'hours' estimate for use in
   proposals. This is *risky* to use when done without a more detailed work plan, and should be used rarely. If this number
   is changed, please leave a comment about why so there is a record - GitHub does not track changes in fields. This value
   should be estimated for use in talking directly to communities **as is**, without any additional tweaks from business
   development or grant writers.

## How do I...?

### Record that a community is interested in an initiative?

We use the label `interested:<community-name>` to indicate that a specific community has expressed interest in
an initiative. If such a label does not exist, please create one (with color `#f6fd60`) and apply it.

### Handle initiatives that require different implementations per cloud provider?

Under very specific circumstances, we have initiatives that will need to be re-implemented for each cloud provider we support. Since
we want to do our work in service of specific communities, we don't want to block an initiative being completed for a long time as we
wait for a different community to have a need. So, initiatives that require per-cloud implementations will be split into two
initiatives, and tracked separately.