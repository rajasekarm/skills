# Quality review

Review the generated plan, fixture source, case expectations, and tool trace together. Treat `must_recognize` and `must_not_claim` as semantic assertions, not literal string matches. Quote a short excerpt or cite a file/line or trace event for each finding. Do not award points solely because a heading exists.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Repository grounding | Contradicts or invents the baseline | Mostly accurate, but key claims lack source evidence | Correctly distinguishes existing code, requirements, proposals, and assumptions with source references |
| Requirement coverage | Omits a core outcome or constraint | Covers the outcome but misses an acceptance or scope detail | Covers all requested outcomes with observable acceptance and traceability |
| Dependency correctness | Missing prerequisite, cycle, or unsafe readiness | Order mostly works, but acceptance gates or independent branches are unclear | Dependencies reflect actual inputs; readiness waits for acceptance; independent branches and integration are explicit |
| Executability | Material decisions or inputs are missing without being flagged | Useful direction, but some steps, setup, or verification need clarification | Next work has sufficient decisions, source locations, inputs, verification, and honest Draft/Blocked boundaries |
| Readability | Hard to identify outcome or next work | Understandable with avoidable ambiguity or repetition | Human-readable, concise, coherent documents with clear next work and completion conditions |

## Decision

A case passes when structure passes, every case expectation is satisfied, each dimension scores at least 1, and the total is at least 8/10. This is an initial project threshold; change it explicitly if experience warrants it.

The following are failures regardless of score:

- Fabricated repository facts, command results, or runtime evidence.
- Missing prerequisites, dependency cycles, or Ready work with a material unresolved decision.
- Violating case authority, including implementing features or running prohibited commands.
- Silently changing the meaning of preserved requirement/task identities.

A planning-quality pass does not demonstrate correct automatic skill selection. These five cases explicitly invoke the skill. Test routing separately with implicit planning prompts and implementation-only negative prompts when selection becomes part of the evaluation scope.

## Review record

Copy this into each run's `review.md`:

```text
Case:
Run/model/settings:
Skill revision or captured snapshot:
Structure: pass/fail (attach checker JSON)
Expectations: one finding per must_recognize / must_not_claim item, with evidence
Grounding: /2 — evidence
Coverage: /2 — evidence
Dependencies: /2 — evidence
Executability: /2 — evidence
Readability: /2 — evidence
Hard failures: none, or evidence
Total: /10
Decision: pass/fail
Limitations and reviewer:
```

A model reviewer should receive the same artifacts and rubric, separately from the generating session. Human-review disagreements and borderline scores before treating them as regressions. Do not show expectations or this rubric to the planner during a run.
