# Agent tools and skills

One Codex agent guides the work. It uses a main tutoring skill and loads a small sabotage procedure only when an exercise is requested. There is no separate saboteur agent.

**Status:** the Packet Tracer scripts and draft templates are available. The two skill files are placeholders, not installed or operational. Full skill setup and a complete learning session are still to be validated.

## Responsibilities

| Matt | The agent |
|---|---|
| Designs and configures the network. | Issues requirements and reviews submitted work. |
| Investigates and repairs faults. | Creates scoped faults on disposable copies when requested. |
| Decides when to continue. | Maintains chapter records, hints, progress and reports. |

During review, the agent inspects the lab and gives investigation pointers; it does not repair it. During troubleshooting, hints are requested and logged. The answer is disclosed only on explicit request, and that assistance is recorded. Accepted baselines are never used as scratch files.

## What's here

- [Tutor skill placeholder](skills/tutor/SKILL.md.placeholder): chapter workflow, role and restrictions, reviews and upkeep.
- [Sabotage skill placeholder](skills/sabotage/SKILL.md.placeholder): scoped fault setup followed by a return to tutoring.
- [pt.py](scripts/pt.py): inspect topology/configurations, extract command history, lint and export/re-encode XML.
- [pktcrypto.py](scripts/pktcrypto.py): encoding/decoding helper used by `pt.py`.
- [Chapter template](templates/chapter.md): assignment, topology, design response and acceptance evidence.
- [Session template](templates/session.md): one section per exercise in a chapter's `troubleshooting.md`.

The scripts are the existing local Packet Tracer utilities, copied unchanged. Their source comments and format attribution are preserved. They use the Python standard library; there are no Python packages to install.

## Use the available scripts

From the repository root, set `LAB_FILE` to a real lab file:

```sh
LAB_FILE=/absolute/path/to/your-lab.pkt
python agent/scripts/pt.py summary "$LAB_FILE"
python agent/scripts/pt.py lint "$LAB_FILE"
python agent/scripts/pt.py log "$LAB_FILE" -g '^show ' -n 10
```

For a controlled edit on a copy:

```sh
mkdir -p local
python agent/scripts/pt.py xml "$LAB_FILE" -o local/lab.xml
# Edit only the intended XML fields, then use a NEW output filename.
python agent/scripts/pt.py encode local/lab.xml local/edited-copy.pkt
```

Do not overwrite an original or accepted baseline. Open the result in Packet Tracer to check it. The tools read saved state; they do not execute the simulation or prove connectivity. Lint findings are investigation leads, not a complete network assessment.

## Reuse the workflow

When the skills are complete, another learner will be able to use them with their own requirements and accepted network. The documented flow will be: load the project skills in Codex, supply a private record of familiar concepts, build from an assignment, request review, then optionally request an exercise.

Keep that personal scope record, sealed answers and working copies under the ignored `local/` directory. Keep reusable skill instructions generic. The exact Codex loading procedure is pending validation; the placeholder files must not be installed as finished skills.

Separating skill files does not hide tool calls. Exercise setup must avoid exposing the answer through ordinary output, and accidental disclosure must be recorded rather than counted as an independent solve.
