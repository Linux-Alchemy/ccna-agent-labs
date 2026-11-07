# Agent tools and skills

One Codex agent guides the work. It uses a main tutoring skill and loads a small sabotage procedure only when an exercise is requested. There is no separate saboteur agent.

**Status:** both skills, Packet Tracer scripts and templates are implemented. The first real chapter-and-ticket cycle is still pending; skill validation is not a claim that live troubleshooting has been completed.

## Responsibilities

| Learner | The agent |
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

## Use with your own agent

Codex is the tested host for this project. For Grok, Claude or another agent, use the same instructions through that host's skill loader if available, or supply the Markdown files directly. Other hosts have not been validated here.

1. **Keep the project together.** Clone or download the repo so the skills can refer to its scripts, templates and chapter records.
2. **Load the tutor instructions.** Give your agent the [main skill](skills/tutor/SKILL.md) and the project location. If it cannot open local files, attach or paste the instructions and relevant chapter/template material.
3. **Set your scope privately.** Ask the agent to create `local/learning-scope.md` with concepts you have covered, eligible troubleshooting topics and your progress sources. Keep this personal record out of git.
4. **Request a chapter review or exercise.** For an exercise, have the same agent read the [sabotage skill](skills/sabotage/SKILL.md) while retaining the main skill's restrictions. You still build and repair the network.

The full workflow needs file access, Python and git execution, plus Packet Tracer checks on your machine. A chat-only agent can discuss supplied material, but cannot edit your local lab or independently verify it. Attaching a skill does not grant those capabilities or hide its tool output.

A starting prompt:

> Read `agent/skills/tutor/SKILL.md` in my project at `<repo path>`, follow it as my lab tutor, and resume from the current chapter record. Ask for any missing scope information before assigning new work.

## Use with Codex

Open this repository as the working project in Codex. The checked-in `.agents/skills/` links point to the two skill folders under `agent/skills/`; no global installation is needed. Codex supports repo-local skill folders and symlinks. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

Ask Codex to use **ccna-agent-labs** to review the current chapter or resume an exercise. In clients supporting skill mentions, use `$ccna-agent-labs`. A requested run loads **ccna-agent-labs-sabotage** in the same context. If the skills do not appear, reopen the project/session and check that the relative symlinks resolve.

Example requests:

- "Use ccna-agent-labs and give me the Chapter 1 assignment."
- "Review my saved lab at <path>."
- "I'd like a troubleshooting session on the accepted chapter."
- "Pause this ticket" / "Resume my ticket" / "The fix is saved; check it."

The learner builds and repairs; the tutor maintains the records. No accepted baseline means no sabotage session yet. Separating skill files does not hide tool calls: an accidental answer disclosure is logged, not counted as an independent solve.
