"""Exercise observable structural failures with temporary generated plans."""
from pathlib import Path
import tempfile
import unittest

from check_structure import check


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.plan = self.workspace / 'plan'
        (self.plan / 'tasks').mkdir(parents=True)
        (self.plan / 'PRD.md').write_text('# PRD\n\n[Milestones](Milestone.md)\n')
        (self.plan / 'Milestone.md').write_text('# Milestones\n\n[M1](tasks/M1.md)\n')
        self.write_tasks('M1', [('T1', 'None'), ('T2', '[T1](#t1)')])

    def write_tasks(self, milestone, tasks):
        body = '# Tasks\n\n| Task | What to do | Depends on | Done when | Status |\n| --- | --- | --- | --- | --- |\n'
        for task, deps in tasks:
            body += f'| [{task}](#{task.lower()}) | Implement | {deps} | Observable outcome | Draft |\n'
        body += '\n## Execution order\n\nAccept prerequisites first.\n\n## Detailed task information\n'
        for task, _ in tasks:
            body += f'\n### {task}\n\nImplementation and verification.\n'
        (self.plan / 'tasks' / f'{milestone}.md').write_text(body)

    def errors(self):
        return check(self.plan, self.workspace, ['PRD.md', 'Milestone.md', 'tasks/M1.md'])

    def test_valid_and_cross_milestone_scoping(self):
        self.write_tasks('M2', [('T1', '[M1/T2](M1.md#t2)')])
        self.assertEqual([], self.errors())

    def test_verification_table_is_not_a_task_table(self):
        path = self.plan / 'tasks/M1.md'
        with path.open('a') as output:
            output.write('\n| Scenario | Expected |\n| --- | --- |\n| Empty input | Header only |\n')
        self.assertEqual([], self.errors())

    def test_none_with_external_condition_annotation(self):
        self.write_tasks('M1', [('T1', 'None (needs VM access)')])
        self.assertEqual([], self.errors())
        self.write_tasks('M1', [('T1', 'VM access')])
        self.assertTrue(any('dependency must be None' in e for e in self.errors()))

    def test_missing_file_and_broken_link(self):
        (self.plan / 'Milestone.md').unlink()
        errors = self.errors()
        self.assertTrue(any('Missing required' in e for e in errors))
        self.assertTrue(any('broken link' in e for e in errors))

    def test_missing_dependency(self):
        self.write_tasks('M1', [('T1', 'T9')])
        self.assertTrue(any('missing dependency M1/T9' in e for e in self.errors()))

    def test_none_with_semicolon_external_condition(self):
        self.write_tasks('M1', [('T1', 'None; external stakeholder decision')])
        self.assertEqual([], self.errors())

    def test_spaced_cross_milestone_label_is_not_a_local_self_cycle(self):
        self.write_tasks('M2', [('T2', '[M1 / T2](M1.md#t2)')])
        self.assertEqual([], self.errors())

    def test_cross_milestone_cycle(self):
        self.write_tasks('M1', [('T1', 'M2/T1')])
        self.write_tasks('M2', [('T1', 'M1/T1')])
        self.assertTrue(any('cycle' in e for e in self.errors()))

    def test_duplicate_task(self):
        self.write_tasks('M1', [('T1', 'None'), ('T1', 'None')])
        self.assertTrue(any('duplicate task' in e for e in self.errors()))

    def test_missing_anchor(self):
        (self.plan / 'PRD.md').write_text('[Task](tasks/M1.md#t99)\n')
        self.assertTrue(any('missing anchor' in e for e in self.errors()))

    def test_escaping_workspace(self):
        (self.plan / 'PRD.md').write_text('[Outside](../../outside.md)\n')
        self.assertTrue(any('leaves workspace' in e for e in self.errors()))

    def test_code_example_links_ignored(self):
        (self.plan / 'PRD.md').write_text('# PRD\n\n```markdown\n[Example](missing.md)\n```\n')
        self.assertEqual([], self.errors())

    def test_missing_detail_and_columns(self):
        path = self.plan / 'tasks/M1.md'
        body = path.read_text().replace('### T2', '### Other')
        path.write_text(body)
        self.assertTrue(any('detail section for T2' in e for e in self.errors()))
        path.write_text(body.replace('Depends on', 'Dependencies'))
        self.assertTrue(any('task table' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
