---
name: first-principles
description: "Reason about an engineering problem from first principles: state the function the system must deliver, split today's assumptions into real constraints (latency, throughput, memory, consistency, cost, contracts) and inherited conventions, challenge each convention with Socratic questions and Five Whys, size the fundamentals with numbers, and rebuild one or two alternatives from the constraints alone. Grounds constraints in the repo when one is present. Use when a design, architecture, or recurring problem feels like it is being solved by copying an existing form, when costs or complexity seem out of proportion to the job, or before choosing between options. Not for comparing already-chosen options or writing an ADR (use engineering:architecture), for enumerating requirement cases (use requirement-cases), or for writing an implementation plan (use plan-writer)."
---

# First Principles

Help the engineer reason about a problem from what is actually true, instead of by analogy to how it is usually done. Reasoning by analogy copies an existing form and makes small changes to it ("we use a queue because the last service did"). First principles thinking breaks the problem down to what is verifiably true in this context, then reasons back up from there.

Two rules shape everything below:

- **Optimise the function, not the form.** The function is the outcome the system must deliver. The form is the current way of delivering it. Most inherited cost and complexity lives in the form.
- **Go one or two levels deeper than usual, not all the way down.** The goal is the irreducible facts *for this problem* (a latency budget, a data volume, a contract), not physics for its own sake. Stop once more depth would not change the answer.

The output goes in chat only. Nothing is saved. If `engineering:architecture` or `plan-writer` runs next in the same session, it uses this analysis as input.

Based on Shane Parrish, "First Principles: The Building Blocks of True Knowledge" (fs.blog/first-principles) and James Clear, "First Principles: Elon Musk on the Power of Thinking for Yourself" (jamesclear.com/first-principles).

## 1. Capture the problem and the current approach

Quote the problem as the user gave it. Then write down the current or proposed approach: what exists today, or the solution the user is leaning towards. If there is no current approach yet, write down the approach that would be copied by default (what a similar system, team, or tutorial would do). That default is what this analysis tests.

If no problem was given, ask for it. Do nothing else first.

## 2. State the function

Write the outcome the system must deliver in one or two sentences, without naming any part of the current solution.

- Good: "A recruiter sees search results that reflect profile edits within 5 seconds, at 200 queries per second."
- Bad: "We need a cache invalidation layer." That describes a form.

If the user cannot state the function without naming the solution, the problem is not yet understood. Ask what would happen to users or the business if the current solution vanished. The answer to that question is the function.

## 3. List the assumptions and tag each one

List everything the current approach takes for granted: requirements, limits, technology choices, team habits, "must haves". Aim for completeness. Unstated assumptions are the ones that cause trouble.

Tag each one with a type:

- **Constraint:** a real limit the solution cannot escape. Examples: latency or throughput required by users or an SLA, available memory or hardware, data volume and growth, consistency or durability guarantees the business depends on, cost ceilings, legal and security requirements, API contracts with clients you do not control.
- **Convention:** something inherited rather than required. Examples: "we always use X for this", a pattern copied from another service, a limit that existed once but may not now, a tool chosen because the team knows it, a requirement nobody can trace to a user need.

Also tag each one with its evidence:

- **Confirmed:** backed by code, config, metrics, docs, or a contract. Cite it (`file:line`, a dashboard, a doc). When a repository is present, read the relevant code, config, schemas, and tests to confirm or refute assumptions. Search; do not guess paths. Never invent a file, metric, or behavior.
- **Assumed:** believed but not verified.

A constraint that is only Assumed is a risk: the whole rebuild may rest on it. Flag it. If there is no repository or no data, say so and continue with everything marked Assumed.

## 4. Challenge each convention

For every Convention, and for every Constraint that is only Assumed, run the questions below. Ask the user when only they can answer. Do not invent answers.

**Socratic questions** (from Parrish):

1. **Clarify:** Why do we think this? What exactly do we think?
2. **Challenge:** How do we know this is true? What if the opposite were true?
3. **Evidence:** What backs this up? What are the sources?
4. **Alternatives:** What would someone from another team, company, or field do?
5. **Consequences:** What if we are wrong? What breaks, and how badly?
6. **Question the question:** Why did we frame it this way? What does this reasoning tell us?

**Five Whys:** ask "why is this needed?" repeatedly until the answer is either a real constraint (a user need, a measured limit, a contract) or "because that's how it's done". The second answer means it is a convention that can be dropped.

Each assumption ends in one of three states:

- **Kept as a constraint**, with the evidence that makes it real.
- **Dropped**: a convention with no real reason behind it. Say what it was protecting against, if anything.
- **Open**: needs data or a decision you cannot get now. Say what would settle it.

Never drop a Confirmed constraint because it is inconvenient.

## 5. Size the fundamentals

Put numbers on what the kept constraints actually demand, using back-of-envelope estimates: requests per second, bytes per record, total data size, network round trips, p99 latency budget split across components, compute and storage cost, engineer-hours to operate.

Then compare:

- **The ideal:** what the kept constraints alone would require.
- **The current:** what the current approach costs or uses.

A large gap means conventions are adding cost. (In the source articles, the raw materials of a rocket were about 2% of its price, so most of the price came from how rockets were usually built, not from what they needed.) Show each estimate's arithmetic and inputs, and tag each input Confirmed or Assumed. If the gap is small, say so. The current approach may already be close to the fundamentals.

## 6. Rebuild from the constraints

Using only the kept constraints and the function from step 2, propose one or two alternative designs. For each:

- How it delivers the function.
- Which dropped conventions it no longer needs.
- What it borrows, if anything, from another domain or system (the printing press combined a wine press with movable type).
- Its main risk.

Include the current approach as a baseline and compare all options against the function and the sized fundamentals in a short table.

If the rebuild arrives back at the current design, say so plainly. That is a valid result: the current approach is now justified by constraints rather than by habit.

## 7. Test the rebuild

For each alternative, state:

- **What would prove it wrong:** the measurement, prototype, or fact that would kill it, and the cheapest way to check that first.
- **Cost of being wrong:** what happens if it fails after adoption, and whether it can be reversed.

First principles reasoning sets the direction. It does not replace iterating on the details, so the next step should be a small, cheap check, not a rewrite.

## 8. Return the analysis

Give the final output in chat, in this order:

1. **Problem:** the original text and the current or default approach.
2. **Function:** the outcome, with no solution named.
3. **Assumptions:** a table with columns Assumption | Constraint or Convention | Confirmed or Assumed (with evidence) | Result (Kept / Dropped / Open).
4. **Fundamentals:** the estimates, ideal against current, and the size of the gap.
5. **Options:** the current baseline plus one or two rebuilt alternatives, compared in a table.
6. **Recommendation:** which direction, and why, in two or three sentences. Say whether the analysis changed the direction or confirmed the current approach.
7. **Cheapest next check:** the one experiment, measurement, or question that would most reduce uncertainty.
8. **Open questions:** items marked Open, each with who or what can settle it. Write `None` if there are none.

Keep it compact. One line per assumption is usually enough.

## Failure modes to avoid

- **Analogy creeping back in:** justifying a choice with "company X does it this way" without knowing whether X has the same constraints.
- **Going too deep:** breaking the problem down past the point where it changes the answer. Stop at one or two levels below the usual.
- **Dropping real constraints:** treating a measured limit or an external contract as a convention.
- **Form disguised as function:** writing the function in step 2 in terms of the current solution.
- **Rebuilding everything:** recommending a rewrite when the gap in step 5 is small or the cheapest check has not been run.
- **Invented evidence:** citing a file, metric, or number that was not actually read or given. Mark it Assumed instead.
