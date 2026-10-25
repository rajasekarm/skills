# Several projects and plans

Read this when coordinating more than one project or plan. Use the same human-readable PRD, milestone overview, and task tables in each project. An optional planning hub contains [Projects.md](../assets/projects.md) and [Portfolio.md](../assets/portfolio.md) for discovery and priorities.

## Storage

```text
planning-hub/
  Projects.md
  Portfolio.md
project-repository/
  docs/plans/P001-feature/
    PRD.md
    Milestone.md
    tasks/
      M1.md
      M2.md
```

Keep specifications in the owning planning repository and centralize only the registry/priority overview. Create or edit only projects within the user's requested scope. A project spanning repositories names one planning repository and registers each code repository. Machine-local configuration maps these identities to actual checkouts and capabilities.

## References people can read

Milestones are `M1`, `M2`; tasks are `T1`, `T2`, unique within their milestone. A task table uses these short labels. Dependencies within its milestone use `T1`, across milestones use `M1/T1`, and outside the plan use `PROJECT/PLAN/M1/T1`. Resolve short labels in the source row's context. Cross-milestone/project dependencies should link to the corresponding task section.

Project IDs are unique in the registry; plan IDs are unique within the project. Record the project and plan once in each document's readable details. A full task reference includes the milestone because `M1/T1` and `M2/T1` are different work. Requirements use their plan-scoped IDs, qualified as `PROJECT/PLAN/R-001` outside their plan.

Resolve a task through the registered project and plan, the PRD/milestone links, and its `tasks/Mn.md#tn` section. Dispatch pins the specification repository, file, commit, task reference, and task revision. Do not infer a task from a filename alone. During a requested migration, keep a readable old-to-new planning-ID mapping; preserve historical runtime identities and existing evidence.

## Dependencies and concurrent work

Check that referenced tasks exist, accepted inputs are available, and the dependency graph has no cycles, including across projects. Unknown external work keeps a consumer Draft or Blocked. Record the producer, accepted result/version, required contract/artifact, and where the worker obtains it.

Same-repository prerequisite code must be present in the consumer's runnable base. A commit in another repository is not automatically available: identify the artifact or API contract the consumer actually needs. Give each task one code repository and represent cross-repository changes through explicit producer, consumer, and integration work.

Only tasks with satisfied dependencies and independent editing/resource scope can run concurrently. Shared migrations, contracts, files, or services require ordering or an integration owner. Keep worker claims/status in the established tracker, or let one coordinator update the milestone task table; independent agents must not overwrite the shared document. The planner describes dependencies, not an executable queue.

## Choosing the next task

Respect the user's existing policy. If none exists, recommend:

1. Continue an owned active run; priority changes do not implicitly preempt it.
2. Filter active plans to Ready tasks with accepted dependencies, accessible specifications, usable code bases, compatible environments, no conflicting claims, and available capacity.
3. Order candidates by portfolio rank, then the team's task priority, then oldest readiness time and full task reference. Without a readiness timestamp, use the reference for the final tie-break.
4. Have the runner claim the chosen logical task before execution. A failed claim requires choosing again. Claims fence the task across revisions.

An explicit assignment still has to pass eligibility checks. Start with one serial dispatcher and one active task per actual code repository; multiple project aliases do not establish isolation. Additional agents need isolated workspaces and explicit concurrency/resource limits. Surface repeatedly deferred work for priority review.

## Results and review

Use the [handoff contract](worker-handoff.md). Return the same task reference, saved specification revision/commit, actual code repository/base/result, accepted dependency versions, observed checks, and blockers. Keep the narrative understandable; store bulky logs as linked evidence. The project reviewer accepts the saved task revision before Done.

Before delivery, check registry mappings, document links, scoped task identities, dependencies/cycles, editing conflicts, and an unambiguous priority order. Report next-task recommendations and exclusions accurately. This skill does not implement polling, claims, queues, or worker execution.
