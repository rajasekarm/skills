# Several projects and plans

Read this when coordinating more than one plan or project. Each plan is still one `plan.md`. An optional planning hub adds [Projects.md](../assets/projects.md) (where each project's code and plans live) and [Portfolio.md](../assets/portfolio.md) (priorities).

```text
planning-hub/
  Projects.md
  Portfolio.md
project-repository/
  docs/plans/csv-export/plan.md
  docs/plans/account-deletion/plan.md
```

## References

Within a plan: `T1` in its own milestone, `M1/T1` elsewhere. Across plans: `PROJECT/PLAN/M1/T1`. Project IDs are unique in the registry; plan IDs are unique within a project. Keep machine-local checkout paths and credentials out of shared documents.

## Dependencies across plans

Check that referenced tasks exist and the combined graph has no cycles. Unknown or unaccepted external work keeps the consumer Draft or Blocked. Name the artifact, contract, or service version the consumer actually needs: a commit in another repository is not automatically available. Give each task one code repository; model cross-repository changes as explicit producer, consumer, and integration tasks.

## Choosing the next task

Follow the user's policy if one exists. Otherwise:

1. Continue work already in progress; a priority change does not preempt it.
2. Consider only Ready tasks with Done dependencies, an available environment, and no conflicting claim.
3. Order by portfolio rank, then task order in the plan, then full task reference.
4. The runner claims the task atomically before starting; a failed claim means choosing again.

Start with one active task per code repository. More agents need isolated workspaces and explicit limits. Surface repeatedly deferred work for a priority review.
