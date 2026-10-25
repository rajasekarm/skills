#!/usr/bin/env bash
# Install skills from this collection into Claude Code and/or Codex.
#
# Every top-level directory in this repository that contains a SKILL.md is a
# skill. By default this script installs all of them, user-wide, for both
# hosts, as symlinks back into this checkout (so `git pull` updates them).
#
# Usage:
#   ./install.sh [options] [skill ...]
#
# Options:
#   --host claude|codex|all   Which host(s) to install into. Default: all.
#   --scope user|project      User-wide or inside one project. Default: user.
#   --project DIR             Project root for --scope project. Default: $PWD.
#   --link                    Symlink into this checkout (default for user scope).
#   --copy                    Copy files (default for project scope).
#   --force                   Replace an existing install at the target path.
#   --uninstall               Remove the install instead of creating it.
#   --list                    List the skills in this collection and exit.
#   --dry-run                 Print what would happen without changing anything.
#   -h, --help                Show this help.
#
# Target locations:
#   Claude Code  user:    ${CLAUDE_CONFIG_DIR:-~/.claude}/skills/<skill>
#                project: <project>/.claude/skills/<skill>
#   Codex        user:    ${CODEX_HOME:-~/.codex}/skills/<skill>
#                project: <project>/.agents/skills/<skill>
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKER=".skill-source"

HOST="all"
SCOPE="user"
PROJECT_DIR=""
MODE=""
FORCE=0
UNINSTALL=0
LIST=0
DRY_RUN=0
SELECTED=()

usage() { sed -n '2,/^set -euo/p' "${BASH_SOURCE[0]}" | sed '$d' | sed 's/^# \{0,1\}//'; }
log()   { printf '%s\n' "$*"; }
warn()  { printf 'warning: %s\n' "$*" >&2; }
die()   { printf 'error: %s\n' "$*" >&2; exit 1; }
run()   { if [ "$DRY_RUN" -eq 1 ]; then log "  [dry-run] $*"; else "$@"; fi; }

while [ $# -gt 0 ]; do
  case "$1" in
    --host)      HOST="${2:-}"; shift 2 ;;
    --host=*)    HOST="${1#*=}"; shift ;;
    --scope)     SCOPE="${2:-}"; shift 2 ;;
    --scope=*)   SCOPE="${1#*=}"; shift ;;
    --project)   PROJECT_DIR="${2:-}"; shift 2 ;;
    --project=*) PROJECT_DIR="${1#*=}"; shift ;;
    --link)      MODE="link"; shift ;;
    --copy)      MODE="copy"; shift ;;
    --force)     FORCE=1; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --list)      LIST=1; shift ;;
    --dry-run)   DRY_RUN=1; shift ;;
    -h|--help)   usage; exit 0 ;;
    --)          shift; SELECTED+=("$@"); break ;;
    -*)          die "unknown option: $1 (see --help)" ;;
    *)           SELECTED+=("$1"); shift ;;
  esac
done

case "$HOST" in claude|codex|all) ;; *) die "--host must be claude, codex, or all" ;; esac
case "$SCOPE" in user|project) ;; *) die "--scope must be user or project" ;; esac
if [ -z "$MODE" ]; then
  if [ "$SCOPE" = "user" ]; then MODE="link"; else MODE="copy"; fi
fi
if [ "$SCOPE" = "project" ]; then
  PROJECT_DIR="$(cd "${PROJECT_DIR:-$PWD}" && pwd)"
  [ "$PROJECT_DIR" = "$REPO_DIR" ] && die "--scope project needs a target project; run from the project or pass --project DIR"
fi

# Discover skills: top-level directories with a SKILL.md.
ALL_SKILLS=()
for d in "$REPO_DIR"/*/; do
  d="${d%/}"
  [ -f "$d/SKILL.md" ] && ALL_SKILLS+=("$(basename "$d")")
done
[ ${#ALL_SKILLS[@]} -gt 0 ] || die "no skills found in $REPO_DIR"

skill_description() {
  # First "description:" line of the SKILL.md frontmatter, quotes stripped.
  awk '/^---$/{n++; next} n==1 && /^description:/{sub(/^description:[ ]*/,""); gsub(/^"|"$/,""); print; exit}' "$1/SKILL.md"
}

if [ "$LIST" -eq 1 ]; then
  for s in "${ALL_SKILLS[@]}"; do
    printf '%-24s %s\n' "$s" "$(skill_description "$REPO_DIR/$s")"
  done
  exit 0
fi

if [ ${#SELECTED[@]} -eq 0 ]; then
  SKILLS=("${ALL_SKILLS[@]}")
else
  SKILLS=()
  for s in "${SELECTED[@]}"; do
    s="${s%/}"; s="$(basename "$s")"
    [ -f "$REPO_DIR/$s/SKILL.md" ] || die "unknown skill: $s (run --list)"
    SKILLS+=("$s")
  done
fi

HOSTS=()
case "$HOST" in
  all)   HOSTS=(claude codex) ;;
  *)     HOSTS=("$HOST") ;;
esac

target_root() {
  case "$1:$SCOPE" in
    claude:user)    printf '%s' "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills" ;;
    claude:project) printf '%s' "$PROJECT_DIR/.claude/skills" ;;
    codex:user)     printf '%s' "${CODEX_HOME:-$HOME/.codex}/skills" ;;
    codex:project)  printf '%s' "$PROJECT_DIR/.agents/skills" ;;
  esac
}

# Returns 0 if the path is an install made from this repo (symlink into it, or
# a copy carrying our marker file).
ours() {
  local p="$1"
  if [ -L "$p" ]; then
    local resolved; resolved="$(readlink -f "$p" 2>/dev/null || true)"
    case "$resolved" in "$REPO_DIR"/*) return 0 ;; esac
    return 1
  fi
  [ -f "$p/$MARKER" ] && grep -q "^source: $REPO_DIR/" "$p/$MARKER"
}

install_one() {
  local host="$1" skill="$2"
  local src="$REPO_DIR/$skill" root; root="$(target_root "$host")"
  local dst="$root/$skill"

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if [ "$MODE" = "link" ] && [ -L "$dst" ] && [ "$(readlink -f "$dst")" = "$src" ]; then
      log "  $host: $skill already linked -> $dst"
      return 0
    fi
    if [ "$FORCE" -eq 1 ]; then
      ours "$dst" || warn "$dst was not installed from this repo; replacing because --force was given"
      run rm -rf "$dst"
    else
      die "$dst already exists. Inspect it, then re-run with --force to replace it."
    fi
  fi

  run mkdir -p "$root"
  if [ "$MODE" = "link" ]; then
    run ln -s "$src" "$dst"
    log "  $host: linked $skill -> $dst"
  else
    run cp -R "$src" "$dst"
    if [ "$DRY_RUN" -eq 0 ]; then
      local rev; rev="$(git -C "$REPO_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
      printf 'source: %s\nrevision: %s\ninstalled: %s\n' "$src" "$rev" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$dst/$MARKER"
    fi
    log "  $host: copied $skill -> $dst"
  fi
}

uninstall_one() {
  local host="$1" skill="$2"
  local root; root="$(target_root "$host")"
  local dst="$root/$skill"
  if [ ! -e "$dst" ] && [ ! -L "$dst" ]; then
    log "  $host: $skill not installed at $dst"
    return 0
  fi
  if ours "$dst" || [ "$FORCE" -eq 1 ]; then
    run rm -rf "$dst"
    log "  $host: removed $dst"
  else
    die "$dst was not installed from this repo. Re-run with --force to remove it anyway."
  fi
}

if [ "$UNINSTALL" -eq 1 ]; then
  log "Uninstalling (${SCOPE} scope${PROJECT_DIR:+, project $PROJECT_DIR}):"
else
  log "Installing (${SCOPE} scope, ${MODE}${PROJECT_DIR:+, project $PROJECT_DIR}):"
fi
for skill in "${SKILLS[@]}"; do
  for host in "${HOSTS[@]}"; do
    if [ "$UNINSTALL" -eq 1 ]; then uninstall_one "$host" "$skill"; else install_one "$host" "$skill"; fi
  done
done

if [ "$UNINSTALL" -eq 0 ] && [ "$DRY_RUN" -eq 0 ]; then
  log ""
  log "Done. Start a new session (or /reload-plugins in Claude Code) to pick up the skills."
  for skill in "${SKILLS[@]}"; do
    log "  Claude Code: /$skill    Codex: \$$skill"
  done
fi
