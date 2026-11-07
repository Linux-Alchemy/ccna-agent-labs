---
name: ccna-agent-labs-sabotage
description: Prepare a requested troubleshooting exercise on a copy of an accepted CCNA Agent Labs Packet Tracer baseline, then return to tutoring. Requires the main tutor skill; do not use for unsolicited faults or ordinary build review.
---

# Prepare one exercise

Read the [main tutor skill](../tutor/SKILL.md) first if it is not loaded. Its boundaries stay in force. Use the same agent, not a subagent. Start only when the learner requests or accepts a run; resume an existing active/paused run instead of replacing it.

1. **Scope.** Identify the accepted chapter, baseline path/version/hash and learner's private troubleshooting ceiling. Allow only concepts both eligible and present in this network. Record components, exclusions and complexity; give the learner a broad scope without identifying the fault. Begin with one plausible addressing/gateway fault, not an obscure expert problem. Vary later runs using their recorded history.
2. **Copy.** Verify the accepted baseline and its passing checks. Create a unique neutral run ID and `local/runs/<id>/`; record the source hash and make an exercise copy. Never mutate the baseline, learner's working build or another ticket. Use `git check-ignore` and tracked-file checks before storing private details.
3. **Break.** Use [pt.py](../../scripts/pt.py) to export XML, change only the intended fields and encode a new exercise file. Preserve running/startup and duplicate fields consistently where required. A successful round trip does not prove the edit works in PT. Record exact changes and undo privately; setup may undo/discard an invalid fault before the ticket opens, never repair for the learner afterwards.
4. **Validate.** Re-read the output, compare intended changes and confirm the original hash is unchanged. Obtain actual PT evidence of the expected symptom against the previously passing checks, plus a relevant unaffected check. If needed, have the learner open the copy and run symptom-level tests without revealing the cause. If evidence is missing, leave setup pending; if the fault is invalid, discard/undo it. Do not present an unverified fault as a ready ticket.
5. **Seal.** Write `local/runs/<id>/answer.md`: scope, baseline/copy identities, fault, changes/undo, expected symptom and validation evidence. Hash the exact bytes with SHA-256; keep that record immutable. Add only neutral ticket/commitment metadata to the chapter's troubleshooting.md using the [session template](../../templates/session.md). Inspect the staged diff and commit the commitment before investigation begins; record the commit ID afterwards. Never commit the answer or unrelated changes. If sealing fails, stop setup rather than opening an unsealed ticket.
6. **Return to tutoring.** Present the symptom-only ticket and exercise-copy path, then follow the main skill. After opening, stop configuration writes; the learner diagnoses and repairs. Scope and sealing evidence do not authorise an answer reveal.

## Avoid accidental spoilers

Use neutral filenames and tool summaries; keep fault details in local files rather than printing XML, config diffs or the answer. Skill separation and gitignore do not hide tool traces. Do not promise secrecy the interface cannot provide. If the answer is exposed, record the run as spoiled and improve the method before another attempt; never present it as an independent solve.

Persist state across chats in the session record and private run folder. On resume, read the answer privately and verify its commitment and file identities before proceeding. Do not silently replace the answer, change the fault or start a second ticket.
