# ccna-agent-labs

I build an evolving business network from requirements. One agent assigns and reviews the work, creates optional troubleshooting exercises, and maintains the records. I configure the network and fix the faults.

I've created this project to accomplish two things. First is getting in more hands on work as I prepare for my CCNA exam. And second was to find a way to create a more real work like experience. There's real value in building labs for practice, of that there's no doubt. But I was looking for something that might be more similar to what one would see on the job. For example, you get handed a scope and you need to design the network, or maybe there's a network up and running and you're tasked with solving an issue. In this case, for the troubleshooting aspect of the project, I ask the agent to literally break something, not tell me what it is, and to only give me a ticket similar to what a network admin might see, my job then is to figure out what the problem is and fix it.

## How it works

The network starts in a solo indie game developer's spare room and grows with the business. Each chapter brings new requirements, design decisions and networking concepts.

1. Agree on the business need and learning goals.
2. Get a brief with requirements—not configuration instructions.
3. Design and build the network, then work through the agent's review.
4. Preserve the accepted network as a chapter baseline.
5. Optionally troubleshoot faults introduced on a copy of that baseline.
6. Expand when ready.

I do the networking. One agent handles assignments, reviews and record keeping, with a separate skill for setting up sabotage exercises. It doesn't build the network or repair it for me.

The records preserve design reasoning, investigation, wrong turns, hints and verification. My work and the agent's contributions stay clearly identified.

To keep the project honest, I'm keeping records, rather, the agent is keeping records. What was built, what was broken and how it was fixed. If at any point I'm utterly stumped and need more explicit assistance from the agent, then that gets recorded too.

## Find your way around

- [Chapter 1: The Spare Room](chapters/01-the-spare-room/)
- [Chapter 2: The First Hires](chapters/02-the-first-hires/)
- [Chapter 3: The First Office](chapters/03-the-first-office/)
- [Agent overview](agent/README.md) — responsibilities and guidance for reuse.
- [Use the skills with your own agent](agent/README.md#use-with-your-own-agent) — Codex, Grok, Claude or another host.
- [Skills](agent/skills/), [scripts](agent/scripts/) and [templates](agent/templates/) — the supporting agent materials.

Issued chapters have a short README with the story, topology and outcome, linked to a detailed assignment and build record. A troubleshooting index is added when the first exercise is planned. Each ticket has its own report under the chapter's troubleshooting/ folder. Chapters 1 and 2 have been issued. Chapter 3 is provisional.

## Current status

**Chapter 1 — The Spare Room is accepted (2026-11-21).** Its [summary and topology](chapters/01-the-spare-room/README.md) link to the [assignment](chapters/01-the-spare-room/assignment.md) and [detailed build record](chapters/01-the-spare-room/build-record.md). The preserved [spare-room.pkt](chapters/01-the-spare-room/spare-room.pkt) baseline is versioned as `chapter-1-v1`.

Acceptance combines saved-state inspection with Matt’s reported Packet Tracer connectivity, service and NAT tests. Tutoring assistance is recorded. The first publishable troubleshooting exercise, T001, is resolved without diagnostic hints; the accepted baseline is unchanged.

**Current work:** The [Chapter 2 assignment](chapters/02-the-first-hires/assignment.md) is issued. Both home offices use the existing HQ internet exit. A second Chapter 1 Tier 1 exercise is requested. The [T001 report](chapters/01-the-spare-room/troubleshooting/T001.md) is closed and approved.

This is a project in progress, not a ready-to-run lab package.
