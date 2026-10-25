# {{milestone_id}}: {{milestone_outcome}}

Read the [PRD](../PRD.md) and [milestone overview](../Milestone.md). This file contains every task for {{milestone_id}}, including its verification instructions.

## Starting point

Describe the existing behavior, shared setup, relevant source files, required services/data, and important constraints once. Distinguish the inspected baseline from the runnable base each task will need after its dependencies are accepted.

## Tasks

| Task | What to do | Depends on | Done when | Status |
| --- | --- | --- | --- | --- |
| [T1](#t1) | {{first_task_work}} | None | {{first_task_acceptance}} | Draft |
| [T2](#t2) | {{second_task_work}} | [T1](#t1) | {{second_task_acceptance}} | Draft |

Replace statuses with current readiness. T2 remains Draft until T1 is actually accepted. A Ready investigation may produce decisions; implementation that needs those decisions stays Draft as separate work.

## Execution order

Complete and review **T1 → T2** in order. T2 becomes Ready after T1's result is accepted.

Replace this example with the actual dependency graph, including any previous-milestone prerequisite. List genuinely independent tasks that can run together, their workspace/resource needs, and who integrates results. Do not invent parallelism or chain unrelated work automatically.

## Detailed task information

### T1

**{{first_task_work}}**

Explain why this work matters and state its requirements and scope.

#### Technical design

Name the technical approach, algorithm or data structure when it matters, explain why it fits, and define the relevant inputs/outputs, persistence, error behavior, and compatibility rules. Identify actual code locations and proposed new files. Keep material open decisions visible; preserve routine implementation choices for the implementer.

#### Implementation steps

Describe the ordered changes and integration points using the inspected source. Include the accepted inputs needed at each step.

For shared code or runtime setup, state which prerequisite produces the runnable input before its consumers start. An accepted design document or a named integration owner alone is not that runnable input. Independent branches must not wait on each other's unlisted shared work.

#### Verification

State the exact setup and commands or manual steps, expected observations, relevant failure cases, and evidence to return. Label checks as observed, source-inspected, or awaiting execution. During planning-only work, do not build a scratch implementation to try these checks; keep future behavioral verification not run.

Confirm shared environment setup, command exit-status expectations, and relevant library behavior. Compare field values when checking compatibility across formats. A recorded failure is not acceptance of the required behavior.

**Observed result:** Not run. Record passed/failed/not-run evidence and limitations after execution.

#### Starting revision and handoff

Task reference: `{{project_id}}/{{plan_id}}/{{milestone_id}}/T1`. Task revision: **1**.

State the repository, required starting code revision, environment, accepted prerequisite versions, and restart/retry behavior. Inspect and preserve existing partial work before retrying; limit cleanup to identified disposable artifacts owned by that run. Preserve existing execution/publication authority. Record run/result references only when they exist.

### T2

**{{second_task_work}}**

Explain what this task adds and the specific accepted T1 output it consumes. State its requirements and scope.

#### Technical design

Specify the required behavior, chosen approach and rationale, interfaces, source locations, and integration with T1's accepted result. Keep it Draft until material design decisions and the input contract are sufficient.

#### Implementation steps

Describe the ordered changes and how to preserve the accepted prerequisite behavior.

#### Verification

State the concrete steps, expected results, failure cases, and evidence for T2. Reuse shared setup by reference; do not repeat it in every task.

**Observed result:** Not run.

#### Starting revision and handoff

Task reference: `{{project_id}}/{{plan_id}}/{{milestone_id}}/T2`. Task revision: **1**.

Record the accepted T1 result/version and a code base containing its required changes before marking T2 Ready. Record remaining blockers explicitly.

## Review

A designated reviewer checks the saved task revision and observed evidence before Done. The task table is the status source unless an established tracker owns status; identify that source and label any mirror as a snapshot. One integration owner updates this shared file when agents work concurrently.

Project: **{{project_id}}**. Plan: **{{plan_id}}**. Updated: **{{date}}**.
