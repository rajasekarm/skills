---
name: learning-lens
description: "Turn a technical project idea into a precise learning question and a small, measurable experiment. Use when someone wants to learn by building, narrow a learning project, or identify what they actually need to understand. Not for ordinary product delivery without a learning goal."
---

# Learning Lens

Help the learner identify what they want to understand, then choose the smallest experiment that can teach it convincingly. A product idea is useful context; it does not automatically define the work to build.

## Find the learning question

Start with the user's stated goal and relevant existing context. Distinguish the example product, the underlying concept or behavior, and the evidence that would show understanding.

If the learning objective is missing, ask one focused question before proposing an architecture or implementation:

> What exactly do you want to understand or be able to explain after building this?

Make the question easier to answer with two or three possibilities grounded in their example. For a URL shortener, these might be high-throughput reads, generating unique short codes, or keeping reads correct during failures. Wait for the answer before finalizing a scope. If the learner is unsure, recommend a starting question with a reason and let them choose.

If they have already said “I want to understand the read path at 100k requests/sec,” use that objective directly. Ask the next question only if it materially changes the experiment, such as whether they mean an HTTP request through the full read path or a datastore operation alone. Avoid a long requirements questionnaire; label reasonable working assumptions and keep genuinely unresolved choices visible.

Phrase the objective as something the learner can explain, predict, diagnose, or demonstrate. “Learn caching” needs refinement; “Explain when caching reduces read latency and what happens when the working set stops fitting” is investigable. A performance number is a target condition, not the whole learning objective.

## Choose what must be built

Trace the path or mechanism needed to answer the question. Include a component only when removing it would hide the phenomenon being studied or prevent useful evidence. Use existing code or a mature service when recreating it teaches nothing relevant; implement a mechanism when its internals are the learning objective.

Preserve the constraints that make the question meaningful: representative data, request behavior, correctness requirements, and the relevant resource or failure boundary. A constant response or a tiny repeated lookup does not establish capacity for an intended dataset and workload. Synthetic data is suitable when it preserves the properties being studied.

Separate the minimal experiment from optional follow-ups. Do not add accounts, dashboards, deployment systems, analytics, or a complete product merely because the example usually includes them. Keep any product behavior the user explicitly wants to learn. If their objective is end-to-end delivery or interactions across components, a larger build can be justified; do not force every project into one endpoint.

Choose tools after the question and experiment are clear. Explain why each proposed component is needed. Do not automatically prescribe caches, shards, replicas, queues, or a particular stack.

## Design an experiment that teaches

Use a short learning loop, adapting its form to the question:

1. **Predict:** state a hypothesis and what observation would challenge it.
2. **Measure:** establish a simple baseline with a correctness check and relevant measurements.
3. **Expose the limit:** introduce a workload, resource constraint, or failure that makes the behavior visible.
4. **Change one mechanism:** choose a remedy based on the observed bottleneck; do not preselect the winning architecture.
5. **Repeat and explain:** compare under the same conditions, check correctness and recovery where relevant, and explain costs and trade-offs.

For conceptual goals, a trace, small simulation, or hand-worked example may provide better evidence than a benchmark. For performance goals, define the operation, workload, environment, measurement window, and success criteria. Pair throughput with latency, errors, and correct results. Keep proposed thresholds distinct from user requirements and observed results.

For high request rates, distinguish offered load, completed correct requests, and load-generator limits. Record enough context to interpret the result: dataset and working-set size, request distribution, warm/cold state, concurrency or arrival rate, test duration, resource limits, and cache hit/miss behavior when relevant. Select the important details for the current experiment instead of interrogating the learner about every variable at once.

Keep targets such as 100k requests/sec explicit. If available hardware cannot demonstrate the target, scope a smaller measured experiment and state the evidence gap. Ask the learner whether to pursue a larger setup when that changes time or cost; never silently replace the target or report extrapolated capacity as measured. A useful bottleneck diagnosis can satisfy a learning milestone even when the performance target remains unmet.

Include consistency, quorum, fault tolerance, or partition behavior when those affect the learning question. Do not append a distributed-systems syllabus to an unrelated experiment.

## Return a focused learning scope

Once the objective is clear, give a compact scope in ordinary language:

- **Learning question:** the one question this experiment should answer, and why it matters to the learner.
- **Evidence of understanding:** what they should be able to explain or predict, and the observation that would support it.
- **Smallest useful build:** the required path, data, components, and important assumptions.
- **Outside this experiment:** concrete features or related topics that can wait.
- **Experiment:** the baseline, limit to expose, next change to investigate, and comparison or correctness checks.
- **Done when:** separate the learning outcome from any performance target; name unresolved evidence honestly.

End with the next concrete action. Keep later ideas optional. Do not turn a scoping conversation into a full curriculum, PRD, implementation, or saved artifact unless requested. If building is already requested, use the clarified scope to guide that work without adding another approval ceremony.

## Reference case: URL-shortener idea, read-path objective

**Initial request:** “I want to build a URL shortener to learn system design.”

**Clarify:** “Which part do you want to understand: serving many reads, generating unique codes, or handling failures correctly?”

**Learner's answer:** “I want to understand a read path that supports 100k requests/sec.”

**Focused question:** “For a defined lookup workload, what limits correct end-to-end reads, and which change moves that limit while meeting an agreed latency and error budget?” Confirm what “read” includes if that is unclear; do not invent the latency budget or available hardware.

**Smallest useful build:** a seeded key-to-URL dataset, a lookup endpoint using an initial store, a load generator, and measurements of throughput, latency, errors, resource use, and result correctness. Include HTTP redirect behavior if it is part of the intended read boundary. A script or fixture can populate mappings; a public link-creation workflow is unnecessary for this question.

**Outside this experiment:** code generation, accounts, custom aliases, a management UI, click analytics, and billing, unless the learner explicitly includes one in their objective.

**First experiment:** measure the initial read path, increase load to expose saturation, identify where time or capacity is lost, then change the evidenced bottleneck and repeat with the workload held constant. Caching or partitioning are candidates to investigate when the evidence warrants them. Preserve representative key access and verify returned mappings so a fast incorrect response cannot count as success.

**Done when:** the learner can explain the limiting resource, use measurements to defend the change, describe its correctness and resource costs, and state whether 100k requests/sec was demonstrated under the recorded conditions or remains unproven. This does not require completing the whole URL-shortener product.
