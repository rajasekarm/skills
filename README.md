# skills

My personal collection of agent skills. Each top-level folder is one skill that works in both **Claude Code** and **OpenAI Codex**, and can be installed user-wide or into a single project.

| Skill | What it does | Invoke |
| --- | --- | --- |
| [learning-lens](learning-lens/SKILL.md) | Clarify what you want to learn from a project idea and scope the smallest useful experiment. | Claude: `/learning-lens` · Codex: `$learning-lens` |
| [project-planner](project-planner/SKILL.md) | Write human-readable PRDs, milestone overviews, and per-milestone task tables grounded in repository evidence. | Claude: `/project-planner` · Codex: `$project-planner` |

Run `./install.sh --list` for the live list.

## Install

### Option A: one script, both hosts

```bash
git clone git@github.com:rajasekarm/skills.git ~/skills
cd ~/skills
./install.sh                      # all skills, user-wide, Claude Code + Codex (symlinks)
./install.sh project-planner      # just one skill
./install.sh --host codex         # only one host
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

The repo doubles as a Claude Code marketplace, so you can install without cloning:

```text
/plugin marketplace add rajasekarm/skills
/plugin install project-planner@rajasekarm-skills
```

or from the shell: `claude plugin marketplace add rajasekarm/skills && claude plugin install project-planner@rajasekarm-skills`. Updates come from `/plugin update project-planner@rajasekarm-skills`.

### Option C: Codex built-in skill installer

In a Codex session:

```text
$skill-installer install project-planner from rajasekarm/skills
```

Codex runs its `install-skill-from-github.py --repo rajasekarm/skills --path project-planner` helper and places the skill in `$CODEX_HOME/skills/project-planner`.

## Where skills land

| Host | User-wide | Project |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/<skill>/` | `.claude/skills/<skill>/` |
| Codex | `~/.codex/skills/<skill>/` | `.agents/skills/<skill>/` |

## Using several skills together

Both hosts read every installed skill's `name` and `description` into the agent's context and load the full `SKILL.md` only when a request matches. Small, focused skills therefore compose: the agent picks the one that fits, and a skill may hand off to a sibling by name (for example "then use `$worker-handoff`"). You can also chain them yourself in one prompt. Keep each skill's description specific about *when* to use it so the agent chooses correctly.

## Skill layout

```text
<skill-name>/
  SKILL.md                 # frontmatter (name, description) + instructions; read by both hosts
  .claude-plugin/plugin.json   # Claude Code plugin manifest ("skills": ["./"])
  agents/openai.yaml       # Codex UI metadata (display name, default prompt)
  assets/                  # templates the skill fills in
  references/              # longer docs loaded on demand
```

## Adding a new skill

1. Create `<skill-name>/SKILL.md` with `name:` matching the folder and a description that says when to use it.
2. Add `<skill-name>/.claude-plugin/plugin.json` (copy from `project-planner` and change the name/description).
3. Add `<skill-name>/agents/openai.yaml` for Codex's picker.
4. Add an entry to `.claude-plugin/marketplace.json` and the table above.
5. Validate: `claude plugin validate .` and `claude plugin validate <skill-name>`.

`install.sh` discovers skills automatically, so no changes there.

## Evaluating project-planner

See [the eval setup](evals/project-planner/README.md) for five isolated fixture cases, a dependency/link/structure checker, and a quality-review rubric. The harness uses Python's standard library; model runs are performed separately in fresh workspaces.
