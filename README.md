# skills

My personal collection of agent skills. Each top-level folder is one skill that works in both **Claude Code** and **OpenAI Codex**, and can be installed user-wide or into a single project.

| Skill | What it does | Invoke |
| --- | --- | --- |
| [plan-writer](plan-writer/SKILL.md) | Write one focused `plan.md`: goal, dependency graph, milestones with demos, and tasks with concrete checks. Planning only. | Claude: `/plan-writer` · Codex: `$plan-writer` |
| [plan-runner](plan-runner/SKILL.md) | Execute a `plan.md`: the main agent coordinates, subagents implement, every task is re-verified and recorded in the plan. | Claude: `/plan-runner <plan.md>` · Codex: `$plan-runner <plan.md>` |
| [learning-lens](learning-lens/SKILL.md) | Clarify what you want to learn from a project idea and scope the smallest useful experiment. | Claude: `/learning-lens` · Codex: `$learning-lens` |

Run `./install.sh --list` for the live list.

## Plan, then run

`plan-writer` and `plan-runner` are a pair. One decides *what* to build and how to check it; the other gets it built and checked. You review at two points: the plan, and each milestone demo.

```text
you ──► /plan-writer "add CSV export"
          │  reads the repo, writes docs/plans/csv-export/plan.md
          ▼
you review and edit plan.md
          │
you ──► /plan-runner docs/plans/csv-export/plan.md
          │  main agent = coordinator
          │  for each Ready task:
          │    mark In progress → subagent implements → coordinator re-runs Verify
          │    → mark Done + add a Progress line (one task at a time)
          ▼
stops at the milestone Demo ──► you accept ──► next milestone
```

### 1. Write the plan

```text
/plan-writer Plan CSV export for signed-in users. Reuse existing auth.
```

It produces a single file, `docs/plans/<slug>/plan.md`:

```markdown
## Graph
M1/T1 → (M1/T2 ∥ M1/T3) → M2/T1

## M1: Export API returns correct CSV
**Demo:** `curl -H "Auth: …" localhost:3000/api/orders/export` returns a header and 3 rows.

| Task | Do | Files | Depends | Verify | Status |
| --- | --- | --- | --- | --- | --- |
| T1 | Add `toCsv(rows)` serializer | `src/export/csv.ts` (new) | None | `npm test csv` passes | Ready |
| T2 | Add `GET /api/orders/export` | `src/routes/orders.ts` | T1 | curl returns 200 + CSV | Draft |
| T3 | Reject unauthenticated export | `src/routes/orders.ts` | T1 | curl without auth → 401 | Draft |
```

Rules the plan follows:

- **Milestone** = something you can demonstrate, with a `**Demo:**` line. At most 5 per plan.
- **Task** = one reviewable change (about one PR), with the files to touch and a concrete **Verify** check. At most 7 per milestone.
- **Depends** + the **Graph** line show what waits for what (`→`) and what can run in parallel (`∥`).
- **Ready** only when every dependency is Done and nothing is undecided. Open decisions stay in **Open questions** and keep tasks Draft.
- Optional `### M1/T2 notes` hold only decisions an agent shouldn't make alone: contracts, chosen approach, code to reuse, constraints, edge cases.

The plan also has Goal, Context, Done when, Decisions, Open questions, and a Progress log. Template: [plan-writer/assets/plan.md](plan-writer/assets/plan.md).

### 2. Run the plan

```text
/plan-runner docs/plans/csv-export/plan.md          # whole plan, milestone by milestone
/plan-runner docs/plans/csv-export/plan.md M1       # one milestone
/plan-runner docs/plans/csv-export/plan.md M1/T2    # one task (good for a first try or a retry)
```

What the coordinator does:

1. Checks the plan and asks once whether it may commit (one commit per verified task).
2. Picks Ready tasks and sends each to a **subagent** with a self-contained brief. Subagents never edit `plan.md`.
3. Uses a **Workflow** (Claude Code) instead when several Ready tasks touch separate files: they are implemented in parallel git worktrees, then merged and verified one by one.
4. Re-runs each task's **Verify** itself; a subagent saying "done" is not evidence.
5. Right after each task passes, updates the plan: Status → Done, plus a Progress line such as
   `- 2026-11-05 M1/T1 Done — npm test csv → 12 passed (a1b2c3d)`.
   Dependents become Ready only then.
6. On failure, retries once, then marks the task Blocked with the reason and stops.
7. At the end of each milestone, runs the Demo and **stops for your acceptance**.

Rerunning the same command resumes from the plan's Status column. It never pushes, opens PRs, or deploys.

Codex: the same loop runs one task at a time; Workflow mode is Claude Code only.

## Install

### Option A: one script, both hosts

```bash
git clone git@github.com:rajasekarm/skills.git ~/skills
cd ~/skills
./install.sh                          # all skills, user-wide, Claude Code + Codex (symlinks)
./install.sh plan-writer plan-runner  # just these skills
./install.sh --host codex             # only one host
```

User-wide installs are symlinks into the checkout, so `git pull` updates every host at once.

To install into a single project instead (copies, so the project stays self-contained):

```bash
cd /path/to/project
~/skills/install.sh --scope project                 # -> .claude/skills/ and .agents/skills/
~/skills/install.sh --scope project --host claude   # only Claude Code
```

Other flags: `--copy` / `--link` to override the default mode, `--force` to replace an existing install, `--uninstall` to remove, `--dry-run` to preview. Honors `CLAUDE_CONFIG_DIR` and `CODEX_HOME`.

### Option B: Claude Code plugin marketplace

```text
/plugin marketplace add rajasekarm/skills
/plugin install plan-writer@rajasekarm-skills
/plugin install plan-runner@rajasekarm-skills
```

Update with `/plugin update <skill>@rajasekarm-skills`.

### Option C: Codex built-in skill installer

In a Codex session:

```text
$skill-installer install plan-writer from rajasekarm/skills
$skill-installer install plan-runner from rajasekarm/skills
```

## Where skills land

| Host | User-wide | Project |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/<skill>/` | `.claude/skills/<skill>/` |
| Codex | `~/.codex/skills/<skill>/` | `.agents/skills/<skill>/` |

Both hosts read every installed skill's `name` and `description` and load the full `SKILL.md` only when a request matches, so keep descriptions specific about *when* to use a skill.

## Skill layout

```text
<skill-name>/
  SKILL.md                     # frontmatter (name, description) + instructions; read by both hosts
  .claude-plugin/plugin.json   # Claude Code plugin manifest ("skills": ["./"])
  agents/openai.yaml           # Codex UI metadata (display name, default prompt)
  assets/                      # templates the skill fills in
  references/                  # longer docs loaded on demand
```

## Adding a new skill

1. Create `<skill-name>/SKILL.md` with `name:` matching the folder and a description that says when to use it.
2. Add `<skill-name>/.claude-plugin/plugin.json` (copy from `plan-writer` and change the name/description).
3. Add `<skill-name>/agents/openai.yaml` for Codex's picker.
4. Add an entry to `.claude-plugin/marketplace.json` and the table above.
5. Validate: `claude plugin validate .` and `claude plugin validate <skill-name>`.

`install.sh` discovers skills automatically, so no changes there.
