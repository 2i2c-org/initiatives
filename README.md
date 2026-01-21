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

## Yuvi's current process

1. We are participating in VEDA PI planning. Can we use that as an experiment to validate our overall structure?
2. Let's treat all the projects we are undertaking (user facing & non-user facing) for this VEDA quarter *that
   serve all our communities* as initiatives here. See if that is useful framing for *VEDA*, as they want to
   demonstrate the value they provide to the broader world.

## What is here?

1. This repository - particularly issues + labels
2. [This board](https://github.com/orgs/2i2c-org/projects/67/settings) primarily as a way to attach additional fields
   to issues. We may not use the Board UI at all
3. A `validate.py`, which is a linter for our structured issues. It's incomplete, but the idea would be that GitHub
   Actions would run this and set up labels correctly

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