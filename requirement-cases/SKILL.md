---
name: requirement-cases
description: "Turn a raw requirement (from Slack, a ticket, a meeting, or a chat message) into a clear statement and a complete set of cases before planning: happy and alternate paths, negative and error cases, data cases, and non-functional cases, grounded in the current codebase. Resolves ambiguities by asking the user. Use when a new requirement arrives and you want to understand every case before writing a plan. Not for writing the implementation plan (use plan-writer) or for deciding what to build next (use opportunity-discovery)."
---

# Requirement Cases

Help the engineer fully understand a requirement before planning it. Requirements usually arrive incomplete: a Slack message, a ticket title, a sentence from a meeting. The aim is to find the cases the requester did not mention, so they get decided now rather than discovered during review or in production.

The output goes in chat only. Nothing is saved. If `plan-writer` runs next in the same session, it uses this analysis as input.

## 1. Capture the requirement as given

Quote the requirement exactly as the user provided it, along with where it came from (Slack, a ticket, a meeting) and who asked, if known. Do not rewrite it yet. Paraphrasing too early hides ambiguity.

If no requirement text was given, ask for it. Do nothing else first.

## 2. Restate it

Write a short restatement:

- **Goal:** the outcome the requester wants, in one sentence. Say why, if the source says why.
- **Actors:** who triggers the behavior and who is affected (user roles, services, jobs).
- **Trigger:** what starts the behavior (a user action, an API call, a schedule, an event).
- **In scope / out of scope:** what this requirement covers, and nearby things it does not.

Where the source does not support a point, mark it **Assumed** rather than presenting it as fact.

## 3. Ground it in the codebase

Read the repository for the parts this requirement touches: the data models and schemas, validations, API handlers, permission checks, background jobs, feature flags, and existing tests for nearby behavior. Search; do not guess paths.

Record what you find as **Confirmed** with a `file:line` citation, for example: "Confirmed: `email` is optional on `Candidate` (`models/candidate.py:42`)." Anything you could not find in code stays **Assumed**. Never invent a file, field, endpoint, or behavior.

Note any conflict between the requirement and the existing code (for example, the requirement assumes a field is always present but the schema allows null). Conflicts become questions in step 5.

If there is no repository, or the requirement touches code you cannot see, say so and continue with every case marked Assumed.

## 4. Enumerate the cases

Cover all four categories every time. For each category, list concrete cases, not generic labels. "User enters an invalid email" is too vague; "Email is present but has no domain (`a@`)" is a case. For each case, give the expected behavior if it is known, or `?` if it is not.

**Happy and alternate paths**
- The main flow from trigger to outcome.
- Valid variations: different roles, optional inputs present or absent, multiple items instead of one, different entry points into the same behavior.

**Negative and error cases**
- Invalid or malformed input.
- Missing permission or wrong role; acting on a resource the actor does not own.
- Failure of a dependency (database, downstream service, third-party API, queue): timeouts, errors, partial responses.
- The action is repeated, cancelled midway, or retried after failure.
- The resource is in an unexpected state (deleted, archived, locked, already processed).

**Data cases**
- Empty, null, and missing values for each relevant field.
- Boundary values: zero, one, the maximum, just over the maximum.
- Very large inputs or result sets (pagination, size limits, memory).
- Duplicates, and records that differ only by case or whitespace.
- Unicode, special characters, very long strings.
- Legacy or migrated data that predates current validations.
- Time zones, date boundaries, and clock differences, if time is involved.

**Non-functional cases**
- Scale and performance: expected volume, latency expectations, hot paths.
- Concurrency: two actors or two jobs acting on the same record at once.
- Idempotency: what happens if the same request or event arrives twice.
- Security and privacy: data exposure, access across tenants, injection, logging of sensitive fields.
- Backward compatibility: existing clients, APIs, stored data, and feature flags.
- Observability: what must be logged or measured to know the feature works in production.

Skip a category item only when it clearly cannot apply, and say why in one line (for example: "Time zones: not applicable, no dates involved").

## 5. Resolve ambiguities with the user

Collect every case marked `?`, every Assumed point that changes behavior, and every conflict from step 3. Ask the user about them in this session, before giving the final output.

- Group related questions so the user answers in as few rounds as possible. Ask the questions that change scope or data model first.
- For each question, offer two or three concrete options and recommend one with a reason, so the user can answer quickly.
- If the user does not know and the requester must decide, mark the question **Open (requester)** and move on. Do not invent an answer.

Fold each answer back into the cases. A case is resolved only when its expected behavior is stated.

## 6. Return the analysis

Give the final output in chat, in this order:

1. **Requirement:** the original text and its source.
2. **Restatement:** goal, actors, trigger, in scope and out of scope.
3. **Requirements:** numbered `R1`, `R2`, … Each is one testable statement of behavior. Under each, list its cases with expected behavior, grouped by category. Tag each fact Confirmed (with `file:line`) or Assumed.
4. **Decisions:** what the user decided in step 5, one line each.
5. **Open questions:** items still marked Open (requester), each with the requirements it blocks. Write these so they can be pasted straight back to the requester. Write `None` if there are none.
6. **Next step:** if there are no open questions, suggest running `plan-writer` in this session. If questions are open, say which requirements are safe to plan now and which must wait.

Keep it compact. One line per case is usually enough. Do not write the implementation plan, propose architecture, or estimate effort. Those belong to `plan-writer`.
