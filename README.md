# ccna-agent-labs

I build an evolving business network from requirements. One agent assigns and reviews the work, creates optional troubleshooting exercises, and maintains the records. I configure the network and fix the faults.

I've created this project to accomplish two things. First is getting in more hands on work as I prepare for my CCNA exam. And second was to find a way to create a more real work like experience. There's real value in building labs for practice, of that there's no doubt. But I was looking for something that might be more similar to what one would see on the job. For example, you get handed a scope and you need to design the network, or maybe there's a network up and running and you're tasked with solving an issue. In this case, for the troubleshooting aspect of the project, I ask the agent to literally break something, not tell me what it is, and to only give me a ticket similar to what a network admin might see, my job then is to figure out what the problem is a fix it. 

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
- [Chapter 3: Separating the Network](chapters/03-separating-the-network/)
- [Agent overview](agent/README.md) — responsibilities and guidance for reuse.
- [Use the skills with your own agent](agent/README.md#use-with-your-own-agent) — Codex, Grok, Claude or another host.
- [Skills](agent/skills/), [scripts](agent/scripts/) and [templates](agent/templates/) — the supporting agent materials.

Each chapter has its own brief, design and acceptance record, with space for a topology screenshot, an accepted Packet Tracer file and a troubleshooting log. Later chapters are provisional.

## Current status

The repository scaffold is in place through Chapter 3, and both agent skills are implemented and discoverable in Codex. Lab builds and the first live chapter-and-ticket cycle are still pending; no chapter network or troubleshooting session has been completed. Missing screenshots and Packet Tracer files are marked with `.placeholder` files.

This is a project in progress, not a ready-to-run lab package.
