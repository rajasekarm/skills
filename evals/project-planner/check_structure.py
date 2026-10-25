#!/usr/bin/env python3
"""Check a generated plan. Standard-library only; semantic expectations need review."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def prose(text):
    return re.sub(r'^\s*(```|~~~).*?^\s*\1\s*$', '', text, flags=re.M | re.S)


def anchors(text):
    counts, result = Counter(), set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug = re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
        index = counts[slug]
        counts[slug] += 1
        result.add(slug + (f'-{index}' if index else ''))
    return result


def check(plan, workspace, required):
    errors, graph, documents = [], {}, {}
    def fail(message):
        errors.append(message)
    if not plan.is_dir():
        return [f'Plan directory missing: {plan}']
    for name in required:
        if not (plan / name).is_file():
            fail(f'Missing required file: {name}')
    for path in plan.rglob('*.md'):
        documents[path.resolve()] = prose(path.read_text())
    task_files = sorted((plan / 'tasks').glob('*.md'))
    if not task_files:
        fail('No milestone task files')
    for path in task_files:
        if not re.fullmatch(r'M[1-9]\d*', path.stem):
            fail(f'{path.name}: expected milestone filename Mn.md')
            continue
        text = documents[path.resolve()]
        for heading in ('Execution order', 'Detailed task information'):
            if not re.search(r'^##\s+' + heading + r'\s*$', text, re.M):
                fail(f'{path.name}: missing {heading} section')
        lines = text.splitlines()
        rows = [line.strip().strip('|').split('|') if line.strip().startswith('|') else None for line in lines]
        expected = ['Task', 'What to do', 'Depends on', 'Done when', 'Status']
        headers = [i for i, row in enumerate(rows) if row is not None and [c.strip() for c in row] == expected]
        if len(headers) != 1:
            fail(f'{path.name}: expected one task table with columns {expected}')
            continue
        details = re.findall(r'^###\s+(T[1-9]\d*)\s*$', text, re.M)
        seen = set()
        for row in rows[headers[0]+1:]:
            if row is None:
                break
            if all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in row):
                continue
            if len(row) != 5:
                fail(f'{path.name}: task row must have five cells')
                continue
            cells = [c.strip() for c in row]
            match = re.fullmatch(r'\[(T[1-9]\d*)\]\(#(t[1-9]\d*)\)', cells[0])
            if not match or match[1].lower() != match[2]:
                fail(f'{path.name}: task ID must link to its detail heading: {cells[0]}')
                continue
            task = match[1]
            if task in seen:
                fail(f'{path.name}: duplicate task {task}')
            seen.add(task)
            if details.count(task) != 1:
                fail(f'{path.name}: expected one detail section for {task}')
            if any(not cell for cell in cells[1:]):
                fail(f'{path.name}/{task}: empty task cell')
            # Remove Markdown link destinations before parsing dependency IDs.
            deps = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', cells[2])
            # A spaced display label still names the same scoped task.
            deps = re.sub(r'\b(M[1-9]\d*)\s*/\s*(T[1-9]\d*)\b', r'\1/\2', deps)
            refs = re.findall(r'(?<![\w/-])(?:[\w.-]+/)*T[1-9]\d*(?![\w/-])', deps)
            no_task_dependency = re.fullmatch(r'None(?:\s+\([^()]*\)|;\s+\S.*)?', deps) is not None
            if not no_task_dependency and not refs:
                fail(f'{path.name}/{task}: dependency must be None or a task reference')
            normalized = []
            for ref in refs:
                if '/' not in ref:
                    ref = f'{path.stem}/{ref}'
                if ref.count('/') > 1:
                    fail(f'{path.name}/{task}: external dependency {ref} requires manual validation')
                else:
                    normalized.append(ref)
            graph[f'{path.stem}/{task}'] = normalized
        if not seen:
            fail(f'{path.name}: no task rows')
        for task in set(details) - seen:
            fail(f'{path.name}: orphan detail section {task}')
    for task, deps in graph.items():
        for dep in deps:
            if dep not in graph:
                fail(f'{task}: missing dependency {dep}')
    active, visited = set(), set()
    def visit(task):
        if task in active:
            fail(f'Dependency cycle involving {task}')
            return
        if task in visited:
            return
        active.add(task)
        for dep in graph.get(task, []):
            visit(dep)
        active.remove(task)
        visited.add(task)
    for task in graph:
        visit(task)
    for path, text in documents.items():
        if text.lstrip().startswith('---\n'):
            fail(f'{path.name}: YAML frontmatter is not allowed')
        for target in re.findall(r'(?<!!)\[[^]\n]+\]\(([^)\s]+)\)', text):
            link = urlsplit(target.strip('<>'))
            if link.scheme or link.netloc:
                continue
            dest = (path.parent / unquote(link.path)).resolve() if link.path else path
            if not dest.is_relative_to(workspace):
                fail(f'{path.name}: link leaves workspace: {target}')
            elif not dest.exists():
                fail(f'{path.name}: broken link: {target}')
            elif link.fragment and dest.suffix == '.md':
                body = documents.get(dest)
                if body is None:
                    body = prose(dest.read_text())
                if unquote(link.fragment) not in anchors(body):
                    fail(f'{path.name}: missing anchor: {target}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--workspace', type=Path, required=True, help='Fixture workspace root; local links must stay inside it')
    parser.add_argument('--expectations', type=Path, required=True)
    args = parser.parse_args()
    expectations = json.loads(args.expectations.read_text())
    errors = check(args.plan.resolve(), args.workspace.resolve(), expectations['required_files'])
    print(json.dumps({'passed': not errors, 'errors': errors}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
