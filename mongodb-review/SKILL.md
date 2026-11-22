---
name: mongodb-review
description: "Review a change that touches MongoDB (Node.js driver or Mongoose) for data safety and performance: missing or wrong indexes, unbounded queries, N+1 access, unbounded document growth, schema validation, multi-document writes without transactions, query injection, and migrations that are unsafe to run twice. Read-only: reports findings with file:line evidence and a PASS/FAIL verdict, never edits code. Use when reviewing a diff, PR, branch, or plan task that changes models, queries, aggregations, indexes, or migrations. Not for SQL databases."
---

# MongoDB Review

Review what a change does to data: whether it stays correct, stays fast as collections grow, and can be deployed and rolled back safely. You report; you never edit code, run migrations, or write to a database.

## 1. Scope the review

Work out what to review, in this order:

1. A diff, PR, branch, commit range, or file list you were given.
2. Otherwise the working tree: `git diff` plus `git diff --staged`; if both are empty, the current branch against its base (`git merge-base HEAD main`, or `master`).

If nothing in scope touches MongoDB, say "No MongoDB changes in scope" with what you checked, give verdict PASS, and stop.

MongoDB code includes: Mongoose schemas and models, driver calls (`collection.find/insert*/update*/delete*/aggregate/bulkWrite`, `findOneAndUpdate`), aggregation pipelines, index definitions (`schema.index`, `createIndex`, `autoIndex` settings), migration scripts, and repository or service code that builds query filters.

## 2. Read in this order

1. **Tests first.** They show the intended behavior. Note missing coverage for new queries or write paths.
2. **Schemas and index definitions** for every collection the change reads or writes, including unchanged ones it now queries differently.
3. **The changed queries and writes,** following each to its callers so you know the input sizes and where filter values come from.
4. **Migrations** and any deploy-order assumptions.

Ground every finding in code you read. Cite `file:line`. Do not report a problem you could not trace.

## 3. Checks

### Indexes and query shape
- Every new or changed filter, sort, and `$lookup` foreign field is served by an index. Check compound index **field order** against equality → sort → range.
- A new index on a large collection: note build impact, and whether the deploy relies on `autoIndex` in production (it should not).
- Removed or renamed fields that existing indexes or queries still use.
- Regex filters without an anchored prefix, `$where`, and `$expr` on hot paths: these cannot use indexes well.

### Bounded reads
- `find` or `aggregate` on user-scale data without `limit`, pagination, or a bounded filter.
- Offset pagination (`skip`) on large or growing collections; prefer range pagination on an indexed field.
- Missing projection when documents are large and only a few fields are used.
- `countDocuments` on hot paths where an estimate or a cached count would do.

### Access patterns
- **N+1:** a query inside a loop or `Promise.all(map(...))` over results; prefer `$in`, `$lookup`, or one batched query.
- Mongoose `populate` chains that fan out into many queries.
- Read-modify-write in application code (`findOne`, change, `save`) where a concurrent request can interleave; prefer an atomic update operator, a conditional filter, or a version field.

### Document design
- Arrays that grow without limit inside a document (comments, events, logs): risk of the 16 MB limit and slow updates. Prefer a separate collection or a bucket pattern.
- Embedding versus referencing: does the access pattern justify it?
- New required fields: are existing documents without the field handled (default, backfill, or tolerant reads)?

### Writes and consistency
- Writes across more than one document or collection that must succeed together, without a transaction or an idempotent recovery path.
- Upserts that need a unique index to prevent duplicates under concurrency.
- Write concern or read preference changes that weaken consistency for data that must be correct.
- `updateMany` or `deleteMany` whose filter could match more than intended, for example an empty or undefined filter value.

### Validation and security
- Filter values taken from request input without type checks: `{ email: req.body.email }` accepts `{ "$ne": null }`. Require schema validation or casting, or reject objects where strings are expected.
- `$where`, `mapReduce`, or `$function` with any user input.
- Mongoose `strict` or `strictQuery` disabled, or schemaless writes that let unknown fields in.
- Sensitive fields returned without projection, or logged.

### Migrations
- Safe to run twice: guarded by a filter, a marker, or a migration record.
- Batched for large collections, not one unbounded `updateMany` holding resources.
- Deploy order works: old code against new data, and new code against old data, during rollout.
- A rollback path exists, or the change is explicitly forward-only and says so.

## 4. Severity

- **Critical:** data loss or corruption, a security hole, or an outage risk. Blocks merge.
- **Important:** a performance or consistency problem that will show at realistic scale. Fix before merge unless deferred with a reason.
- **Nit:** a minor improvement. The author may decline.
- **FYI:** an observation, no action needed.

Improve health, not perfection: do not block on unrelated existing issues. Mention a pre-existing problem only if the change makes it worse, and label it as pre-existing.

## 5. Output

```
## MongoDB review: PASS | FAIL

Scope: <what was reviewed, e.g. branch plan/csv-export vs main, 6 files>
Collections touched: <names>

### Findings
1. [Critical] <problem> — <file:line>
   Why: <consequence at realistic scale or under concurrency>
   Fix: <the smallest change that resolves it>
2. ...

### Checked, no findings
<check groups from section 3 that were examined and found clean>

### Not checked
<anything you could not verify and why, e.g. collection sizes unknown, no access to index list in production>
```

The verdict is FAIL if there is any Critical or Important finding, otherwise PASS. If you are unsure of collection sizes, say what size would make a finding matter rather than guessing.
