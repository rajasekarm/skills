# Workflow mode (Claude Code)

Use this only for a batch of two or more Ready tasks in the same milestone that have disjoint Files and no shared migration, contract, or service, when commits are allowed. The workflow parallelizes implementation. Verification and plan updates stay with you, one task at a time, after it returns.

Invoking this workflow is the explicit opt-in the Workflow tool requires, because this skill instructs it. Load the `workflow-authoring` skill first if it is available, and keep the batch under the session's workflow size guideline.

## What to pass

Pass the batch as `args`, an actual JSON array (not a string):

```json
[
  {"ref": "M1/T2", "brief": "<full subagent brief from SKILL.md>", "files": ["src/routes/summary.ts"], "verify": "npm test summary"},
  {"ref": "M1/T3", "brief": "<full subagent brief>", "files": ["src/routes/download.ts"], "verify": "npm test download"}
]
```

Each `verify` must be the focused command for that task's files (see Focused tests in SKILL.md), never the whole suite: parallel worktrees each running a full suite multiply the cost and leave stray runners.

Each brief must tell the subagent to commit its change on its worktree branch (so the work survives worktree cleanup) and to return that branch name. It still must not edit `plan.md`.

## Script

```js
export const meta = {
  name: 'plan-runner-batch',
  description: 'Implement independent plan tasks in parallel worktrees',
  phases: [{ title: 'Implement' }],
}

const RESULT = {
  type: 'object',
  properties: {
    ref: { type: 'string' },
    branch: { type: 'string' },
    files_changed: { type: 'array', items: { type: 'string' } },
    verify_command: { type: 'string' },
    verify_output: { type: 'string' },
    passed: { type: 'boolean' },
    blockers: { type: 'array', items: { type: 'string' } },
  },
  required: ['ref', 'branch', 'files_changed', 'verify_command', 'verify_output', 'passed', 'blockers'],
}

const results = await pipeline(args, task =>
  agent(task.brief, { label: task.ref, phase: 'Implement', isolation: 'worktree', schema: RESULT }))

const missing = args.filter((task, i) => !results[i]).map(task => task.ref)
if (missing.length) log(`No result for: ${missing.join(', ')}`)
return { results: results.filter(Boolean), missing }
```

## After it returns

Handle results in Graph order, one task at a time:

1. Set the task to `In review`. Merge its branch into the working branch. On a conflict, stop and report; do not resolve it by rewriting another task's work.
2. Read the diff, then run the task's Verify yourself on the merged code.
3. Pass: update `plan.md` for that task (Status, Progress line, readiness) before merging the next branch.
4. Fail or missing result: retry once with a subagent, then mark `Blocked` with the reason.

The subagent's `passed` field is a hint, never evidence. Workflow run IDs resume only within the same session; `plan.md` Status and Progress are the durable record.
