---
name: opportunity-discovery
description: "Staff engineer's companion for deciding what an engineering-led team (platform, infra, internal tooling, or a solo project) should build next. Gathers signals from the system, users, organization, and industry; checks them against the repo; and returns a ranked shortlist of three with evidence and the argument for each. Use when asked what to work on next, where the team should invest, how to find or justify platform work, or how to build a roadmap without a PM. Not for planning how to build a chosen item (use plan-writer) or for scoping a learning project (use learning-lens)."
---

# Engineering Opportunity Discovery

Engineering-led teams have no PM handing over a roadmap and no revenue line to say what worked. Work exists only when someone finds it. Signals are never scarce: outages, bills, workarounds, and repeated asks are always present. The failure mode is a backlog built from the **loudest** signal, usually the latest outage or a skip-level request. Your job is to collect signals across all four sources, weigh them, and argue for a few.

Output is a **ranked shortlist of three** opportunities, in chat. Do not write files, create tickets, or start planning or implementing. The chosen item goes to `plan-writer` afterward.

## 1. Frame the scope

Establish, in at most two questions if not already clear:

- **Unit:** which team, platform, service, or repo is being examined, and who its users are (internal teams, external customers, yourself).
- **Horizon and capacity:** roughly how much effort the next bet can take (a week, a quarter, one engineer, a team).

If the user already gave this, proceed. State any assumption you make.

## 2. Gather evidence from the repo first

Before asking anything else, read what is locally verifiable. Use the repo in the working directory unless the user names another. Look for:

| Signal | Where to look |
|---|---|
| Recurring failures | `postmortems/`, `incidents/`, RCA docs, runbooks; repeated themes across them, not one outage |
| Toil | runbooks with manual steps, scripts in `scripts/` / `bin/` that people run by hand, CI retries, flaky-test skips |
| Overloaded use-cases | config flags or code paths bolted on for one consumer, comments like "hack", "workaround", "for team X", forks or wrappers of the platform, abused generic fields |
| Debt and churn | `git log --since=6.months --name-only` hotspots, files touched in many fixes, TODO/FIXME/XXX density |
| Stale decisions | ADRs, design docs, or READMEs whose stated reasons no longer hold (dependency versions, scale numbers, "temporary" choices) |
| Migration debris | deprecated APIs still called, dual code paths, version flags that never reached 100% |
| Cost | infra-as-code sizing, over-provisioned resources, paid vendors or SaaS clients that the team could reconsider |
| LLM / inference cost | model calls in loops or hot paths, missing caching or batching, no token or spend limits, the largest model used where a smaller one would do |
| Security risk | auth boundaries, secrets in code or config, unvalidated input reaching execution paths, dependencies with known vulnerabilities |

Keep this pass bounded: sample, grep, and read headings. Do not read the whole codebase. Note the file path or command behind each finding; that is its evidence.

The repo is not the whole production system. Code shows that something *could* be slow, costly, or fragile; only metrics, incidents, bills, or users show that it *is*.

## 3. Interview for what the repo cannot show

Ask a short batch of questions (one message, at most five) for the sources code cannot reveal. Prefer recent and specific questions over opinions:

- **Users:** "What did a user team last ask for or complain about? What workaround have you seen them build on top of you?"
- **Cost:** "What does this cost per month, and which line is growing fastest? Any vendor contract up for renewal?"
- **Organization:** "What are this quarter's OKRs that touch this area? What topic have leaders brought up more than once recently?"
- **Adoption:** "Which teams have not migrated or adopted, and what do they say blocks them?"
- **Industry:** "Is there a design choice here that the wider industry has since moved away from or toward?"

If the user doesn't know an answer, record it as unknown. Do not invent numbers.

## 4. Record each signal

For each candidate signal, record:

- **Source:** System / Users / Organization / Industry.
- **Evidence:** file path, command output, or "reported by user."
- **Status:** **Confirmed** (directly supported by evidence of real impact: an incident, a metric, a bill, a user report) or **Hypothesis** (plausible but not yet shown to cause impact, including anything inferred only from reading code).
- **Timing:** **leading** (predicts future pain or value: workarounds, adoption gaps, industry shifts) or **lagging** (describes pain that already happened: outages, bills, toil).
- **Argument:** **pre-argued** (the case already exists: a postmortem, a cost line, an OKR) or **needs building** (you must assemble the case: industry lag, a leader's repeated topic, discovery conversations).

Merge signals that point to the same underlying problem. Several weak signals that converge are stronger than one loud one.

For each merged candidate, before ranking:

- **Root cause:** name why it happens, not just the symptom. If you can't, it stays a Hypothesis.
- **Existing solution:** check whether something already solves it (an internal library, a platform feature, a vendor, a half-finished effort). If it does, the opportunity is adoption, not building.

## 5. Rank

Use judgment, guided by these rules:

1. **Overloaded use-cases rank highest.** They are leading, and the argument is already running in production: users built the prototype for you. Check that more than one consumer shares the need before you generalize it.
2. **Convergence beats volume.** A problem seen in a postmortem, a workaround, *and* a cost line outranks a single dramatic incident.
3. **Prefer leading over lagging** when the evidence is otherwise comparable. Lagging signals are cheap to argue but tell you about the past.
4. **Discount the loudest.** The latest outage and the most senior opinion get a deliberate second look. A leader repeating a topic is the weakest signal on its own; treat it as a prompt to find evidence, not as evidence.
5. **Serve the long tail.** Teams that haven't migrated usually show where the platform is incomplete, not that those teams are stubborn.
6. **Buy versus build is never settled for good.** Revisit it when scale, the team, or the market has changed.
7. **Respect capacity.** A great opportunity that cannot fit the stated horizon gets a smallest-first-step version or drops down the list.

## 6. Return the shortlist

Return exactly this shape, concise and in plain language:

```markdown
## Scope
<unit, users, horizon; assumptions labeled>

## Top 3
### 1. <opportunity as a problem, not a solution>
- **Status:** <Confirmed/Hypothesis>
- **Evidence:** <items with paths or sources>
- **Root cause:** <why it happens>
- **Signal type:** <source(s)> · <leading/lagging> · <pre-argued/needs building>
- **Why now:** <what gets worse or what is lost by waiting>
- **Alternatives:** <could it be solved without building anything: config, process, adopting an existing tool, or doing nothing>
- **Case against:** <strongest reason not to do it>
- **Recommendation:** <smallest first step: a bounded probe or prototype that would confirm or kill it>
- **Success metric:** <baseline → target; if no baseline exists, how to collect one first>

### 2. ...
### 3. ...

## Considered and set aside
- <signal> — <one-line reason>

## Unknowns
- <question whose answer could change the ranking>

## Next action
<one concrete step, e.g. "Run /plan-writer on #1 with this evidence" or "Ask team X about their workaround">
```

Keep each opportunity framed as a **problem with evidence**, not a feature. A smallest first step is an exploration, not a commitment. Present a recommendation, but the user chooses. Do not start planning or implementing until they do.

## Guardrails

- No invented evidence: every claim names its source or is labeled Hypothesis/unknown.
- Never claim production is slow, expensive, or unreliable based only on reading source code.
- Do not pad the list. If fewer than three opportunities have real evidence, return fewer and say why.
- Do not expand scope: an idea outside the unit being examined goes to "Considered and set aside" rather than onto the shortlist.
- "Inventing work" means finding necessary work, never busywork. If no candidate beats doing nothing, say so.
