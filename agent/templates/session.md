# <ticket-id> — <symptom title>

[Troubleshooting index](../troubleshooting.md) · [Chapter summary](../README.md) · [Build record](../build-record.md)

**State:** <planned / setup pending / active / paused / closed>

**Outcome:** <not started / pending / solved / solved with hints / answer-assisted / unresolved / spoiled by disclosure>

**Requester:** <name/role when established> · **Resolved by:** <learner or pending>

**Baseline:** <accepted chapter version; details below>

## Ticket

<Reported symptom and business impact only. For a planned placeholder, leave this pending; do not invent a complaint or start an exercise.>

**Confirmed observations:** <actual symptom checks, or pending>.

**Completion criteria:** <required restored behaviour and relevant unaffected checks, or pending>.

## Investigation

<!-- Clean up supplied notes and output into checks → observations → reasoning → action. Remove paste artefacts, repeated prompts and irrelevant lines; preserve failures, wrong turns, uncertainty and the learner's actual process. Retain exact commands/values or short excerpts when they provide useful evidence. -->

| Step | Check / action | Finding and reasoning |
|---|---|---|
| <step> | <what the learner actually checked or changed> | <observation, conclusion or next action> |

<!-- For a short run, the table is enough: remove the optional expanded log below. For a long run, keep the table as the concise investigation summary and preserve the full chronology below. Do not discard wrong turns or assistance when compacting. -->

<details>
<summary>Full investigation log</summary>

<Cleaned, detailed checks, observations, hypotheses, lookups and wrong turns in order. Distinguish learner reports from agent inspection and pasted output. Use selected excerpts where needed rather than automatically copying whole transcripts. Include a log here only when it adds useful detail beyond the summary.>

</details>

## Assistance

<Visible summary of hints/guidance, or explicitly none/not started. Preserve hints verbatim with level and time when known. Record explicit answer requests and disclosure. A lengthy hint transcript may be folded, but keep the assistance level and any answer reveal visible here.>

## Resolution

**Cause:** <learner's demonstrated diagnosis after resolution; pending while open; withhold an unrevealed cause if unresolved>.

**Repair:** <what the learner actually changed; pending or not repaired where appropriate>.

## Verification

| Check | Result | Evidence / source |
|---|---|---|
| <required check> | <pending / pass / fail / unverified> | <tutor saved-state inspection / learner-run test report / supplied output> |

<!-- Preserve meaningful counts, timeouts and interrupted tests. Identify before/after-repair evidence; do not present a pre-repair or partially successful test as a clean final pass. -->

**Outcome:** <concise disposition, including any workaround, remaining uncertainty and attribution. Do not claim agent-run tests without evidence.>

## Takeaway

<Short lesson grounded in the demonstrated investigation and repair; pending until there is evidence. Do not reveal an unrequested answer in an unresolved run.>

<details>
<summary>Run metadata</summary>

- **Private run ID:** <neutral identifier linking this ticket to its ignored run folder, or not assigned>.
- **Baseline identity:** <chapter, version/tag, SHA-256>.
- **Initial exercise SHA-256:** <after setup; otherwise pending>.
- **Repaired exercise SHA-256:** <after verification; otherwise pending>.
- **Answer commitment:** <SHA-256 and pre-ticket commit; never the sealed answer or undo details>.
- **Opened / closed:** <actual timestamps, or not opened/not closed>.
- **Active time:** <recorded or unknown; do not equate elapsed wall-clock time with active work>.

</details>

<!-- Collapsed sections reduce scrolling; they are public content, not a privacy boundary. Sealed answers, fault setup, private scope sources and scratch data stay under gitignored local/. -->
