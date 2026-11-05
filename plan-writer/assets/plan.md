# {{plan_title}}

## Goal

{{one_sentence_user_outcome}}

## Context

{{why_this_matters}} Already works: {{existing_behavior}} (`{{source_file}}:{{line}}`). Out of scope: {{exclusions}}.

## Graph

M1/T1 → (M1/T2 ∥ M1/T3) → M2/T1

## M1: {{first_milestone_outcome}}

**Demo:** {{command_or_action}} shows {{expected_observation}}.

| Task | Do | Files | Depends | Verify | Status |
| --- | --- | --- | --- | --- | --- |
| T1 | {{one_reviewable_outcome}} | `{{path}}` | None | `{{command}}` → {{expected_output}} | Ready |
| T2 | {{one_reviewable_outcome}} | `{{path}}` | T1 | {{action}} → {{observation}}; {{failure_case}} | Draft |
| T3 | {{one_reviewable_outcome}} | `{{path}}` (new) | T1 | {{action}} → {{observation}} | Draft |

### M1/T2 notes

- **Contract:** {{interface_or_format_other_tasks_rely_on}}
- **Approach:** {{chosen_design}} because {{reason}}.
- **Reuse:** `{{existing_function}}` in `{{source_file}}:{{line}}`.
- **Edge cases:** {{cases_that_must_work}}
- **Open:** {{unresolved_decision}}. T2 stays Draft until decided.

## M2: {{second_milestone_outcome}}

**Demo:** {{command_or_action}} shows {{expected_observation}}.

| Task | Do | Files | Depends | Verify | Status |
| --- | --- | --- | --- | --- | --- |
| T1 | {{integrate_or_expose_result}} | `{{path}}` | M1/T2, M1/T3 | {{end_to_end_check}} | Draft |

## Done when

- [ ] M1 and M2 demos pass and are accepted.
- [ ] {{overall_acceptance}}

## Decisions

- D1: {{decision}} because {{reason}}.

## Open questions

- {{question}}: blocks M1/T2.

## Progress

- Not started
