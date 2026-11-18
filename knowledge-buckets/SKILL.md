---
name: knowledge-buckets
description: "Build and maintain a working understanding of a domain (a codebase, team, system, or technical field) in one file sorted into four buckets: facts, procedures, a 12-box mental model, and a questions log. Use when ramping up on a new area, consolidating what was learned in a session, or checking what is still unclear. Not for scoping a single learning experiment (use learning-lens) or for planning implementation work (use plan-writer)."
---

# Knowledge Buckets

Help the learner build an accurate, compact picture of one domain and keep it current. All knowledge for a domain lives in one Markdown file, sorted into four buckets. The aim is understanding the learner can use, not a complete archive: keep the file short, and improve it as understanding improves.

## Locate the knowledge file

One file per domain. Default path: `docs/learning/<domain-slug>.md` in the current project. Use a different path if the learner names one. If the file exists, read it before doing anything else and continue from it; never start over because the file is old or incomplete.

Ask at most one question before starting, and only if the domain is unclear: "Which area is this for?" Name the domain narrowly enough that a 12-box model can describe it ("Findem search indexing pipeline", not "Findem").

## The four buckets

Use this structure for the file:

```markdown
# <Domain>

_Last updated: YYYY-MM-DD_

## Facts
### Working memory
- <high-frequency fact the learner needs without looking up>
### Reference
- <low-frequency fact> — where to find it: <path, doc, or command>

## Procedures
### <Procedure name>
Steps: 1. … 2. …
Status: read | done with supervision | done alone (YYYY-MM-DD)

## Model
<diagram of at most 12 boxes, Mermaid or ASCII>
- <one line per important relationship or pattern the diagram shows>
Checked against: <expert, source doc, or code path> | unchecked

## Questions
- [ ] <open question>
- [x] <answered question> → <short answer or link> (YYYY-MM-DD)
```

### Facts: memorize less, look up more

Put a fact in **Working memory** only when the learner will need it often and slowly looking it up would block them: core names, scope, key interfaces, a handful of numbers. Keep this list short, roughly 15 items or fewer; if it grows, demote items. Everything else goes in **Reference** with *where to find it*, not the value itself when the value changes or is sensitive. Never write credentials, tokens, or secrets into the file; record only where they are kept.

### Procedures: learn by doing

Record step-by-step operations the learner must perform: deploys, on-call checks, running the test suite, debugging a known failure. Track how each procedure was learned, because reading a runbook is not the same as doing it. When a procedure is still at `read`, suggest the cheapest way to do it for real: in a sandbox, by driving while an expert watches, or by volunteering for the task. Promote the status only on the learner's report of actually doing it.

### Model: at most 12 boxes

Draw how the main components or ideas connect. Hard limit of 12 boxes; if the domain needs more, it is too broad: zoom out and merge, or split into a second domain file. Prefer the overall pattern (data flow, control flow, ownership boundaries) to implementation detail.

The model is a hypothesis until checked. Mark it `unchecked` until the learner has compared it against an expert, the authoritative docs, or the code. When the repository is available, verify boxes and arrows against the code yourself and cite the files; mark anything you could not confirm. Encourage the learner to draw the model from memory first, then compare it with the file, before you redraw it.

### Questions: a record that only grows

Capture every question as it comes up, including basic ones. When a question is answered, check it off and add a short answer or link; **never delete questions**. The list shows how understanding progressed and doubles as onboarding material for the next person. Order open questions with the ones blocking current work first.

## Working with the file

**Starting a domain:** create the file with the four headings. Seed it from what is available, such as the repository, docs the learner points to, or the conversation, and say which items came from which source. Seed the Questions bucket generously; an honest list of unknowns is more useful than a confident but wrong model.

**After a learning session:** ask what the learner did, read, or found out, or take it from the conversation. Sort each item into the right bucket, answer the questions you can answer from evidence (cite it), add new questions, and update the date. Show the learner a short summary of changes rather than reprinting the file.

**Checking gaps:** on request, report briefly: open questions blocking current work, procedures only at `read`, whether the model is `unchecked`, and working-memory items that seem stale. Recommend one next action, not a curriculum.

## Boundaries

- Keep it lean. Do not add buckets, tags, spaced-repetition schedules, or flashcard exports unless the learner asks.
- Do not invent facts to fill buckets. An empty section or an open question is better than a guess.
- Record what the learner knows and does; do not mark understanding or procedures as complete on their behalf.
- Updating the file is the job. Do not turn a session into a study plan, PRD, or new project.
