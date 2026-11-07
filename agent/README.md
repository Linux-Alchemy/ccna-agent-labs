# Agent tools and skills

One Codex agent guides the work. It uses a main tutoring skill and loads a small sabotage procedure only when an exercise is requested. There is no separate saboteur agent.

**Status:** both skills, Packet Tracer scripts and templates are implemented. The first real chapter-and-ticket cycle is still pending; skill validation is not a claim that live troubleshooting has been completed.

## Responsibilities

| Matt | The agent |
|---|---|
| Designs and configures the network. | Issues requirements and reviews submitted work. |
| Investigates and repairs faults. | Creates scoped faults on disposable copies when requested. |
| Decides when to continue. | Maintains chapter records, hints, progress and reports. |

During review, the agent inspects the lab and gives investigation pointers; it does not repair it. During troubleshooting, hints are requested and logged. The answer is disclosed only on explicit request, and that assistance is recorded. Accepted baselines are never used as scratch files.

## What's here

- [Tutor skill](skills/tutor/SKILL.md): chapter workflow, role and restrictions, reviews and upkeep.
- [Sabotage skill](skills/sabotage/SKILL.md): scoped fault setup followed by a return to tutoring.
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

## Use with Codex

Open this repository as the working project in Codex. The checked-in `.agents/skills/` links point to the two skill folders under `agent/skills/`; no global installation is needed. Codex supports repo-local skill folders and symlinks. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

Ask Codex to use **ccna-agent-labs** to review the current chapter or resume an exercise. In clients supporting skill mentions, use `$ccna-agent-labs`. A requested run loads **ccna-agent-labs-sabotage** in the same context. If the skills do not appear, reopen the project/session and check that the relative symlinks resolve.

Before assigning new work, the tutor reads `local/learning-scope.md`. For your own use, have the tutor create this private file with your current build concepts, troubleshooting-eligible topics, progress-source locations and the date/evidence of the last check. There is no required provider or curriculum. Keep personal scope sources, sealed answers and working copies under the ignored `local/` directory.

Example requests:

- "Use ccna-agent-labs and give me the Chapter 1 assignment."
- "Review my saved lab at <path>."
- "I'd like a troubleshooting session on the accepted chapter."
- "Pause this ticket" / "Resume my ticket" / "The fix is saved; check it."

The learner builds and repairs; the tutor maintains the records. No accepted baseline means no sabotage session yet. Separating skill files does not hide tool calls: an accidental answer disclosure is logged, not counted as an independent solve.
